import markdown
from flask import Blueprint, render_template, abort
from app.storage.module_store import load_module
from app.storage.question_store import load_questions
from app.storage.progress_store import get_progress, flush

study_bp = Blueprint('study', __name__)


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

    # Convert text blocks to HTML via markdown
    rendered_blocks = []
    for block in section.blocks:
        if block.type == 'text':
            html = markdown.markdown(block.content, extensions=['tables', 'fenced_code'])
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
