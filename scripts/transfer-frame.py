import os
import re

def replace_frame_with_md_image(content):
    # 使用正则表达式匹配 Frame 和 img 标签
    frame_pattern = r'<Frame[^>]*>\s*<img src="([^"]*)"[^>]*>\s*</Frame>'
    # 替换为 Markdown 图片格式
    content = re.sub(frame_pattern, r'![](\1)', content)
    
    # 匹配 figure 标签格式
    figure_pattern = r'<figure><img src="([^"]*)"[^>]*><figcaption>(?:<p>)?(.*?)(?:</p>)?</figcaption></figure>'
    # 如果 figcaption 中有内容就作为图片描述，否则留空
    content = re.sub(figure_pattern, lambda m: f'![{m.group(2)}]({m.group(1)})' if m.group(2) else f'![]({m.group(1)})', content)
    
    return content

def process_md_files(directory):
    # 遍历目录下的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 替换内容
                    new_content = replace_frame_with_md_image(content)
                    
                    # 如果内容有变化，写回文件
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    # 指定要处理的目录路径，这里使用当前目录
    directory = "."
    process_md_files(directory)