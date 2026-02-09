import json
import os
from app.config import DATA_QUESTIONS_DIR
from app.models.question import Question

_cache = {}


def save_questions(module_id: str, questions: list):
    os.makedirs(DATA_QUESTIONS_DIR, exist_ok=True)
    path = os.path.join(DATA_QUESTIONS_DIR, f'{module_id}.json')
    data = [q.to_dict() for q in questions]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    _cache[module_id] = questions


def load_questions(module_id: str) -> list:
    if module_id in _cache:
        return _cache[module_id]
    path = os.path.join(DATA_QUESTIONS_DIR, f'{module_id}.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    questions = [Question.from_dict(d) for d in data]
    _cache[module_id] = questions
    return questions


def load_all_questions() -> list:
    os.makedirs(DATA_QUESTIONS_DIR, exist_ok=True)
    all_q = []
    for fname in sorted(os.listdir(DATA_QUESTIONS_DIR)):
        if fname.endswith('.json'):
            module_id = fname.replace('.json', '')
            all_q.extend(load_questions(module_id))
    return all_q


def add_question(question: Question):
    questions = load_questions(question.module_id)
    questions.append(question)
    save_questions(question.module_id, questions)


def update_question(question: Question):
    questions = load_questions(question.module_id)
    for i, q in enumerate(questions):
        if q.id == question.id:
            questions[i] = question
            break
    save_questions(question.module_id, questions)


def delete_question(module_id: str, question_id: str):
    questions = load_questions(module_id)
    questions = [q for q in questions if q.id != question_id]
    save_questions(module_id, questions)
    _cache[module_id] = questions


def clear_cache():
    _cache.clear()
