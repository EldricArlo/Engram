好的，项目取名为 **Engram** 非常棒，这个词本身就与记忆和学习紧密相关，很有深意。

遵从您的指示，我将分部分为您提供完整的、重构后的项目代码。我们将从项目的基础结构和说明文件开始，这能帮助您理解所有代码文件应该如何组织。

---

### **第一部分：项目基础结构与说明文件**

一个优秀的项目，始于一个清晰的结构和一份完善的说明文档。这能让您或任何其他协作者快速上手。

#### **1. 项目目录结构**

首先，请按照下面的结构创建文件夹和空白文件。这将是我们放置后续代码的“骨架”。

```
engram/
│
├── data/                    # 用于存放所有数据文件
│
├── scripts/                 # 用于存放辅助脚本
│
├── main.py                  # 主应用程序（稍后填充代码）
├── README.md                # 项目说明文件（代码见下方）
└── requirements.txt         # 项目依赖库文件（代码见下方）
```

*   您需要在 `engram` 文件夹内手动创建 `data` 和 `scripts` 这两个子文件夹。

#### **2. 依赖声明文件 (`requirements.txt`)**

这个文件非常简单，它告诉 Python 需要安装哪个第三方库来运行我们的脚本。

**文件名：`requirements.txt`** (放置在项目根目录 `engram/` 下)

```txt
# 用于将英文单词转换为国际音标 (IPA)
eng-to-ipa==0.0.2
```

*   **使用方法：** 用户在终端里进入 `engram` 目录后，只需运行 `pip install -r requirements.txt` 即可安装好所需依赖。

#### **3. 项目说明文件 (`README.md`)**

这是整个项目的“使用说明书”，至关重要。它解释了项目的用途、如何安装、以及详细的使用流程。一个好的 `README.md` 文件可以极大地提升项目的专业性和可用性。

**文件名：`README.md`** (放置在项目根目录 `engram/` 下)

````markdown
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
````

---

现在，我们已经为 **Engram** 项目打好了坚实的基础。您已经拥有了清晰的目录结构和完善的说明文档。

**请告诉我“继续”，我将为您提供第二部分：重构后的两个辅助脚本 (`scripts/` 目录下的文件) 的完整代码。**