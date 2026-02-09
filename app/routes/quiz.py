import random
from flask import Blueprint, render_template, request, jsonify, abort
from app.storage.module_store import load_module
from app.storage.question_store import load_questions, load_all_questions
from app.storage.progress_store import get_progress, flush

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route('/module/<module_id>/quiz')
def quiz_config(module_id):
    module = load_module(module_id)
    if not module:
        abort(404)
    questions = load_questions(module_id)
    categories = sorted(set(q.category for q in questions))
    types = sorted(set(q.question_type for q in questions))
    return render_template('quiz/shell.html',
                           module=module,
                           categories=categories,
                           types=types,
                           total_questions=len(questions))


@quiz_bp.route('/quiz/next', methods=['POST'])
def quiz_next():
    module_id = request.form.get('module_id', '')
    categories = request.form.getlist('categories')
    types = request.form.getlist('types')
    count = int(request.form.get('count', 10))
    current_idx = int(request.form.get('current_idx', 0))
    question_ids = request.form.get('question_ids', '')

    if not question_ids:
        # First call: select questions
        questions = load_questions(module_id) if module_id else load_all_questions()
        if categories:
            questions = [q for q in questions if q.category in categories]
        if types:
            questions = [q for q in questions if q.question_type in types]
        random.shuffle(questions)
        questions = questions[:count]
        question_ids = ','.join(q.id for q in questions)
        current_idx = 0
    else:
        questions = _resolve_question_ids(question_ids, module_id)

    if current_idx >= len(questions):
        # Quiz complete
        progress = get_progress()
        return render_template('quiz/complete.html',
                               total=len(questions),
                               progress=progress)

    question = questions[current_idx]
    template = f'quiz/partials/{question.question_type}.html'
    return render_template(template,
                           question=question,
                           current_idx=current_idx,
                           total=len(questions),
                           question_ids=question_ids,
                           module_id=module_id,
                           categories=','.join(categories) if categories else '',
                           types=','.join(types) if types else '')


@quiz_bp.route('/quiz/submit', methods=['POST'])
def quiz_submit():
    question_id = request.form.get('question_id', '')
    module_id = request.form.get('module_id', '')
    question_ids = request.form.get('question_ids', '')
    current_idx = int(request.form.get('current_idx', 0))
    user_answer = request.form.get('user_answer', '')

    questions = _resolve_question_ids(question_ids, module_id)
    if current_idx >= len(questions):
        abort(400)

    question = questions[current_idx]

    return render_template('quiz/result.html',
                           question=question,
                           user_answer=user_answer,
                           current_idx=current_idx,
                           total=len(questions),
                           question_ids=question_ids,
                           module_id=module_id)


@quiz_bp.route('/quiz/grade', methods=['POST'])
def quiz_grade():
    question_id = request.form.get('question_id', '')
    grade = request.form.get('grade', '')  # correct, partial, incorrect
    module_id = request.form.get('module_id', '')
    question_ids = request.form.get('question_ids', '')
    current_idx = int(request.form.get('current_idx', 0))
    categories = request.form.get('categories', '')
    types = request.form.get('types', '')

    # Update progress
    progress = get_progress()
    qp = progress.get_question_progress(question_id)
    qp.record_attempt(grade)
    progress.update_streak()
    flush()

    # Serve next question
    next_idx = current_idx + 1
    questions = _resolve_question_ids(question_ids, module_id)

    if next_idx >= len(questions):
        return render_template('quiz/complete.html',
                               total=len(questions),
                               progress=progress)

    question = questions[next_idx]
    template = f'quiz/partials/{question.question_type}.html'
    return render_template(template,
                           question=question,
                           current_idx=next_idx,
                           total=len(questions),
                           question_ids=question_ids,
                           module_id=module_id,
                           categories=categories,
                           types=types)


@quiz_bp.route('/review')
def review():
    """Spaced repetition review session."""
    progress = get_progress()
    due_ids = progress.due_for_review()

    if not due_ids:
        return render_template('quiz/no_review.html')

    # Resolve questions
    all_questions = load_all_questions()
    q_map = {q.id: q for q in all_questions}
    due_questions = [q_map[qid] for qid in due_ids if qid in q_map]

    if not due_questions:
        return render_template('quiz/no_review.html')

    random.shuffle(due_questions)
    question_ids = ','.join(q.id for q in due_questions)

    question = due_questions[0]
    template = f'quiz/partials/{question.question_type}.html'
    return render_template('quiz/shell.html',
                           module=None,
                           review_mode=True,
                           first_question_html=render_template(
                               template,
                               question=question,
                               current_idx=0,
                               total=len(due_questions),
                               question_ids=question_ids,
                               module_id='',
                           ),
                           total_questions=len(due_questions))


@quiz_bp.route('/random')
def random_quiz():
    """Quick-fire random questions across all modules."""
    all_questions = load_all_questions()
    if not all_questions:
        abort(404)
    random.shuffle(all_questions)
    questions = all_questions[:10]
    question_ids = ','.join(q.id for q in questions)

    question = questions[0]
    template = f'quiz/partials/{question.question_type}.html'
    return render_template('quiz/shell.html',
                           module=None,
                           random_mode=True,
                           categories=[],
                           types=[],
                           total_questions=len(questions),
                           first_question_html=render_template(
                               template,
                               question=question,
                               current_idx=0,
                               total=len(questions),
                               question_ids=question_ids,
                               module_id='',
                           ))


def _resolve_question_ids(question_ids_str: str, module_id: str) -> list:
    """Resolve comma-separated question IDs to Question objects."""
    if not question_ids_str:
        return []
    ids = question_ids_str.split(',')
    all_questions = load_questions(module_id) if module_id else load_all_questions()
    q_map = {q.id: q for q in all_questions}
    return [q_map[qid] for qid in ids if qid in q_map]
