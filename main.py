import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import sys

# --- 1. 配置与常量 ---
# 动态计算项目路径，确保可移植性
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
VOCABULARY_FILE = os.path.join(DATA_DIR, 'words_with_phonetics.txt')
PROGRESS_FILE = os.path.join(BASE_DIR, 'progress.json')


# --- 2. 数据模型 ---
class Word:
    """一个简单的数据类，用于封装单词信息。"""
    def __init__(self, english, phonetics, definition):
        self.english = english
        self.phonetics = phonetics
        self.definition = definition

class VocabularyManager:
    """
    负责所有数据相关逻辑的类：
    - 加载单词文件
    - 加载和保存学习进度
    """
    def __init__(self, filepath, progress_path):
        self.filepath = filepath
        self.progress_path = progress_path
        self.words = self._load_vocabulary()

    def _load_vocabulary(self):
        """从 .txt 文件加载和解析单词，返回 Word 对象列表。"""
        words = []
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('\t')
                        if len(parts) == 3:
                            word = Word(parts[0], parts[1], parts[2])
                            words.append(word)
        except FileNotFoundError:
            messagebox.showerror(
                "错误", 
                f"未找到单词文件 '{self.filepath}'。\n\n请确保文件存在，或先运行 'scripts/add_phonetics.py' 生成该文件。"
            )
            sys.exit(1)
        except Exception as e:
            messagebox.showerror("文件读取错误", f"读取文件时发生错误: {e}")
            sys.exit(1)
        return words

    def load_progress(self):
        """加载用户进度，返回一个有效的索引值。"""
        if os.path.exists(self.progress_path):
            try:
                with open(self.progress_path, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                    index = progress.get("current_index", 0)
                    # 关键检查：确保索引在加载后仍然有效，防止单词列表缩短导致越界
                    if 0 <= index < len(self.words):
                        return index
            except (json.JSONDecodeError, TypeError):
                # 如果文件损坏或为空，则从头开始
                return 0
        return 0

    def save_progress(self, current_index):
        """将当前单词索引保存到进度文件。"""
        progress = {"current_index": current_index}
        with open(self.progress_path, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=4)


# --- 3. 主应用界面 ---
class EngramApp:
    """
    负责UI界面的创建、布局和用户交互。
    """
    # 使用类常量避免“魔法字符串”
    MODE_EN_TO_ZH = 'en_to_zh'
    MODE_ZH_TO_EN = 'zh_to_en'

    def __init__(self, root):
        self.root = root
        self.root.title("Engram - 单词记忆应用")
        self.root.geometry("600x400")

        # 实例化数据管理器
        self.vocab_manager = VocabularyManager(VOCABULARY_FILE, PROGRESS_FILE)
        self.words = self.vocab_manager.words

        # 健壮性检查：如果单词列表为空，则提示并退出
        if not self.words:
            messagebox.showerror("错误", f"'{VOCABULARY_FILE}' 文件为空或格式不正确。")
            self.root.quit()
            return
            
        self.current_index = self.vocab_manager.load_progress()
        self.current_word = None
        
        self._setup_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.show_word_sequentially()

    def _on_closing(self):
        """关闭应用前保存进度。"""
        self.vocab_manager.save_progress(self.current_index)
        self.root.destroy()

    def _setup_widgets(self):
        """创建界面组件。"""
        # --- 显示区域 ---
        self.main_frame = tk.Frame(self.root, pady=20)
        self.main_frame.pack(expand=True, fill="both")

        self.english_label = tk.Label(self.main_frame, text="", font=("Arial", 36, "bold"))
        self.english_label.pack(pady=10)
        self.phonetics_label = tk.Label(self.main_frame, text="", font=("Arial", 18))
        self.phonetics_label.pack(pady=5)
        self.definition_label = tk.Label(self.main_frame, text="", font=("Arial", 16), wraplength=500, justify='center')
        self.definition_label.pack(pady=10)
        
        # --- 拼写测试输入框和反馈 ---
        self.spell_entry = tk.Entry(self.main_frame, font=("Arial", 18), justify='center')
        self.feedback_label = tk.Label(self.main_frame, text="", font=("Arial", 14), fg="blue")

        # --- 控制按钮区域 ---
        self.control_frame = tk.Frame(self.root, pady=10)
        self.control_frame.pack(fill="x", side="bottom")

        # --- 模式切换区域 ---
        self.mode_frame = tk.Frame(self.root, pady=10)
        self.mode_frame.pack(fill="x", side="bottom")

        tk.Button(self.mode_frame, text="顺序学习", command=self.show_word_sequentially).pack(side="left", expand=True)
        tk.Button(self.mode_frame, text="英译中抽查", command=lambda: self.start_flashcard_mode(self.MODE_EN_TO_ZH)).pack(side="left", expand=True)
        tk.Button(self.mode_frame, text="中译英抽查", command=lambda: self.start_flashcard_mode(self.MODE_ZH_TO_EN)).pack(side="left", expand=True)
        tk.Button(self.mode_frame, text="拼写测试", command=self.start_spelling_test).pack(side="left", expand=True)

    def _clear_view(self):
        """清理界面，为切换到新模式做准备。"""
        for widget in self.control_frame.winfo_children():
            widget.destroy() # 使用destroy彻底移除旧按钮
        self.english_label.config(text="")
        self.phonetics_label.config(text="")
        self.definition_label.config(text="")
        self.spell_entry.pack_forget()
        self.feedback_label.pack_forget()

    def update_word_display(self, show_def=True):
        """更新显示的单词信息。"""
        self.current_word = self.words[self.current_index]
        self.english_label.config(text=self.current_word.english)
        self.phonetics_label.config(text=self.current_word.phonetics)
        self.definition_label.config(text=self.current_word.definition if show_def else "")

    def show_word_sequentially(self):
        """顺序学习模式。"""
        self._clear_view()
        tk.Button(self.control_frame, text="上一个", command=self.prev_word).pack(side="left", expand=True)
        tk.Button(self.control_frame, text="显示/隐藏释义", command=self.toggle_definition).pack(side="left", expand=True)
        tk.Button(self.control_frame, text="下一个", command=self.next_word).pack(side="right", expand=True)
        self.update_word_display()

    def next_word(self):
        self.current_index = (self.current_index + 1) % len(self.words)
        self.update_word_display()

    def prev_word(self):
        self.current_index = (self.current_index - 1 + len(self.words)) % len(self.words)
        self.update_word_display()
    
    def toggle_definition(self):
        if self.definition_label.cget("text"):
            self.definition_label.config(text="")
        else:
            self.definition_label.config(text=self.current_word.definition)

    def start_flashcard_mode(self, mode):
        """开始闪卡抽查模式。"""
        self._clear_view()
        self.current_word = random.choice(self.words)
        
        if mode == self.MODE_EN_TO_ZH:
            self.english_label.config(text=self.current_word.english)
            self.phonetics_label.config(text=self.current_word.phonetics)
        else: # MODE_ZH_TO_EN
            self.definition_label.config(text=self.current_word.definition)

        def show_answer():
            self.english_label.config(text=self.current_word.english)
            self.phonetics_label.config(text=self.current_word.phonetics)
            self.definition_label.config(text=self.current_word.definition)

        tk.Button(self.control_frame, text="显示答案", command=show_answer).pack(side="left", expand=True)
        tk.Button(self.control_frame, text="下一个", command=lambda: self.start_flashcard_mode(mode)).pack(side="right", expand=True)

    def start_spelling_test(self):
        """开始拼写测试模式。"""
        self._clear_view()
        self.current_word = random.choice(self.words)
        self.phonetics_label.config(text=self.current_word.phonetics)
        self.definition_label.config(text=self.current_word.definition)
        
        self.spell_entry.pack(pady=10)
        self.spell_entry.delete(0, tk.END)
        self.spell_entry.focus_set()
        self.feedback_label.pack(pady=5)
        self.feedback_label.config(text="")
        
        self.spell_entry.bind("<Return>", self.check_spelling)
        tk.Button(self.control_frame, text="检查拼写", command=self.check_spelling).pack(side="left", expand=True)
        tk.Button(self.control_frame, text="下一个", command=self.start_spelling_test).pack(side="right", expand=True)

    def check_spelling(self, event=None):
        user_input = self.spell_entry.get().strip()
        if user_input.lower() == self.current_word.english.lower():
            self.feedback_label.config(text="正确!", fg="green")
            self.root.after(1000, self.start_spelling_test)
        else:
            self.feedback_label.config(text=f"错误, 正确答案是: {self.current_word.english}", fg="red")

# --- 4. 程序入口 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = EngramApp(root)
    root.mainloop()