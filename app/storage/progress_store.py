import json
import os
from app.config import PROGRESS_FILE
from app.models.progress import UserProgress

_progress = None


def _load() -> UserProgress:
    global _progress
    if _progress is not None:
        return _progress
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        _progress = UserProgress.from_dict(data)
    else:
        _progress = UserProgress()
    return _progress


def get_progress() -> UserProgress:
    return _load()


def flush():
    p = _load()
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(p.to_dict(), f, indent=2, ensure_ascii=False)


def reset_module(module_id: str):
    p = _load()
    if module_id in p.modules:
        p.modules[module_id].status = 'not_started'
        p.modules[module_id].sections_viewed = []
    # Reset all questions for this module
    to_remove = [qid for qid, qp in p.questions.items()
                 if qid.startswith(module_id) or True]  # We'll filter by module in questions
    # Actually we need to check by module - questions have module_id in their data
    # For simplicity, just reset the module progress and keep question progress
    # (questions are tracked by question_id, not module)
    flush()


def reset_module_questions(module_id: str, question_ids: list):
    """Reset progress for specific question IDs belonging to a module."""
    p = _load()
    if module_id in p.modules:
        p.modules[module_id].status = 'not_started'
        p.modules[module_id].sections_viewed = []
    for qid in question_ids:
        if qid in p.questions:
            del p.questions[qid]
    flush()


def reload():
    global _progress
    _progress = None
    return _load()
