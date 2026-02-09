import json
import os
from app.config import DATA_MODULES_DIR
from app.models.module import Module

_cache = {}


def save_module(module: Module):
    os.makedirs(DATA_MODULES_DIR, exist_ok=True)
    path = os.path.join(DATA_MODULES_DIR, f'{module.id}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(module.to_dict(), f, indent=2, ensure_ascii=False)
    _cache[module.id] = module


def load_module(module_id: str) -> Module:
    if module_id in _cache:
        return _cache[module_id]
    path = os.path.join(DATA_MODULES_DIR, f'{module_id}.json')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    module = Module.from_dict(data)
    _cache[module_id] = module
    return module


def list_modules() -> list:
    os.makedirs(DATA_MODULES_DIR, exist_ok=True)
    modules = []
    for fname in sorted(os.listdir(DATA_MODULES_DIR)):
        if fname.endswith('.json'):
            module_id = fname.replace('.json', '')
            m = load_module(module_id)
            if m:
                modules.append(m)
    return modules


def clear_cache():
    _cache.clear()
