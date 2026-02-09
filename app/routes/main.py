from flask import Blueprint, render_template
from app.storage.module_store import list_modules
from app.storage.question_store import load_questions
from app.storage.progress_store import get_progress

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    modules = list_modules()
    progress = get_progress()
    due_ids = progress.due_for_review()

    module_data = []
    for m in modules:
        mp = progress.get_module_progress(m.id)
        mp.total_sections = len(m.sections)
        questions = load_questions(m.id)
        q_attempted = sum(1 for q in questions if progress.get_question_progress(q.id, create=False).attempts > 0)
        q_total = len(questions)

        # Collect categories present in this module
        categories = list(set(s.category for s in m.sections if s.category not in ('review', 'general', 'mixed')))

        module_data.append({
            'module': m,
            'progress': mp,
            'questions_attempted': q_attempted,
            'questions_total': q_total,
            'categories': categories,
        })

    return render_template('dashboard.html',
                           modules=module_data,
                           progress=progress,
                           due_count=len(due_ids))
