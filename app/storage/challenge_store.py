import json
import os
from app.config import DATA_CHALLENGES_DIR

_cache = {}


def load_challenge(challenge_id):
    if challenge_id in _cache:
        return _cache[challenge_id]
    path = os.path.join(DATA_CHALLENGES_DIR, f'{challenge_id}.json')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    _cache[challenge_id] = data
    return data


def load_all_challenges():
    os.makedirs(DATA_CHALLENGES_DIR, exist_ok=True)
    challenges = []
    for fname in sorted(os.listdir(DATA_CHALLENGES_DIR)):
        if fname.endswith('.json'):
            challenge_id = fname.replace('.json', '')
            c = load_challenge(challenge_id)
            if c:
                challenges.append(c)
    return challenges


def clear_cache():
    _cache.clear()
