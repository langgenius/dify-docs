#!/usr/bin/env python3
"""CJK (Chinese + Japanese) documentation format linter for Dify docs.

Checks a list of .mdx or .md files under zh/ or ja/ against the deterministic
rules in writing-guides/formatting-guide.md,
tools/translate/formatting-zh.md, and tools/translate/formatting-ja.md.
Prints a grouped report to stdout.

Usage:
    python3 check-format-cjk.py <file> [<file> ...]
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


# ---------- data types ----------

@dataclass
class Violation:
    line: int
    rule: str
    message: str


# ---------- constants ----------

FENCE_RE = re.compile(r'^(\s*)(`{3,}|~{3,})(.*)$')
HEADING_RE = re.compile(r'^(#{1,6})(\s+)(.+?)\s*$')
FM_RE = re.compile(r'\A---\n(.*?)\n---\n', re.DOTALL)
FM_FIELD_RE = re.compile(r'^([A-Za-z][\w-]*)\s*:\s*(.*?)\s*$')
INLINE_CODE_RE = re.compile(r'`[^`\n]*`')
URL_RE = re.compile(r'https?://[^\s)（）<>]+')
LINK_RE = re.compile(r'\[([^\]\n]+)\]\(([^)\n]+)\)')

# CJK: CJK Unified Ideographs + hiragana/katakana + extensions
CJK = r'[\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]'
CJK_RE = re.compile(CJK)
LATIN_ALNUM = r'[A-Za-z0-9]'

CJK_PUNCT = '，。、；：！？（）「」『』【】〈〉《》・…'

# Japanese heuristic char ranges
HIRAGANA = r'[\u3040-\u309F]'
KATAKANA = r'[\u30A0-\u30FF]'
JA_ONLY = r'[\u3040-\u30FF]'


# ---------- shared helpers ----------

def _strip_inline_code(line: str) -> str:
    return INLINE_CODE_RE.sub('', line)


def _strip_code_and_urls(line: str) -> str:
    s = INLINE_CODE_RE.sub('', line)
    # collapse markdown link syntax [text](url) -> text so the bracket and
    # paren characters don't count as prose punctuation
    s = re.sub(r'\[([^\]\n]+)\]\([^)\n]+\)', r'\1', s)
    s = URL_RE.sub('', s)
    return s


def _yaml_needs_quotes(value: str) -> bool:
    """Match the documented rule: quote only when the value contains a colon
    followed by a space. Other YAML edge cases are intentionally not flagged
    because the formatting guide restricts the rule to the `: ` case."""
    return ': ' in value


def _unquote(v: str) -> tuple[str, str]:
    v = v.rstrip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1], '"'
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        return v[1:-1], "'"
    return v, ''


def detect_lang(path: Path) -> str:
    s = path.as_posix()
    if s.startswith('zh/') or '/zh/' in s:
        return 'zh'
    if s.startswith('ja/') or '/ja/' in s:
        return 'ja'
    return 'unknown'


# ---------- shared structural checks ----------

def check_frontmatter(text: str, lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    m = FM_RE.match(text)
    if not m:
        return vs
    has_title = False
    for offset, line in enumerate(m.group(1).split('\n')):
        line_num = 2 + offset
        fm = FM_FIELD_RE.match(line)
        if not fm:
            continue
        field, raw = fm.group(1), fm.group(2)
        if field == 'title':
            has_title = True
        if field == 'description':
            stripped, _ = _unquote(raw)
            if stripped.rstrip().endswith('.') or stripped.rstrip().endswith('。'):
                vs.append(Violation(line_num, 'F-desc-trailing-period',
                                    f'description ends with a period: {raw!r}'))
        if field in ('title', 'description', 'sidebarTitle'):
            stripped, q = _unquote(raw)
            needs = _yaml_needs_quotes(stripped)
            if needs and not q:
                vs.append(Violation(line_num, 'F-quote-needed',
                                    f'{field!r} needs double quotes.'))
            elif q == "'":
                vs.append(Violation(line_num, 'F-single-quote',
                                    f'{field!r} uses single quotes; use double.'))
            elif q == '"' and not needs:
                vs.append(Violation(line_num, 'F-quote-unnecessary',
                                    f'{field!r} is quoted unnecessarily.'))
    if not has_title:
        vs.append(Violation(1, 'F-title-missing',
                            'Frontmatter missing required `title`.'))
    fm_end_line = text[:m.end()].count('\n')
    if fm_end_line < len(lines):
        after = lines[fm_end_line]
        if after.strip() != '':
            vs.append(Violation(fm_end_line + 1, 'F-blank-after-fm',
                                'No blank line after frontmatter.'))
    return vs


def check_headings(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    prev_depth = 0
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        hm = HEADING_RE.match(line)
        if not hm:
            continue
        depth = len(hm.group(1))
        title = hm.group(3)
        if title.rstrip().endswith('#'):
            vs.append(Violation(i, 'H-trailing-hash',
                                'Heading has a trailing `#`.'))
        if prev_depth and depth > prev_depth + 1:
            vs.append(Violation(i, 'H-skip-level',
                                f'Heading jumped H{prev_depth} -> H{depth}.'))
        prev_depth = depth
        if i > 2 and lines[i - 2].strip() != '':
            vs.append(Violation(i, 'H-blank-before',
                                'Missing blank line before heading.'))
        if i < len(lines) and lines[i].strip() != '':
            vs.append(Violation(i, 'H-blank-after',
                                'Missing blank line after heading.'))
        # heading ending punctuation in CJK context
        last = title.rstrip().rstrip('#').rstrip()
        if last and last[-1] in '。，、；：':
            vs.append(Violation(
                i, 'H-heading-end-punct',
                f'Heading ends with punctuation {last[-1]!r}; drop it.'))
    return vs


def check_bold_italic(lines: list[str], lang: str) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    bold_colon_re = re.compile(r'\*\*[^*\n]+?[:\uFF1A]\*\*')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_inline_code(line)
        if bold_colon_re.search(s):
            parts = s.split('**')
            if len(parts) >= 3 and len(parts) % 2 == 1:
                for idx in range(1, len(parts) - 1, 2):
                    seg = parts[idx]
                    if seg and seg[-1] in (':', '\uFF1A'):
                        vs.append(Violation(
                            i, 'B-trailing-colon-inside',
                            f'Colon inside bold: "**{seg}**"'))
        # CJK italic detection: *text* where text contains CJK, not in code
        # Skip lines where the line is predominantly code markers.
        ital_re = re.compile(
            r'(?<!\*)\*([^*\n]+?)\*(?!\*)')
        for m in ital_re.finditer(s):
            seg = m.group(1)
            if CJK_RE.search(seg):
                vs.append(Violation(
                    i, 'CJK-italic',
                    f'Italic used on CJK text: *{seg}*. Use bold instead.'))
    return vs


def check_lists(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r'^(\s*)\*\s', line):
            vs.append(Violation(i, 'L-asterisk-bullet',
                                'List uses `* ` bullet; use `- `.'))
        m = re.match(r'^( +)[-*]\s', line)
        if m:
            indent = len(m.group(1))
            if indent % 2 != 0:
                vs.append(Violation(
                    i, 'L-nested-indent',
                    f'Nested list indented with {indent} spaces.'))
    list_re = re.compile(r'^\s*[-*]\s|^\s*\d+\.\s')
    in_fence = False
    prev_list = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            prev_list = False
            continue
        if in_fence:
            continue
        is_list = list_re.match(line) is not None
        if is_list and not prev_list and i > 1:
            prev_line = lines[i - 2]
            if not HEADING_RE.match(prev_line) and prev_line.strip() != '':
                vs.append(Violation(i, 'L-blank-before',
                                    'Missing blank line before list.'))
        if prev_list and not is_list and line.strip() != '':
            vs.append(Violation(i, 'L-blank-after',
                                'Missing blank line after list.'))
        prev_list = is_list
    return vs


def check_code_blocks(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        m = FENCE_RE.match(line)
        if not m:
            continue
        if not in_fence:
            in_fence = True
            lang_tag = m.group(3).strip()
            if not lang_tag:
                vs.append(Violation(i, 'C-no-language',
                                    'Code block has no language tag.'))
            if i > 1 and lines[i - 2].strip() != '':
                vs.append(Violation(i, 'C-blank-before',
                                    'Missing blank line before code block.'))
        else:
            in_fence = False
            if i < len(lines) and lines[i].strip() != '':
                vs.append(Violation(i, 'C-blank-after',
                                    'Missing blank line after code block.'))
    return vs


DISCLAIMER_MARKERS = ('本文档由 AI 自动翻译',
                      'このドキュメントは AI によって自動翻訳')


def check_links(lines: list[str], lang: str) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    click_here = ('click here', 'here', '点击这里', '点击此处', 'こちら',
                  'ここ', 'クリック')
    wrong_prefix = '/en/'
    target_prefix = f'/{lang}/'
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # Skip cross-lang link checks inside the translation disclaimer —
        # the disclaimer intentionally links to the English source.
        is_disclaimer_line = any(m in line for m in DISCLAIMER_MARKERS)
        s = _strip_inline_code(line)
        for m in LINK_RE.finditer(s):
            text, url = m.group(1), m.group(2)
            t = text.strip().lower().rstrip('.。')
            if t in click_here:
                vs.append(Violation(i, 'Li-click-here',
                                    f'Non-descriptive link text: {text!r}.'))
            if url.startswith('http://'):
                vs.append(Violation(i, 'Li-http-external',
                                    f'External http:// link: {url!r}.'))
            if url.startswith(wrong_prefix) and not is_disclaimer_line:
                vs.append(Violation(
                    i, 'CJK-cross-lang-link',
                    f'Internal link starts with {wrong_prefix!r} in {lang}/ '
                    f'file; use {target_prefix!r}.'))
    return vs


def check_images(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    raw_img_re = re.compile(r'<img\b', re.IGNORECASE)
    md_img_re = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    frame_re = re.compile(r'<Frame\b([^>]*)>')
    caption_re = re.compile(r'caption=\"([^\"]*)\"')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if raw_img_re.search(line):
            vs.append(Violation(
                i, 'I-raw-img-tag',
                'Raw <img> tag; use <Frame> with markdown image.'))
    # frame/caption pairing
    i = 0
    while i < len(lines):
        line = lines[i]
        fm = frame_re.search(line)
        if fm:
            cap_m = caption_re.search(fm.group(1) or '')
            caption = cap_m.group(1) if cap_m else None
            alts: list[tuple[int, str, str]] = []
            j = i + 1
            while j < len(lines) and '</Frame>' not in lines[j]:
                for mm in md_img_re.finditer(lines[j]):
                    alts.append((j + 1, mm.group(1), mm.group(2)))
                j += 1
            if caption is not None and alts:
                alt_line, alt, _ = alts[0]
                if alt != caption:
                    vs.append(Violation(
                        alt_line, 'I-caption-alt-mismatch',
                        f'Frame caption "{caption}" != alt "{alt}".'))
            i = j + 1
        else:
            i += 1
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for mm in md_img_re.finditer(line):
            alt, url = mm.group(1), mm.group(2)
            if len(alt) > 125:
                vs.append(Violation(i, 'I-alt-too-long',
                                    f'Alt text {len(alt)} chars; <125.'))
            if url.startswith('/images/'):
                fname = url.rsplit('/', 1)[-1]
                stem, _, ext = fname.rpartition('.')
                if ext and ext != ext.lower():
                    vs.append(Violation(i, 'I-filename-uppercase-ext',
                                        f'Uppercase ext: {fname!r}.'))
                if re.search(r'@\d+x', fname):
                    vs.append(Violation(i, 'I-filename-retina-suffix',
                                        f'Retina suffix: {fname!r}.'))
                if re.match(r'^(CleanShot|Screenshot|IMG_|image\d)', fname,
                            re.IGNORECASE):
                    vs.append(Violation(i, 'I-filename-default-tool',
                                        f'Default tool name: {fname!r}.'))
                if re.search(r'[_\s]', stem) or re.search(r'[A-Z]', stem):
                    vs.append(Violation(i, 'I-filename-non-kebab',
                                        f'Not kebab-case: {fname!r}.'))
    return vs


def check_mintlify(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    callout_re = re.compile(r'^\s*<(Info|Tip|Note|Warning)\b[^>]*>',
                            re.IGNORECASE)
    closer_re = re.compile(r'^\s*</(Info|Tip|Note|Warning)>\s*$',
                           re.IGNORECASE)
    tab_re = re.compile(r'<Tab(?:\s+[^>]*)?>')
    tab_title_re = re.compile(r'\btitle\s*=\s*"[^"]*"')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if callout_re.match(line) and i > 1 and lines[i - 2].strip() != '':
            vs.append(Violation(i, 'M-component-blank-before',
                                'Missing blank line before callout.'))
        if closer_re.match(line) and i < len(lines) \
                and lines[i].strip() != '':
            vs.append(Violation(i, 'M-component-blank-after',
                                'Missing blank line after callout.'))
        for m in tab_re.finditer(line):
            if not tab_title_re.search(m.group(0)):
                vs.append(Violation(i, 'M-tab-no-title',
                                    '<Tab> without title attribute.'))
    return vs


def check_spacing(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    blank_run = 0
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            blank_run = 0
            continue
        if in_fence:
            continue
        if line.strip() == '':
            blank_run += 1
            if blank_run == 2:
                vs.append(Violation(i, 'S-double-blank',
                                    'Consecutive blank lines.'))
        else:
            blank_run = 0
        if line != line.rstrip():
            vs.append(Violation(i, 'S-trailing-whitespace',
                                'Line has trailing whitespace.'))
    return vs


def check_dashes(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    em_space = re.compile(r'\s—\s|\s—|—\s')
    en_space = re.compile(r'\d\s+–\s+\d|\d\s+–\d|\d–\s+\d')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_inline_code(line)
        if em_space.search(s):
            vs.append(Violation(i, 'P-em-dash-spaces',
                                'Em dash has surrounding spaces.'))
        if en_space.search(s):
            vs.append(Violation(i, 'P-en-dash-spaces',
                                'En dash in range has surrounding spaces.'))
    return vs


# ---------- CJK-shared rules ----------

def check_cjk_latin_spacing(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    # CJK followed immediately by Latin alphanumeric or leading `
    # (excluding punctuation-adjacent cases)
    pat_cjk_latin = re.compile(rf'{CJK}[A-Za-z0-9`]')
    pat_latin_cjk = re.compile(rf'[A-Za-z0-9`]{CJK}')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_code_and_urls(line)
        if pat_cjk_latin.search(s) or pat_latin_cjk.search(s):
            vs.append(Violation(
                i, 'CJK-latin-spacing',
                'CJK character adjacent to Latin/digit/backtick without '
                'space.'))
    return vs


def check_cjk_halfwidth_punct(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    # half-width , . : ; ? ! ( ) adjacent to CJK
    pat = re.compile(rf'{CJK}[,\.:;?!()]|[,\.:;?!()]{CJK}')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_code_and_urls(line)
        if pat.search(s):
            vs.append(Violation(
                i, 'CJK-halfwidth-punct',
                'Half-width punctuation adjacent to CJK character.'))
    return vs


def check_cjk_bold_spacing(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    # Bold adjacent to CJK without space: X**bold** or **bold**X where X is
    # CJK and no space between.
    pat_after = re.compile(rf'{CJK}\*\*[^*\n]+?\*\*')
    pat_before = re.compile(rf'\*\*[^*\n]+?\*\*{CJK}')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_inline_code(line)
        if pat_after.search(s) or pat_before.search(s):
            vs.append(Violation(
                i, 'CJK-bold-no-space',
                'Bold adjacent to CJK without space on that side.'))
    return vs


def check_cjk_link_spacing(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    # [text](url) adjacent to CJK without space
    pat_after = re.compile(rf'{CJK}\[[^\]\n]+?\]\([^)\n]+?\)')
    pat_before = re.compile(rf'\[[^\]\n]+?\]\([^)\n]+?\){CJK}')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_inline_code(line)
        if pat_after.search(s) or pat_before.search(s):
            vs.append(Violation(
                i, 'CJK-link-no-space',
                'Link text adjacent to CJK without space on that side.'))
    return vs


def check_cjk_em_dash(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    # em dash in text that is predominantly CJK (contains at least one CJK
    # char on the line outside code)
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_inline_code(line)
        if ('—' in s or '——' in s) and CJK_RE.search(s):
            vs.append(Violation(
                i, 'CJK-em-dash',
                'Em dash in CJK text; restructure without the dash.'))
    return vs


def check_cjk_disclaimer(lines: list[str], text: str, lang: str
                         ) -> list[Violation]:
    # Must appear directly below frontmatter. Permit a single blank line
    # between close of frontmatter and the disclaimer.
    vs: list[Violation] = []
    m = FM_RE.match(text)
    if not m:
        return vs
    fm_end_line = text[:m.end()].count('\n')
    # scan next ~10 lines for the disclaimer
    needle = '本文档由 AI 自动翻译' if lang == 'zh' \
        else 'このドキュメントは AI によって自動翻訳' if lang == 'ja' \
        else None
    if not needle:
        return vs
    window = '\n'.join(lines[fm_end_line:fm_end_line + 10])
    if needle not in window:
        vs.append(Violation(fm_end_line + 1, 'CJK-disclaimer-missing',
                            f'Translation disclaimer not found near top '
                            f'(expected text containing {needle!r}).'))
    return vs


# ---------- Chinese-only rules ----------

def check_zh_ascii_ellipsis(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    pat = re.compile(rf'(?:{CJK}|\s)\.{{3}}')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_code_and_urls(line)
        if '...' in s and CJK_RE.search(s):
            vs.append(Violation(
                i, 'ZH-ascii-ellipsis',
                '`...` used in Chinese text; use `……` instead.'))
    return vs


def check_zh_fullwidth_slash(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_code_and_urls(line)
        if '／' in s:
            vs.append(Violation(i, 'ZH-fullwidth-slash',
                                'Full-width slash `／`; use `/`.'))
    return vs


def check_zh_quotes(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    # mainland curly quotes or straight quotes around CJK content
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_code_and_urls(line)
        # Curly double quotes
        if re.search(rf'“[^”\n]*{CJK}[^”\n]*”', s):
            vs.append(Violation(
                i, 'ZH-quotes',
                'Mainland-style double quotes around CJK; use 「」.'))
        # Curly single quotes
        if re.search(rf'‘[^’\n]*{CJK}[^’\n]*’', s):
            vs.append(Violation(
                i, 'ZH-quotes',
                'Mainland-style single quotes around CJK; use 「」.'))
    return vs


def check_zh_range_hyphen(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    # digit-digit or digit–digit in Chinese context where ～ should be used
    pat = re.compile(r'\d+\s?[-–]\s?\d+')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_code_and_urls(line)
        if not CJK_RE.search(s):
            continue
        for m in pat.finditer(s):
            # look at surrounding 8 chars for CJK context
            start = max(0, m.start() - 8)
            end = min(len(s), m.end() + 8)
            ctx = s[start:end]
            if CJK_RE.search(ctx):
                vs.append(Violation(
                    i, 'ZH-range-hyphen',
                    f'Numeric range {m.group(0)!r} uses hyphen/en-dash; '
                    'use `～`.'))
                break  # one flag per line is enough
    return vs


def check_zh_percent_space(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    pat = re.compile(r'\d\s+[%°]')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_code_and_urls(line)
        if pat.search(s):
            vs.append(Violation(i, 'ZH-percent-space',
                                'Space before `%` or `°`.'))
    return vs


# ---------- Japanese-only rules ----------

FW_DIGIT_RE = re.compile(r'[\uFF10-\uFF19]')
FW_LATIN_RE = re.compile(r'[\uFF21-\uFF3A\uFF41-\uFF5A]')
FW_SPACE = '\u3000'
SENTENCE_END_RE = re.compile(r'[。！？]')


def check_ja_fullwidth_ascii(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_code_and_urls(line)
        if FW_DIGIT_RE.search(s):
            vs.append(Violation(i, 'JA-fullwidth-digit',
                                'Full-width digit used; use half-width.'))
        if FW_LATIN_RE.search(s):
            vs.append(Violation(i, 'JA-fullwidth-latin',
                                'Full-width Latin letter; use half-width.'))
        if FW_SPACE in s:
            vs.append(Violation(i, 'JA-fullwidth-space',
                                'Full-width space `　`; use half-width.'))
    return vs


def check_ja_sentence_length(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if HEADING_RE.match(line):
            continue
        s = _strip_code_and_urls(line).strip()
        if not CJK_RE.search(s):
            continue
        # split on Japanese sentence-ending punctuation, then count chars
        segments = SENTENCE_END_RE.split(s)
        for seg in segments:
            seg = seg.strip()
            if len(seg) > 80 and CJK_RE.search(seg):
                vs.append(Violation(
                    i, 'JA-sentence-too-long',
                    f'Sentence ~{len(seg)} characters; split sentences >80.'))
                break
    return vs


def check_ja_go_prefix(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    bad = ('ご確認', 'ご参照', 'ご入力')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_code_and_urls(line)
        for w in bad:
            if w in s:
                vs.append(Violation(
                    i, 'JA-go-prefix',
                    f'Overly formal honorific {w!r}; drop the ご prefix.'))
    return vs


def check_ja_heading_sentence(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        hm = HEADING_RE.match(line)
        if not hm:
            continue
        t = hm.group(3).rstrip(' #。！？').rstrip()
        if re.search(r'します$|します。$', t):
            vs.append(Violation(
                i, 'JA-heading-sentence-ending',
                'Japanese heading ends with "します"; prefer noun-phrase '
                'form (e.g., 〜の作成).'))
    return vs


def check_ja_style_mix(lines: list[str], text: str) -> list[Violation]:
    # Detect mix of です/ます and だ/である in body text outside code.
    vs: list[Violation] = []
    body_parts = []
    in_fence = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        body_parts.append(_strip_code_and_urls(line))
    body = '\n'.join(body_parts)
    polite = bool(re.search(r'です。|ます。|ですか。|ません。', body))
    plain = bool(re.search(r'だ。|である。|ではない。', body))
    if polite and plain:
        vs.append(Violation(
            1, 'JA-style-mix',
            'File mixes です/ます and だ/である forms; use one register.'))
    return vs


# ---------- runner ----------

def lint_file(path: Path) -> tuple[str, dict[str, list[Violation]]]:
    lang = detect_lang(path)
    text = path.read_text()
    lines = text.split('\n')
    results: dict[str, list[Violation]] = {}

    results['frontmatter'] = check_frontmatter(text, lines)
    results['headings'] = check_headings(lines)
    results['bold_italic'] = check_bold_italic(lines, lang)
    results['lists'] = check_lists(lines)
    results['code'] = check_code_blocks(lines)
    results['links'] = check_links(lines, lang)
    results['images'] = check_images(lines)
    results['mintlify'] = check_mintlify(lines)
    results['spacing'] = check_spacing(lines)
    results['dashes'] = check_dashes(lines)

    results['cjk_latin_spacing'] = check_cjk_latin_spacing(lines)
    results['cjk_halfwidth_punct'] = check_cjk_halfwidth_punct(lines)
    results['cjk_bold_spacing'] = check_cjk_bold_spacing(lines)
    results['cjk_link_spacing'] = check_cjk_link_spacing(lines)
    results['cjk_em_dash'] = check_cjk_em_dash(lines)
    results['cjk_disclaimer'] = check_cjk_disclaimer(lines, text, lang)

    if lang == 'zh':
        results['zh_ellipsis'] = check_zh_ascii_ellipsis(lines)
        results['zh_slash'] = check_zh_fullwidth_slash(lines)
        results['zh_quotes'] = check_zh_quotes(lines)
        results['zh_range'] = check_zh_range_hyphen(lines)
        results['zh_percent'] = check_zh_percent_space(lines)
    if lang == 'ja':
        results['ja_fullwidth_ascii'] = check_ja_fullwidth_ascii(lines)
        results['ja_sentence_length'] = check_ja_sentence_length(lines)
        results['ja_go_prefix'] = check_ja_go_prefix(lines)
        results['ja_heading_sentence'] = check_ja_heading_sentence(lines)
        results['ja_style_mix'] = check_ja_style_mix(lines, text)

    return lang, results


def print_report(path: Path, lang: str, results: dict[str, list[Violation]]):
    total = sum(len(v) for v in results.values())
    print(f'\n### {path} ({lang})')
    if total == 0:
        print('  ✅ no deterministic issues found')
        return
    by_line: list[Violation] = []
    for group in results.values():
        by_line.extend(group)
    by_line.sort(key=lambda v: (v.line, v.rule))
    for v in by_line:
        print(f'  {v.line:>5}  [{v.rule}]  {v.message}')


def main(argv: list[str]) -> int:
    if not argv:
        print('usage: check-format-cjk.py <file> [<file> ...]', file=sys.stderr)
        return 2
    total = 0
    for arg in argv:
        p = Path(arg)
        if not p.exists():
            print(f'skip (missing): {p}', file=sys.stderr)
            continue
        lang = detect_lang(p)
        if lang == 'unknown':
            print(f'skip (non-zh/ja): {p}', file=sys.stderr)
            continue
        lang, results = lint_file(p)
        print_report(p, lang, results)
        total += sum(len(v) for v in results.values())
    print(f'\nTotal violations: {total}')
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
