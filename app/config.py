import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES_DIR = os.path.join(BASE_DIR, 'modules')
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_MODULES_DIR = os.path.join(DATA_DIR, 'modules')
DATA_QUESTIONS_DIR = os.path.join(DATA_DIR, 'questions')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')

CATEGORY_COLORS = {
    'sql': '#3B82F6',
    'python': '#F59E0B',
    'stats': '#10B981',
    'ml': '#F97316',
    'product': '#F97316',
    'behavioral': '#F97316',
    'terminology': '#8B5CF6',
}

CATEGORY_EMOJI = {
    '🔷': 'sql',
    '🔶': 'python',
    '🟢': 'stats',
    '🟠': 'ml',
    '🟣': 'terminology',
}

SM2_INTERVALS = [1, 3, 7, 14, 30]
