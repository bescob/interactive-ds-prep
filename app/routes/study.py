import re
import markdown
from flask import Blueprint, render_template, abort
from app.storage.module_store import load_module
from app.storage.question_store import load_questions
from app.storage.progress_store import get_progress, flush

study_bp = Blueprint('study', __name__)


def _strip_quick_quiz(text):
    """Remove Quick Quiz + Answer pairs from text content.
    These get extracted into interactive Practice Questions instead."""
    return re.sub(
        r'\n*\*\*Quick quiz[^*]*\*\*.*$',
        '', text, flags=re.DOTALL | re.IGNORECASE
    ).strip()


def _strip_self_test_answers(text):
    """Remove answer block from self-test content.
    Answers are available via the interactive Practice Questions below."""
    return re.sub(
        r'\n*\*\*Answers?:?\*\*.*$',
        '', text, flags=re.DOTALL | re.IGNORECASE
    ).strip()


@study_bp.route('/module/<module_id>')
def module_overview(module_id):
    module = load_module(module_id)
    if not module:
        abort(404)
    questions = load_questions(module_id)
    progress = get_progress()
    mp = progress.get_module_progress(module_id)
    mp.total_sections = len(module.sections)
    return render_template('study/overview.html',
                           module=module,
                           questions=questions,
                           progress=mp,
                           user_progress=progress)


@study_bp.route('/module/<module_id>/section/<int:section_idx>')
def section_view(module_id, section_idx):
    module = load_module(module_id)
    if not module or section_idx >= len(module.sections):
        abort(404)

    section = module.sections[section_idx]
    questions = [q for q in load_questions(module_id) if q.section_title == section.title]

    # Mark section as viewed
    progress = get_progress()
    mp = progress.get_module_progress(module_id)
    mp.total_sections = len(module.sections)
    if section_idx not in mp.sections_viewed:
        mp.sections_viewed.append(section_idx)
    if mp.status == 'not_started':
        mp.status = 'in_progress'
    if len(mp.sections_viewed) >= len(module.sections):
        mp.status = 'completed'
    progress.update_streak()
    flush()

    is_self_test = 'self-test' in section.title.lower() or 'self test' in section.title.lower()

    # Convert text blocks to HTML, stripping quiz content that's already
    # shown as interactive Practice Questions below
    rendered_blocks = []
    skip_next_code = False

    for i, block in enumerate(section.blocks):
        if skip_next_code and block.type == 'code':
            skip_next_code = False
            continue
        skip_next_code = False

        if block.type == 'text':
            text = block.content
            if is_self_test:
                text = _strip_self_test_answers(text)
            else:
                cleaned = _strip_quick_quiz(text)
                # If quiz ended with bare "**Answer:**", the answer code is in the next block
                if cleaned != text and re.search(r'\*\*Answer:?\*\*\s*$', text):
                    skip_next_code = True
                text = cleaned

            if text:
                html = markdown.markdown(text, extensions=['tables', 'fenced_code'])
                rendered_blocks.append({'type': 'html', 'content': html})
        elif block.type == 'code':
            rendered_blocks.append({'type': 'code', 'content': block.content, 'language': block.language or ''})

    prev_idx = section_idx - 1 if section_idx > 0 else None
    next_idx = section_idx + 1 if section_idx < len(module.sections) - 1 else None

    return render_template('study/section.html',
                           module=module,
                           section=section,
                           section_idx=section_idx,
                           blocks=rendered_blocks,
                           questions=questions,
                           prev_idx=prev_idx,
                           next_idx=next_idx)


@study_bp.route('/module/<module_id>/flashcards')
def flashcards(module_id):
    module = load_module(module_id)
    if not module:
        abort(404)
    questions = load_questions(module_id)
    # Pre-render markdown for front/back so JS can use innerHTML
    cards = [{'id': q.id,
              'front': markdown.markdown(q.prompt, extensions=['fenced_code']),
              'back': markdown.markdown(q.answer, extensions=['fenced_code']),
              'category': q.category, 'type': q.question_type} for q in questions]
    return render_template('study/flashcard.html',
                           module=module,
                           cards=cards)
