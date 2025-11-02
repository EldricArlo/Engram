# Engram - 单词记忆应用

Engram 是一款帮助用户记忆英语单词的桌面应用程序。它提供多种学习和测试模式，并能自动保存学习进度。

## 功能特性

- **数据预处理**：自动为单词列表添加国际音标。
- **多种学习模式**：
    - **顺序学习**：按顺序浏览和学习单词。
    - **英译中抽查**：随机显示英文单词，测试中文释义。
    - **中译英抽查**：随机显示中文释义，测试英文单词。
    - **拼写测试**：听音标、看释义，拼写单词。
- **进度管理**：自动保存和加载学习进度，方便下次继续。
- **数据导出**：可将单词列表导出为带复选框的 Markdown 表格，方便打印和离线学习。

## 项目结构

```
engram/
│
├── data/
│   ├── words.txt                   # 【用户提供】原始单词文件
│   └── words_with_phonetics.txt    # 【脚本生成】带音标的单词文件
│
├── scripts/
│   ├── add_phonetics.py            # 添加音标的脚本
│   └── convert_to_markdown.py      # 转换为Markdown的脚本
│
├── main.py                         # 主应用程序入口
├── progress.json                   # 【程序生成】学习进度文件
├── vocabulary.md                   # 【脚本生成】导出的Markdown文件
├── README.md                       # 本说明文件
└── requirements.txt                # 项目依赖库
```

## 使用流程

### 步骤一：首次设置与数据准备

1.  **准备单词源文件**：
    准备一个UTF-8编码的文本文件，每行包含一个单词和它的释义，用一个或多个空格隔开。例如：
    ```
    apple 苹果
    banana 香蕉
    ```
    将此文件命名为 `words.txt` 并放入 `data` 文件夹。

2.  **安装依赖库**：
    打开终端（或命令行），进入项目根目录 `engram/`，然后运行以下命令：
    ```bash
    pip install -r requirements.txt
    ```

3.  **生成带音标的单词文件**：
    继续在终端中运行以下命令，为您的单词列表添加音标。脚本会自动读取 `data/words.txt` 并生成 `data/words_with_phonetics.txt`。
    ```bash
    python scripts/add_phonetics.py data/words.txt data/words_with_phonetics.txt
    ```
    现在，您的学习资料已准备就绪。

### 步骤二：日常学习

当您想背单词时，只需在终端中运行主程序：

```bash
python main.py
```
程序启动后，会加载 `data/words_with_phonetics.txt` 的内容。关闭窗口时，学习进度会自动保存在 `progress.json` 文件中。

### 步骤三：导出为Markdown（可选）

如果您希望将单词列表打印出来，可以运行以下命令：

```bash
python scripts/convert_to_markdown.py data/words_with_phonetics.txt vocabulary.md
```
该命令会在项目根目录下生成一个名为 `vocabulary.md` 的文件。