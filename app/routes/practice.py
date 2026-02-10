from flask import Blueprint, render_template, request, jsonify
from app.storage.question_store import load_all_questions
from app.storage.challenge_store import load_all_challenges, load_challenge
from app.sql_runner import execute_and_compare

practice_bp = Blueprint('practice', __name__, url_prefix='/practice')


@practice_bp.route('/')
def browse():
    category = request.args.get('category', '')
    q_type = request.args.get('type', '')
    source = request.args.get('source', '')
    search = request.args.get('search', '').strip().lower()

    # load module questions
    module_questions = []
    if source != 'challenges':
        for q in load_all_questions():
            module_questions.append({
                'id': q.id,
                'title': q.prompt[:120],
                'prompt': q.prompt,
                'answer': q.answer,
                'category': q.category,
                'question_type': q.question_type,
                'source': 'module',
                'module_id': q.module_id,
                'section_title': q.section_title,
                'code_language': q.code_language,
                'rubric': q.rubric,
                'is_challenge': False,
            })

    # load standalone challenges
    challenges = []
    if source != 'modules':
        for c in load_all_challenges():
            challenges.append({
                'id': c['id'],
                'title': c['title'],
                'prompt': c['prompt'],
                'answer': c['answer'],
                'category': c.get('category', ''),
                'question_type': 'sql_challenge',
                'source': 'challenge',
                'difficulty': c.get('difficulty', ''),
                'scenario': c.get('scenario', ''),
                'sql_setup': c.get('sql_setup', ''),
                'sql_answer': c.get('sql_answer', ''),
                'expected_columns': c.get('expected_columns', []),
                'expected_rows': c.get('expected_rows', []),
                'concepts': c.get('concepts', []),
                'rubric': c.get('rubric', []),
                'is_challenge': True,
            })

    items = module_questions + challenges

    # filters
    if category:
        items = [i for i in items if i['category'] == category]
    if q_type:
        if q_type == 'sql_challenge':
            items = [i for i in items if i['is_challenge']]
        else:
            items = [i for i in items if i['question_type'] == q_type]
    if search:
        items = [i for i in items if search in i['prompt'].lower() or search in i['title'].lower()]

    # collect filter options
    all_items = module_questions + challenges
    categories = sorted(set(i['category'] for i in all_items if i['category']))
    types = sorted(set(i['question_type'] for i in all_items))

    return render_template('practice/browse.html',
                           items=items,
                           categories=categories,
                           types=types,
                           selected_category=category,
                           selected_type=q_type,
                           selected_source=source,
                           search_query=request.args.get('search', ''))


@practice_bp.route('/sql-run', methods=['POST'])
def sql_run():
    data = request.get_json()
    challenge_id = data.get('challenge_id', '')
    user_sql = data.get('sql', '')

    challenge = load_challenge(challenge_id)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404

    setup_sql = challenge.get('sql_setup', '')
    reference_sql = challenge.get('sql_answer', '')
    expected_rows = challenge.get('expected_rows')
    expected_columns = challenge.get('expected_columns')

    result = execute_and_compare(
        setup_sql=setup_sql,
        user_sql=user_sql,
        reference_sql=reference_sql,
        expected_rows=expected_rows,
        expected_columns=expected_columns,
    )

    return jsonify(result)
