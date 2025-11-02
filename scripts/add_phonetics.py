import eng_to_ipa as ipa
import argparse
import sys

def add_phonetics_to_file(input_file, output_file):
    """
    读取一个包含单词和释义的文件，为每个单词添加音标，并写入新文件。

    输入文件格式: 'word definition' (使用空格或制表符分隔)
    输出文件格式: 'word\t[phonetics]\tdefinition' (使用制表符分隔)
    """
    print(f"正在处理文件: {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:

            for i, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue

                # 使用 maxsplit=1 分割，确保只分割一次，保留释义的完整性
                parts = line.split(maxsplit=1)
                
                if len(parts) < 2:
                    print(f"警告: 第 {i} 行格式不正确，已跳过: '{line}'", file=sys.stderr)
                    continue
                
                word, definition = parts[0], parts[1]
                
                # 获取单词的音标
                phonetics = ipa.convert(word)
                
                # 构建新的行，格式为：单词\t[音标]\t释义
                new_line = f"{word}\t[{phonetics}]\t{definition}\n"
                outfile.write(new_line)

        print(f"处理完成！结果已保存到 {output_file}")

    except FileNotFoundError:
        print(f"错误: 找不到输入文件 '{input_file}'", file=sys.stderr)
        sys.exit(1) # 退出程序并返回错误码
    except Exception as e:
        print(f"发生未知错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # 1. 创建一个命令行参数解析器
    parser = argparse.ArgumentParser(
        description="为单词文件添加音标。",
        epilog="示例: python scripts/add_phonetics.py data/words.txt data/words_with_phonetics.txt"
    )
    
    # 2. 添加需要的参数
    parser.add_argument("input_file", help="输入的原始单词文件路径 (例如: data/words.txt)")
    parser.add_argument("output_file", help="输出的带音标的文件路径 (例如: data/words_with_phonetics.txt)")
    
    # 3. 解析命令行参数
    args = parser.parse_args()
    
    # 4. 调用主函数
    add_phonetics_to_file(args.input_file, args.output_file)