import argparse
import sys

def convert_to_markdown_table(input_file, output_file):
    """
    将特定格式的文本文件转换为带有复选框的 Markdown 表格。

    输入文件格式: 'word\t[phonetics]\tdefinition'
    """
    print(f"正在从 {input_file} 生成 Markdown 文件...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', encoding='utf-8') as f_out:

            # 写入 Markdown 表格的头部
            f_out.write("| 完成 | 单词 | 发音 | 释义 |\n")
            f_out.write("|:----:|:----|:----|:----|\n")

            # 逐行读取和转换
            for i, line in enumerate(f_in, 1):
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    word, pronunciation, definition = parts[0], parts[1], parts[2]
                    
                    # 写入表格行，并在第一列添加一个未选中的复选框
                    f_out.write(f"| [ ] | {word} | {pronunciation} | {definition} |\n")
                else:
                    print(f"警告: 第 {i} 行格式不正确，已跳过: '{line}'", file=sys.stderr)
        
        print(f"成功将 {input_file} 转换为 {output_file}")

    except FileNotFoundError:
        print(f"错误: 找不到输入文件 '{input_file}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"发生未知错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="将单词列表转换为带有复选框的 Markdown 表格。",
        epilog="示例: python scripts/convert_to_markdown.py data/words_with_phonetics.txt vocabulary.md"
    )
    
    parser.add_argument("input_file", help="输入的带音标的单词文件路径。")
    parser.add_argument("output_file", help="输出的 Markdown 文件路径。")
    
    args = parser.parse_args()
    
    convert_to_markdown_table(args.input_file, args.output_file)