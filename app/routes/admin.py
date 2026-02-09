from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.storage.module_store import list_modules, save_module
from app.storage.question_store import (
    load_questions, load_all_questions, add_question, update_question, delete_question
)
from app.models.question import Question, QUESTION_TYPES
from app.parser.master_doc_parser import parse_master_doc
from app.parser.question_extractor import extract_questions
from app.storage.question_store import save_questions

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/ingest', methods=['GET', 'POST'])
def ingest():
    if request.method == 'POST':
        content = request.form.get('content', '')
        title = request.form.get('title', 'Imported Content')
        action = request.form.get('action', 'preview')

        if not content.strip():
            flash('No content provided', 'error')
            return redirect(url_for('admin.ingest'))

        module = parse_master_doc(content, title=title)
        questions = extract_questions(module)

        if action == 'save':
            save_module(module)
            save_questions(module.id, questions)
            flash(f'Saved module "{title}" with {len(module.sections)} sections and {len(questions)} questions', 'success')
            return redirect(url_for('main.dashboard'))

        return render_template('admin/ingest.html',
                               preview_module=module,
                               preview_questions=questions,
                               content=content,
                               title=title)

    return render_template('admin/ingest.html')


@admin_bp.route('/questions')
def questions_list():
    modules = list_modules()
    module_id = request.args.get('module', '')
    category = request.args.get('category', '')
    q_type = request.args.get('type', '')

    if module_id:
        questions = load_questions(module_id)
    else:
        questions = load_all_questions()

    if category:
        questions = [q for q in questions if q.category == category]
    if q_type:
        questions = [q for q in questions if q.question_type == q_type]

    categories = sorted(set(q.category for q in load_all_questions()))
    types = sorted(set(q.question_type for q in load_all_questions()))

    return render_template('admin/questions.html',
                           questions=questions,
                           modules=modules,
                           categories=categories,
                           types=types,
                           question_types=QUESTION_TYPES,
                           selected_module=module_id,
                           selected_category=category,
                           selected_type=q_type)


@admin_bp.route('/questions/add', methods=['POST'])
def question_add():
    q = Question.create(
        module_id=request.form.get('module_id', ''),
        section_title=request.form.get('section_title', 'Custom'),
        category=request.form.get('category', 'general'),
        question_type=request.form.get('question_type', 'free_text'),
        prompt=request.form.get('prompt', ''),
        answer=request.form.get('answer', ''),
        code_language=request.form.get('code_language', '') or None,
        options=[o.strip() for o in request.form.get('options', '').split('\n') if o.strip()],
        rubric=[r.strip() for r in request.form.get('rubric', '').split('\n') if r.strip()],
        source='manual',
    )
    add_question(q)
    flash(f'Question added: {q.prompt[:50]}...', 'success')
    return redirect(url_for('admin.questions_list', module=q.module_id))


@admin_bp.route('/questions/<module_id>/<question_id>/edit', methods=['POST'])
def question_edit(module_id, question_id):
    questions = load_questions(module_id)
    q = next((q for q in questions if q.id == question_id), None)
    if not q:
        flash('Question not found', 'error')
        return redirect(url_for('admin.questions_list'))

    q.prompt = request.form.get('prompt', q.prompt)
    q.answer = request.form.get('answer', q.answer)
    q.question_type = request.form.get('question_type', q.question_type)
    q.category = request.form.get('category', q.category)
    q.code_language = request.form.get('code_language', '') or None
    options_str = request.form.get('options', '')
    if options_str:
        q.options = [o.strip() for o in options_str.split('\n') if o.strip()]
    rubric_str = request.form.get('rubric', '')
    if rubric_str:
        q.rubric = [r.strip() for r in rubric_str.split('\n') if r.strip()]

    update_question(q)
    flash('Question updated', 'success')
    return redirect(url_for('admin.questions_list', module=module_id))


@admin_bp.route('/questions/<module_id>/<question_id>/delete', methods=['POST'])
def question_delete(module_id, question_id):
    delete_question(module_id, question_id)
    flash('Question deleted', 'success')
    return redirect(url_for('admin.questions_list', module=module_id))
