"""
Parser for unstructured markdown content (e.g. pasted from Claude.ai).

Strategy:
1. Try splitting on headers (H1/H2/H3)
2. Fall back to --- horizontal rules
3. Fall back to paragraph chunking (~500 words)

Auto-tag chunks by keyword detection.
"""

import re
from app.models.module import Module, Section, ContentBlock


SQL_KEYWORDS = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'GROUP BY', 'HAVING', 'ORDER BY',
                'INSERT', 'UPDATE', 'DELETE', 'CREATE TABLE', 'ALTER', 'INDEX',
                'UNION', 'CTE', 'WITH', 'WINDOW', 'PARTITION BY', 'subquery']

PYTHON_KEYWORDS = ['pandas', 'numpy', 'def ', 'class ', 'import ', 'lambda',
                   'list comprehension', 'dict', 'tuple', 'generator',
                   'decorator', '.apply(', '.groupby(', '.merge(', 'DataFrame']

STATS_KEYWORDS = ['probability', 'p-value', 'hypothesis', 'confidence interval',
                  'standard deviation', 'variance', 'bayes', 'regression',
                  'normal distribution', 'CLT', 'central limit', 'sampling',
                  'type I', 'type II', 'significance', 'A/B test']

ML_KEYWORDS = ['model', 'training', 'overfitting', 'underfitting', 'bias-variance',
               'random forest', 'gradient boosting', 'XGBoost', 'neural network',
               'regularization', 'L1', 'L2', 'cross-validation', 'feature',
               'precision', 'recall', 'F1', 'AUC', 'ROC', 'classification',
               'clustering', 'deep learning', 'logistic regression']


def parse_master_doc(content: str, module_id: str = None, title: str = 'Imported Content') -> Module:
    """Parse unstructured markdown into a Module."""
    if module_id is None:
        module_id = 'imported-' + re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    sections = []

    # Strategy 1: Split on headers
    header_chunks = re.split(r'\n(#{1,3}\s+.+)', content)
    if len(header_chunks) > 2:
        sections = _parse_header_chunks(header_chunks)
    else:
        # Strategy 2: Split on horizontal rules
        hr_chunks = re.split(r'\n---+\n', content)
        if len(hr_chunks) > 1:
            sections = _parse_plain_chunks(hr_chunks)
        else:
            # Strategy 3: Paragraph chunking
            sections = _chunk_by_paragraphs(content)

    for i, section in enumerate(sections):
        section.order = i

    return Module(
        id=module_id,
        title=title,
        number=0,
        subtitle='Imported content',
        sections=sections,
    )


def _parse_header_chunks(chunks: list) -> list:
    sections = []
    i = 0
    while i < len(chunks):
        chunk = chunks[i].strip()
        if chunk.startswith('#'):
            title = re.sub(r'^#+\s*', '', chunk)
            body = chunks[i + 1] if i + 1 < len(chunks) else ''
            category = auto_tag(title + ' ' + body)
            blocks = _text_to_blocks(body)
            sections.append(Section(title=title, category=category, blocks=blocks))
            i += 2
        else:
            if chunk:
                category = auto_tag(chunk)
                blocks = _text_to_blocks(chunk)
                sections.append(Section(title='Introduction', category=category, blocks=blocks))
            i += 1
    return sections


def _parse_plain_chunks(chunks: list) -> list:
    sections = []
    for i, chunk in enumerate(chunks):
        chunk = chunk.strip()
        if not chunk:
            continue
        # Use first line as title
        lines = chunk.split('\n', 1)
        title = lines[0].strip().strip('#').strip('*').strip()[:80]
        category = auto_tag(chunk)
        blocks = _text_to_blocks(chunk)
        sections.append(Section(title=title, category=category, blocks=blocks))
    return sections


def _chunk_by_paragraphs(content: str, target_words: int = 500) -> list:
    paragraphs = re.split(r'\n\n+', content)
    sections = []
    current_lines = []
    current_words = 0

    for para in paragraphs:
        words = len(para.split())
        if current_words + words > target_words and current_lines:
            text = '\n\n'.join(current_lines)
            title = current_lines[0][:80].strip('# *')
            category = auto_tag(text)
            blocks = _text_to_blocks(text)
            sections.append(Section(title=title, category=category, blocks=blocks))
            current_lines = []
            current_words = 0
        current_lines.append(para)
        current_words += words

    if current_lines:
        text = '\n\n'.join(current_lines)
        title = current_lines[0][:80].strip('# *')
        category = auto_tag(text)
        blocks = _text_to_blocks(text)
        sections.append(Section(title=title, category=category, blocks=blocks))

    return sections


def _text_to_blocks(text: str) -> list:
    """Split text into ContentBlock objects, separating code blocks."""
    blocks = []
    parts = re.split(r'(```\w*\n.*?```)', text, flags=re.DOTALL)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        code_match = re.match(r'```(\w*)\n(.*?)```', part, re.DOTALL)
        if code_match:
            lang = code_match.group(1) or None
            blocks.append(ContentBlock(type='code', content=code_match.group(2).strip(), language=lang))
        else:
            blocks.append(ContentBlock(type='text', content=part))
    return blocks


def auto_tag(text: str) -> str:
    """Auto-detect category from text content."""
    text_upper = text.upper()
    text_lower = text.lower()

    scores = {
        'sql': sum(1 for kw in SQL_KEYWORDS if kw.upper() in text_upper),
        'python': sum(1 for kw in PYTHON_KEYWORDS if kw.lower() in text_lower),
        'stats': sum(1 for kw in STATS_KEYWORDS if kw.lower() in text_lower),
        'ml': sum(1 for kw in ML_KEYWORDS if kw.lower() in text_lower),
    }

    best = max(scores, key=scores.get)
    if scores[best] > 0:
        return best
    return 'general'
