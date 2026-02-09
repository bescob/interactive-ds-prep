"""
State-machine parser for structured interview prep markdown modules.

Handles patterns:
- H1 title with module number
- H2 sections with emoji category prefixes
- Quick Quiz / Answer pairs
- Code blocks (fenced)
- Self-Test sections with numbered Q&A
- Module 14 round-based format
- Tables, lists, regular text
"""

import re
import os
from app.models.module import Module, Section, ContentBlock
from app.config import CATEGORY_EMOJI


def parse_module_file(filepath: str) -> Module:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    filename = os.path.basename(filepath)
    # Extract module number from filename like Module-01-Warm-Up.md
    num_match = re.search(r'Module-(\d+)', filename)
    module_num = int(num_match.group(1)) if num_match else 0
    module_id = f'module-{module_num:02d}'

    title = ''
    subtitle = ''
    sections = []
    current_section = None
    current_text_lines = []
    in_code_block = False
    code_lines = []
    code_lang = None

    def flush_text():
        nonlocal current_text_lines
        text = '\n'.join(current_text_lines).strip()
        if text and current_section:
            current_section.blocks.append(ContentBlock(type='text', content=text))
        current_text_lines = []

    def flush_section():
        nonlocal current_section
        flush_text()
        if current_section:
            sections.append(current_section)
        current_section = None

    for line in lines:
        raw = line.rstrip('\n')

        # Handle code blocks
        if raw.lstrip().startswith('```'):
            if in_code_block:
                # End code block
                code_content = '\n'.join(code_lines)
                if current_section:
                    flush_text()
                    current_section.blocks.append(
                        ContentBlock(type='code', content=code_content, language=code_lang)
                    )
                code_lines = []
                code_lang = None
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
                lang_match = re.match(r'```(\w+)', raw.lstrip())
                code_lang = lang_match.group(1) if lang_match else None
            continue

        if in_code_block:
            code_lines.append(raw)
            continue

        # H1 title
        if raw.startswith('# ') and not raw.startswith('## '):
            # e.g. "# Module 01 — Warm Up"
            title_match = re.match(r'#\s+Module\s+\d+\s*[—–-]\s*(.*)', raw)
            if title_match:
                title = title_match.group(1).strip()
            else:
                title = raw[2:].strip()
            continue

        # Subtitle (italicized topics line)
        if raw.startswith('*') and raw.endswith('*') and 'Topics:' in raw:
            subtitle = raw.strip('* ')
            continue

        # Horizontal rule - section separator
        if raw.strip() == '---':
            continue

        # H2 section header
        if raw.startswith('## '):
            flush_section()
            section_title = raw[3:].strip()
            category = detect_category(section_title)
            current_section = Section(
                title=section_title,
                category=category,
                order=len(sections),
            )
            continue

        # H3 subsection - treat as bold text within current section
        if raw.startswith('### '):
            if current_section:
                flush_text()
                current_text_lines.append(f'**{raw[4:].strip()}**')
            continue

        # Regular content line
        if current_section is not None:
            current_text_lines.append(raw)

    # Flush remaining
    flush_section()

    return Module(
        id=module_id,
        title=title,
        number=module_num,
        subtitle=subtitle,
        sections=sections,
        source_file=filename,
    )


def detect_category(title: str) -> str:
    """Detect category from emoji prefix or keywords in section title."""
    for emoji, cat in CATEGORY_EMOJI.items():
        if emoji in title:
            return cat

    title_lower = title.lower()

    # Module 14 round-based detection
    if 'speed definition' in title_lower:
        return 'terminology'
    if 'sql' in title_lower:
        return 'sql'
    if 'stats' in title_lower or 'probability' in title_lower:
        return 'stats'
    if 'ml' in title_lower or 'machine learning' in title_lower:
        return 'ml'
    if 'python' in title_lower or 'pandas' in title_lower:
        return 'python'
    if 'product' in title_lower:
        return 'product'
    if 'behavioral' in title_lower:
        return 'behavioral'
    if 'self-test' in title_lower or 'self test' in title_lower:
        return 'review'
    if 'round' in title_lower:
        return 'mixed'
    if 'checklist' in title_lower or 'final' in title_lower:
        return 'review'
    if 'chicago' in title_lower or 'company' in title_lower:
        return 'product'
    if 'repeat' in title_lower:
        # "Repeat: L1 vs L2" etc
        if 'l1' in title_lower or 'l2' in title_lower:
            return 'ml'
        if 'standard error' in title_lower or 'se ' in title_lower:
            return 'stats'
        return 'review'

    return 'general'
