#!/usr/bin/env python3
"""English documentation format linter for Dify docs.

Checks a list of .mdx or .md files against the deterministic rules in
writing-guides/formatting-guide.md. Prints a grouped report to stdout.

Usage:
    python3 check-format-en.py <file> [<file> ...]
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


# ---------- shared regexes ----------

FENCE_RE = re.compile(r'^(\s*)(`{3,}|~{3,})(.*)$')
HEADING_RE = re.compile(r'^(#{1,6})(\s+)(.+?)\s*$')
FM_RE = re.compile(r'\A---\n(.*?)\n---\n', re.DOTALL)
FM_FIELD_RE = re.compile(r'^([A-Za-z][\w-]*)\s*:\s*(.*?)\s*$')


# ---------- frontmatter ----------

def _yaml_needs_quotes(value: str) -> bool:
    """Match the documented rule: quote only when the value contains a colon
    followed by a space. Other YAML edge cases (leading special chars,
    reserved words, numeric-looking values) are not flagged because the
    formatting guide intentionally restricts the rule to the `: ` case."""
    return ': ' in value


def _unquote(v: str) -> tuple[str, str]:
    """Return (stripped_value, quote_char_or_empty)."""
    v = v.rstrip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1], '"'
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        return v[1:-1], "'"
    return v, ''


def check_frontmatter(text: str, lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    m = FM_RE.match(text)
    if not m:
        if text.lstrip().startswith('---'):
            vs.append(Violation(1, 'F-title-missing',
                                'Malformed frontmatter block.'))
        return vs

    has_title = False
    fm_body = m.group(1)
    for offset, line in enumerate(fm_body.split('\n')):
        line_num = 2 + offset  # frontmatter begins at line 2 content
        fm = FM_FIELD_RE.match(line)
        if not fm:
            continue
        field, raw = fm.group(1), fm.group(2)
        if field == 'title':
            has_title = True
        if field == 'description':
            stripped, _ = _unquote(raw)
            if stripped.rstrip().endswith('.'):
                vs.append(Violation(line_num, 'F-desc-trailing-period',
                                    f'description ends with a period: {raw!r}'))
        if field in ('title', 'description', 'sidebarTitle'):
            stripped, q = _unquote(raw)
            needs = _yaml_needs_quotes(stripped)
            if needs and not q:
                vs.append(Violation(line_num, 'F-quote-needed',
                                    f'{field!r} value contains a colon+space; '
                                    f'wrap in double quotes.'))
            elif q == "'":
                vs.append(Violation(line_num, 'F-single-quote',
                                    f'{field!r} uses single quotes; use '
                                    'double quotes.'))
            elif q == '"' and not needs:
                vs.append(Violation(line_num, 'F-quote-unnecessary',
                                    f'{field!r} is quoted unnecessarily; '
                                    'quote only when value contains `: `.'))

    if not has_title:
        vs.append(Violation(1, 'F-title-missing',
                            'Frontmatter missing required `title` field.'))

    fm_end_line = text[:m.end()].count('\n')
    # line after closing `---` should be blank
    if fm_end_line < len(lines):
        after = lines[fm_end_line]
        if after.strip() != '':
            vs.append(Violation(fm_end_line + 1, 'F-blank-after-fm',
                                'No blank line after frontmatter.'))

    return vs


# ---------- headings ----------

# Verbs where the -ing form is almost always a true verb and should be base form.
ING_VERBS = {
    'Accessing': 'Access', 'Adding': 'Add', 'Adjusting': 'Adjust',
    'Building': 'Build', 'Calling': 'Call', 'Choosing': 'Choose',
    'Completing': 'Complete', 'Configuring': 'Configure',
    'Connecting': 'Connect', 'Creating': 'Create', 'Customizing': 'Customize',
    'Debugging': 'Debug', 'Defining': 'Define', 'Deleting': 'Delete',
    'Developing': 'Develop', 'Editing': 'Edit', 'Embedding': 'Embed',
    'Enabling': 'Enable', 'Exporting': 'Export', 'Filling': 'Fill',
    'Finding': 'Find', 'Generating': 'Generate', 'Getting': 'Get',
    'Handling': 'Handle', 'Importing': 'Import', 'Improving': 'Improve',
    'Initializing': 'Initialize', 'Installing': 'Install',
    'Integrating': 'Integrate', 'Introducing': 'Introduce',
    'Invoking': 'Invoke', 'Managing': 'Manage', 'Modifying': 'Modify',
    'Obtaining': 'Obtain', 'Packaging': 'Package', 'Passing': 'Pass',
    'Placing': 'Place', 'Preparing': 'Prepare', 'Publishing': 'Publish',
    'Resetting': 'Reset', 'Retrieving': 'Retrieve', 'Running': 'Run',
    'Saving': 'Save', 'Setting': 'Set', 'Sharing': 'Share', 'Signing': 'Sign',
    'Storing': 'Store', 'Syncing': 'Sync', 'Synchronizing': 'Synchronize',
    'Using': 'Use', 'Viewing': 'View',
}

# Heading texts that are legitimate section concepts (gerund-as-noun) and must
# not be flagged. Compared after stripping surrounding ** and numeric prefixes.
SKIP_ING_HEADINGS = {
    'Troubleshooting', 'Getting Started',
    'Logging', 'Indexing', 'Testing', 'Tracing', 'Billing',
    'Filtering', 'Sorting',
    'Chunking and Cleaning',
    'Mounting & Volumes', 'Breaking Changes',
    'Streaming Output', 'Streaming Behavior',
    'Processing Mode', 'Processing Considerations',
    'Branching Logic',
    'Publishing Methods', 'Publishing Options',
    'Publishing Best Practices', 'Publishing Recommendations',
    'Monitoring Data List',
    'Branding and Appearance',
    'Embedding Model',
    'TextEmbedding Implementation',
    'During Pull Request (PR) Review',
    'Packaging and Deployment',
}

HEADING_PREFIX_RE = re.compile(r'^\s*(?:\d+[\.\)]\s*|\([a-z\d]+\)\s*)')


def _strip_bold(t: str) -> str:
    t = t.strip()
    while t.startswith('**') and t.endswith('**') and len(t) > 4:
        t = t[2:-2].strip()
    return t


def check_headings(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    prev_heading_depth = 0
    heading_lines: list[int] = []

    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        hm = HEADING_RE.match(line)
        if not hm:
            continue
        hashes, _, title = hm.group(1), hm.group(2), hm.group(3)
        depth = len(hashes)

        # trailing #
        if title.rstrip().endswith('#'):
            vs.append(Violation(i, 'H-trailing-hash',
                                'Heading has a trailing `#`.'))

        # level skip (only flag forward jumps by >1, not regressions)
        if prev_heading_depth and depth > prev_heading_depth + 1:
            vs.append(Violation(i, 'H-skip-level',
                                f'Heading jumped from H{prev_heading_depth} '
                                f'to H{depth}; no intermediate level.'))
        prev_heading_depth = depth
        heading_lines.append(i)

        # blank line before / after (unless adjacent to file boundary or
        # frontmatter)
        if i > 2 and lines[i - 2].strip() != '':
            # allow heading immediately after frontmatter close
            vs.append(Violation(i, 'H-blank-before',
                                'Missing blank line before heading.'))
        if i < len(lines) and lines[i].strip() != '':
            vs.append(Violation(i, 'H-blank-after',
                                'Missing blank line after heading.'))

        # -ing verb detection
        core = _strip_bold(title)
        core2 = HEADING_PREFIX_RE.sub('', core)
        if core2 not in SKIP_ING_HEADINGS and core not in SKIP_ING_HEADINGS:
            m2 = re.match(r'([A-Za-z][\w]*)', core2)
            if m2:
                first = m2.group(1)
                if first in ING_VERBS:
                    vs.append(Violation(
                        i, 'H-ing-verb',
                        f'Heading starts with "{first}"; use base form '
                        f'"{ING_VERBS[first]}".'))
    return vs


# ---------- bold / italic ----------

INLINE_CODE_RE = re.compile(r'`[^`\n]*`')


def _strip_inline_code(line: str) -> str:
    return INLINE_CODE_RE.sub('', line)


def check_bold_italic(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    bold_colon_re = re.compile(r'\*\*[^*\n]+?[:\uFF1A]\*\*')
    # underscore italic: _X_ where underscores are not inside words
    ital_re = re.compile(r'(?:(?<=^)|(?<=\s)|(?<=[\(\[\{\"\']))_[^_\n]+?_'
                         r'(?=$|[\s\.,;:!?\)\]\}\"\'])')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_inline_code(line)
        if bold_colon_re.search(s):
            # need bold-pair awareness to avoid false positives (like
            # "**A** text:**B**"): a real match means colon sits inside a
            # properly paired bold span.
            parts = s.split('**')
            if len(parts) >= 3 and len(parts) % 2 == 1:
                for idx in range(1, len(parts) - 1, 2):
                    seg = parts[idx]
                    if seg and seg[-1] in (':', '\uFF1A'):
                        vs.append(Violation(
                            i, 'B-trailing-colon-inside',
                            f'Colon inside bold: "**{seg}**" — move colon '
                            'outside the asterisks.'))
        for m in ital_re.finditer(s):
            vs.append(Violation(
                i, 'B-underscore-italic',
                f'Italic with underscores: {m.group(0)!r}. Use `*text*`.'))
    return vs


# ---------- lists ----------

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
            vs.append(Violation(
                i, 'L-asterisk-bullet',
                'List uses `* ` bullet; use `- ` instead.'))
        # nested list indentation: any leading whitespace must be multiple of 2
        m = re.match(r'^( +)[-*]\s', line)
        if m:
            indent = len(m.group(1))
            if indent % 2 != 0:
                vs.append(Violation(
                    i, 'L-nested-indent',
                    f'Nested list item indented with {indent} spaces; '
                    'use multiples of 2.'))
    # blank lines around list blocks
    list_re = re.compile(r'^\s*[-*]\s|^\s*\d+\.\s')
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        is_list = list_re.match(line) is not None
        prev_is_list = i > 1 and list_re.match(lines[i - 2]) is not None
        prev_is_blank = i > 1 and lines[i - 2].strip() == ''
        if is_list and not prev_is_list and not prev_is_blank and i > 1:
            # first item of a list
            # only flag if previous line is non-heading content
            prev = lines[i - 2]
            if not HEADING_RE.match(prev) and prev.strip() != '':
                vs.append(Violation(
                    i, 'L-blank-before',
                    'Missing blank line before list.'))
        if (is_list and not prev_is_list
                and i < len(lines)
                and i + 1 <= len(lines)):
            # check that the item after the final list item has a blank
            pass  # handled implicitly by pair-wise scan below
    # after-list blank check
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
        if prev_list and not is_list and line.strip() != '':
            # transitioning out of a list block without a blank line
            vs.append(Violation(
                i, 'L-blank-after',
                'Missing blank line after list block.'))
        prev_list = is_list
    return vs


# ---------- code blocks ----------

def check_code_blocks(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    fence_start_line = 0
    for i, line in enumerate(lines, 1):
        m = FENCE_RE.match(line)
        if not m:
            continue
        if not in_fence:
            in_fence = True
            fence_start_line = i
            lang = m.group(3).strip()
            if not lang:
                vs.append(Violation(
                    i, 'C-no-language',
                    'Code block has no language tag.'))
            # blank line before fenced block
            if i > 1 and lines[i - 2].strip() != '':
                # allow start of file or after frontmatter
                vs.append(Violation(
                    i, 'C-blank-before',
                    'Missing blank line before code block.'))
        else:
            in_fence = False
            # blank line after
            if i < len(lines) and lines[i].strip() != '':
                vs.append(Violation(
                    i, 'C-blank-after',
                    'Missing blank line after code block.'))
    return vs


# ---------- links ----------

def check_links(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    link_re = re.compile(r'\[([^\]\n]+)\]\(([^)\n]+)\)')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in link_re.finditer(_strip_inline_code(line)):
            text, url = m.group(1), m.group(2)
            t = text.strip().lower().rstrip('.')
            if t in ('click here', 'here'):
                vs.append(Violation(
                    i, 'Li-click-here',
                    f'Non-descriptive link text: {text!r}.'))
            if url.startswith('http://'):
                vs.append(Violation(
                    i, 'Li-http-external',
                    f'External link uses http://: {url!r}.'))
            if url.startswith('/') and not url.startswith('/en/') \
                    and not url.startswith('/images/') \
                    and not url.startswith('/api-reference/') \
                    and not url.startswith('/#'):
                # only flag clearly internal-looking paths
                if re.match(r'^/[a-z]+/', url):
                    vs.append(Violation(
                        i, 'Li-internal-no-prefix',
                        f'Internal link does not start with /en/: {url!r}.'))
    return vs


# ---------- images ----------

def check_images(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False

    raw_img_re = re.compile(r'<img\b', re.IGNORECASE)
    md_img_re = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    frame_re = re.compile(r'<Frame\b([^>]*)>')
    caption_re = re.compile(r'caption=\"([^\"]*)\"')

    # collect frame captions to match with alt text on following lines
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if raw_img_re.search(line):
            vs.append(Violation(
                i, 'I-raw-img-tag',
                'Raw <img> tag; use <Frame> with markdown image instead.'))

    # Frame/caption pairing: for each <Frame caption="..."> block, find the
    # enclosed markdown image's alt on a subsequent line before </Frame>.
    i = 0
    while i < len(lines):
        line = lines[i]
        fm = frame_re.search(line)
        if fm:
            attrs = fm.group(1) or ''
            cap_m = caption_re.search(attrs)
            caption = cap_m.group(1) if cap_m else None
            # scan forward for </Frame>, collect first markdown image
            alts: list[tuple[int, str, str]] = []  # (line, alt, url)
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
                        f'Frame caption "{caption}" does not match alt '
                        f'text "{alt}".'))
            i = j + 1
        else:
            i += 1

    # Alt text size / default-name / filename checks on any markdown image
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
                vs.append(Violation(
                    i, 'I-alt-too-long',
                    f'Alt text is {len(alt)} chars; keep under 125.'))
            if not alt.strip():
                vs.append(Violation(
                    i, 'I-alt-empty',
                    'Image has empty alt text; confirm the image is '
                    'purely decorative.'))
            # filename checks (only on local paths under /images/)
            if url.startswith('/images/'):
                fname = url.rsplit('/', 1)[-1]
                stem, _, ext = fname.rpartition('.')
                if ext and ext != ext.lower():
                    vs.append(Violation(
                        i, 'I-filename-uppercase-ext',
                        f'Image extension is uppercase: {fname!r}.'))
                if re.search(r'@\d+x', fname):
                    vs.append(Violation(
                        i, 'I-filename-retina-suffix',
                        f'Image filename has retina suffix: {fname!r}.'))
                if re.match(r'^(CleanShot|Screenshot|IMG_|image\d)', fname,
                            re.IGNORECASE):
                    vs.append(Violation(
                        i, 'I-filename-default-tool',
                        f'Image filename looks like a default tool output: '
                        f'{fname!r}.'))
                if re.search(r'[_\s]', stem) or re.search(r'[A-Z]', stem):
                    vs.append(Violation(
                        i, 'I-filename-non-kebab',
                        f'Image filename is not kebab-case/lowercase: '
                        f'{fname!r}.'))
                if not re.match(r'^[\x00-\x7f]+$', fname):
                    vs.append(Violation(
                        i, 'I-filename-non-kebab',
                        f'Image filename contains non-ASCII characters: '
                        f'{fname!r}.'))
                m3 = re.match(r'([A-Za-z]+)', stem)
                if m3:
                    first_word = m3.group(1).lower().capitalize()
                    if first_word in ING_VERBS:
                        vs.append(Violation(
                            i, 'I-filename-ing-verb',
                            f'Image filename starts with -ing verb '
                            f'{first_word!r}; use base form.'))
    return vs


# ---------- Mintlify components ----------

def check_mintlify_components(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    callout_re = re.compile(r'^\s*<(Info|Tip|Note|Warning)\b[^>]*>', re.IGNORECASE)
    tab_no_title_re = re.compile(r'<Tab(?:\s+[^>]*)?>')
    tab_title_attr_re = re.compile(r'\btitle\s*=\s*"[^"]*"')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if callout_re.match(line):
            if i > 1 and lines[i - 2].strip() != '':
                vs.append(Violation(
                    i, 'M-component-blank-before',
                    'Missing blank line before Mintlify callout.'))
        for m in tab_no_title_re.finditer(line):
            if not tab_title_attr_re.search(m.group(0)):
                vs.append(Violation(
                    i, 'M-tab-no-title',
                    '<Tab> element without a title attribute.'))
    # end-of-component blank
    closer_re = re.compile(r'^\s*</(Info|Tip|Note|Warning)>\s*$',
                           re.IGNORECASE)
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if closer_re.match(line):
            if i < len(lines) and lines[i].strip() != '':
                vs.append(Violation(
                    i, 'M-component-blank-after',
                    'Missing blank line after Mintlify callout.'))
    return vs


# ---------- UI elements ----------

def check_ui_elements(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    arrow_re = re.compile(r'\*\*[^*\n]+?\*\*\s*(?:→|->|=>)\s*\*\*[^*\n]+?\*\*')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if arrow_re.search(line):
            vs.append(Violation(
                i, 'U-menu-arrow',
                'Menu path uses `→`, `->`, or `=>`; use `>` instead.'))
    return vs


# ---------- spacing ----------

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
                vs.append(Violation(
                    i, 'S-double-blank',
                    'Two or more consecutive blank lines.'))
        else:
            blank_run = 0
        if line != line.rstrip():
            vs.append(Violation(
                i, 'S-trailing-whitespace',
                'Line has trailing whitespace.'))
    return vs


# ---------- punctuation ----------

def check_punctuation(lines: list[str]) -> list[Violation]:
    vs: list[Violation] = []
    in_fence = False
    em_dash_spaces = re.compile(r'\s—\s|\s—|—\s')
    en_dash_spaces = re.compile(r'\d\s+–\s+\d|\d\s+–\d|\d–\s+\d')
    fw_punct = re.compile(r'[A-Za-z][，。；：！？（）、]|[，。；：！？（）、][A-Za-z]')
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = _strip_inline_code(line)
        if em_dash_spaces.search(s):
            vs.append(Violation(
                i, 'P-em-dash-spaces',
                'Em dash has surrounding whitespace; write `word—word`.'))
        if en_dash_spaces.search(s):
            vs.append(Violation(
                i, 'P-en-dash-spaces',
                'En dash in numeric range has surrounding whitespace; '
                'write `2–4`.'))
        if fw_punct.search(s):
            vs.append(Violation(
                i, 'P-fullwidth-in-english',
                'Full-width punctuation adjacent to Latin letters in English '
                'content.'))
    return vs


# ---------- runner ----------

ALL_CHECKS = [
    ('frontmatter', check_frontmatter),
    ('headings', check_headings),
    ('bold_italic', check_bold_italic),
    ('lists', check_lists),
    ('code', check_code_blocks),
    ('links', check_links),
    ('images', check_images),
    ('mintlify', check_mintlify_components),
    ('ui', check_ui_elements),
    ('spacing', check_spacing),
    ('punctuation', check_punctuation),
]


def lint_file(path: Path) -> dict[str, list[Violation]]:
    text = path.read_text()
    lines = text.split('\n')
    results: dict[str, list[Violation]] = {}
    for name, fn in ALL_CHECKS:
        # frontmatter needs text for regex; others only need lines
        if name == 'frontmatter':
            results[name] = fn(text, lines)
        else:
            results[name] = fn(lines)
    return results


def print_report(path: Path, results: dict[str, list[Violation]]):
    total = sum(len(v) for v in results.values())
    print(f'\n### {path}')
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
        print('usage: check-format-en.py <file> [<file> ...]', file=sys.stderr)
        return 2
    total = 0
    for arg in argv:
        p = Path(arg)
        if not p.exists():
            print(f'skip (missing): {p}', file=sys.stderr)
            continue
        # only process .mdx/.md under en/
        if not (str(p).startswith('en/') or '/en/' in str(p.as_posix())):
            print(f'skip (non-en): {p}', file=sys.stderr)
            continue
        results = lint_file(p)
        print_report(p, results)
        total += sum(len(v) for v in results.values())
    print(f'\nTotal violations: {total}')
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
