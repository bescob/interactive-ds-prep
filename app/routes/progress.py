from flask import Blueprint, request, jsonify, redirect, url_for
from app.storage.progress_store import get_progress, flush, reset_module_questions
from app.storage.question_store import load_questions

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/api/progress/<module_id>/reset', methods=['POST'])
def reset_module(module_id):
    questions = load_questions(module_id)
    question_ids = [q.id for q in questions]
    reset_module_questions(module_id, question_ids)
    return redirect(request.referrer or url_for('main.dashboard'))


@progress_bp.route('/api/progress/stats')
def progress_stats():
    p = get_progress()
    return jsonify({
        'daily_streak': p.daily_streak,
        'total_attempted': p.total_attempted,
        'total_correct': p.total_correct,
        'due_for_review': len(p.due_for_review()),
    })
