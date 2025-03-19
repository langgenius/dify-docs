#此代码可以直接对比三份不同语言版本，找出下面几点：
# 1. 标题格式不正确：比如，中文版里小标题都是###，英文版却是####；再比如中文版里标题是普通格式，但英文版里标题加粗或是倾斜。
# 2. 文字格式不正确：比如，中文版有三段内容，英文版却有两段。
# 3. 图片缺失：比如，英文版内的小标题里有一张照片，日语版里没有或者有两张。
# 4. 文件不正确：比如中文版内的一个文件夹里有三份文件，但日语版内只有两份或者是有四份。

# 使用方式：
# 在命令行依次输入下面的命令
# cd middleware
# python md_comparator.py (或者 python3 md_comparator.py)

# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path
from collections import defaultdict

class MDComparator:
    def __init__(self, zh_path, en_path, ja_path):
        self.paths = {'zh': zh_path, 'en': en_path, 'ja': ja_path}
        self.report = defaultdict(list)
        self.report_file = Path("comparison_report.md")  # 固定报告文件名
        self.summary_files = {
            'zh': 'SUMMARY.md',
            'en': 'SUMMARY.md', 
            'ja': 'SUMMARY.md'
        }

    def compare_all(self):
        self._compare_directory_structure()
        self._compare_summary_files()  # 新增的SUMMARY对比
        for file_path in self._get_all_md_files():
            self._compare_file(file_path)
        self.generate_report()

    # 新增的SUMMARY对比方法
    def _compare_summary_files(self):
        """对比各语言版本的SUMMARY.md目录结构"""
        summary_contents = {}
        
        # 读取各语言SUMMARY文件内容
        for lang in ['zh', 'en', 'ja']:
            summary_path = os.path.join(self.paths[lang], self.summary_files[lang])
            try:
                with open(summary_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                summary_contents[lang] = self._parse_summary(content)
            except FileNotFoundError:
                self.report['directory_structure'].append(
                    f"{lang.upper()} SUMMARY文件缺失: {self.summary_files[lang]}"
                )
                summary_contents[lang] = set()

        # 先检查英文版
        self._compare_single_lang_summary('en', summary_contents)
        # 添加分隔标记
        self.report['summary_structure'].append("--- ENGLISH CHECK COMPLETED / 日文检查开始 ---")
        # 再检查日语版
        self._compare_single_lang_summary('ja', summary_contents)

    def _compare_single_lang_summary(self, lang, summary_contents):
        """对比单个语言的SUMMARY差异"""
        all_paths = summary_contents['zh'].union(summary_contents['en'], summary_contents['ja'])
        
        # 检查缺失路径
        for path in summary_contents['zh'] - summary_contents[lang]:
            self.report['summary_structure'].append(
                f"{lang.upper()} SUMMARY缺失路径: {path} (存在于中文版)"
            )
            
        # 检查多余路径
        for path in summary_contents[lang] - summary_contents['zh']:
            self.report['summary_structure'].append(
                f"{lang.upper()} SUMMARY多余路径: {path} (不存在于中文版)"
            )
    def _parse_summary(self, content):
        """解析SUMMARY.md文件，提取所有md路径"""
        paths = set()
        # 匹配所有[...](...)格式的链接
        pattern = re.compile(r'\[.*?\]\((.*?\.md)\)')
        
        # 递归处理嵌套列表
        stack = []
        for line in content.split('\n'):
            # 计算缩进级别
            indent = len(re.match(r'^(\s*)\*', line).group(1)) if re.match(r'^\s*\*', line) else 0
            
            # 维护缩进栈
            while stack and stack[-1][0] >= indent:
                stack.pop()
            
            # 解析当前行路径
            match = pattern.search(line)
            if match:
                path = match.group(1)
                # 拼接父级路径
                full_path = os.path.join(*[p[1] for p in stack], path)
                paths.add(full_path.replace('\\', '/'))  # 统一使用斜杠
                
                # 如果是目录节点，加入栈
                if line.strip().endswith('.md') and not line.strip().startswith('*'):
                    stack.append((indent, os.path.dirname(path)))
        
        return paths

    def _get_all_md_files(self):
        """获取中文版目录下所有md文件的相对路径"""
        md_files = []
        for root, _, files in os.walk(self.paths['zh']):
            for file in files:
                if file.endswith('.md'):
                    rel_path = os.path.relpath(root, self.paths['zh'])
                    md_files.append(os.path.join(rel_path, file))
        return md_files

    def _compare_directory_structure(self):
        """对比目录结构差异"""
        for lang in ['en', 'ja']:
            for root, _, files in os.walk(self.paths['zh']):
                rel_path = os.path.relpath(root, self.paths['zh'])
                target_dir = os.path.join(self.paths[lang], rel_path)
                print(rel_path)
                
                # 检查目标目录是否存在
                if not os.path.exists(target_dir):
                    self.report['directory_structure'].append(
                        f"{lang.upper()} 目录缺失: {rel_path}"
                    )
                    continue
                
                # 比较文件数量
                zh_files = set(f for f in files if f.endswith('.md'))
                target_files = set(f for f in os.listdir(target_dir) if f.endswith('.md'))
                
                if len(zh_files) != len(target_files):
                    diff = zh_files.symmetric_difference(target_files)
                    self.report['directory_structure'].append(
                        f"{lang.upper()} 文件数量不一致: {rel_path} "
                        f"(ZH: {len(zh_files)}, {lang.upper()}: {len(target_files)})\n"
                        f"差异文件: {', '.join(diff)}"
                    )

    def _compare_file(self, rel_path):
        """对比单个文件内容"""
        contents = {}
        try:
            for lang in ['zh', 'en', 'ja']:
                full_path = os.path.join(self.paths[lang], rel_path)
                with open(full_path, 'r', encoding='utf-8') as f:
                    contents[lang] = f.read()
        except FileNotFoundError as e:
            self.report['directory_structure'].append(f"文件缺失: {rel_path} ({e})")
            return

        self._compare_headings(contents, rel_path)
        self._compare_paragraphs(contents, rel_path)
        self._compare_images(contents, rel_path)

    # ------------------- 标题对比逻辑 -------------------
    def _compare_headings(self, contents, rel_path):
        """对比各语言标题结构"""
        headings = {}
        for lang, content in contents.items():
            lang_headings = []
            # 添加flags参数修复正则匹配问题
            for match in re.finditer(r'^(#{1,6})\s*(\*?)(.*?)(\*?)\s*$', content, flags=re.M):
                level = len(match.group(1))
                is_bold = '**' in match.group(0)
                is_italic = '*' in match.group(0) and not is_bold
                lang_headings.append({
                    'level': level,
                    'bold': is_bold,
                    'italic': is_italic,
                    'text': match.group(3).strip()
                })
            headings[lang] = lang_headings

        # 以中文版为基准进行对比
        zh_headings = headings['zh']
        for lang in ['en', 'ja']:
            if lang not in headings:
                continue

            other_headings = headings[lang]
            
            # 检查标题数量
            if len(zh_headings) != len(other_headings):
                self.report['headings'].append(
                    f"{lang.upper()} 标题数量不一致: {rel_path} "
                    f"(ZH: {len(zh_headings)}, {lang.upper()}: {len(other_headings)})"
                )
                continue

            # 逐个对比标题属性
            for i, (zh_h, other_h) in enumerate(zip(zh_headings, other_headings)):
                # 比较标题级别
                if zh_h['level'] != other_h['level']:
                    self.report['headings'].append(
                        f"{lang.upper()} 标题级别不一致: {rel_path} 第{i+1}个标题 "
                        f"(ZH: {'#'*zh_h['level']}, {lang.upper()}: {'#'*other_h['level']})"
                    )
                
                # 比较粗体样式
                if zh_h['bold'] != other_h['bold']:
                    self.report['headings'].append(
                        f"{lang.upper()} 标题粗体不一致: {rel_path} 第{i+1}个标题 "
                        f"(ZH: {'加粗' if zh_h['bold'] else '无'}, "
                        f"{lang.upper()}: {'加粗' if other_h['bold'] else '无'})"
                    )
                
                # 比较斜体样式
                if zh_h['italic'] != other_h['italic']:
                    self.report['headings'].append(
                        f"{lang.upper()} 标题斜体不一致: {rel_path} 第{i+1}个标题 "
                        f"(ZH: {'斜体' if zh_h['italic'] else '无'}, "
                        f"{lang.upper()}: {'斜体' if other_h['italic'] else '无'})"
                    )

    # ------------------- 段落对比逻辑 -------------------
    def _compare_paragraphs(self, contents, rel_path):
        """对比段落数量差异"""
        para_counts = {}
        for lang, content in contents.items():
            # 用两个以上换行分割段落，并过滤空段落
            paragraphs = [p.strip() for p in re.split(r'\n{2,}', content) if p.strip()]
            para_counts[lang] = len(paragraphs)

        if len(set(para_counts.values())) > 1:
            self.report['paragraphs'].append(
                f"段落数量不一致: {rel_path}\n"
                f"ZH: {para_counts['zh']}, EN: {para_counts['en']}, JA: {para_counts['ja']}"
            )

    # ------------------- 报告生成逻辑 -------------------
    def _compare_images(self, contents, rel_path):
        img_counts = {}
        for lang, content in contents.items():
            sections = re.split(r'^#{2,6}\s+.*', content, flags=re.M)
            img_counts[lang] = [len(re.findall(r'!\[.*?\]\(.*?\)', sec)) for sec in sections]
        
        # 比较每个section的图片数量
        max_sections = max(len(img_counts[lang]) for lang in img_counts)
        for i in range(max_sections):
            counts = [img_counts[lang][i] if i < len(img_counts[lang]) else 0 
                    for lang in ['zh', 'en', 'ja']]
            if len(set(counts)) > 1:
                self.report['images'].append(
                    f"图片数量不一致: {rel_path} Section {i+1} "
                    f"(ZH: {counts[0]}, EN: {counts[1]}, JA: {counts[2]})"
                )

    # ------------------- 报告生成逻辑 -------------------
    def generate_report(self):
        """生成Markdown格式报告"""
        report_content = ["# 文档对比报告\n"]

        # 添加SUMMARY结构问题（带分隔线）
        if self.report.get('summary_structure'):
            report_content.append("## SUMMARY文件结构问题\n")
            
            # 插入英文检查结果
            en_items = [item for item in self.report['summary_structure'] 
                      if item.startswith('EN ') or 'ENGLISH CHECK' in item]
            report_content.extend(f"- {item}" for item in en_items)
            
            # 插入日文检查结果
            ja_items = [item for item in self.report['summary_structure'] 
                      if item.startswith('JA ')]
            if ja_items:
                report_content.append("\n--- 日文版检查结果 ---")  # 添加分隔线
                report_content.extend(f"- {item}" for item in ja_items)
            
            report_content.append("\n")
        
        # 目录结构问题
        if self.report['directory_structure']:
            report_content.append("## 目录结构问题\n")
            report_content.extend(f"- {item}" for item in self.report['directory_structure'])
            report_content.append("\n")

        # 标题格式问题
        if self.report['headings']:
            report_content.append("## 标题格式问题\n")
            report_content.extend(f"- {item}" for item in self.report['headings'])
            report_content.append("\n")

        # 段落数量问题
        if self.report['paragraphs']:
            report_content.append("## 段落数量问题\n")
            report_content.extend(f"- {item}" for item in self.report['paragraphs'])
            report_content.append("\n")

        # 图片差异问题
        if self.report['images']:
            report_content.append("## 图片差异问题\n")
            report_content.extend(f"- {item}" for item in self.report['images'])
            report_content.append("\n")

        # 写入文件（自动覆盖旧报告）
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_content))
        print(f"报告已生成：{self.report_file.absolute()}")

    # [原有代码：_compare_headings() 和 _compare_images() 需保留]
    # ...（保持原有标题和图片对比逻辑不变）...

if __name__ == "__main__":
    # 使用示例（路径需替换为实际路径）
    comparator = MDComparator(
        zh_path="../zh_CN",
        en_path="../en",
        ja_path="../jp"
    )
    comparator.compare_all()