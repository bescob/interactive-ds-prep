#!/usr/bin/env python3
"""Parse all markdown modules into JSON data files."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import MODULES_DIR
from app.parser.module_parser import parse_module_file
from app.parser.question_extractor import extract_questions
from app.storage.module_store import save_module
from app.storage.question_store import save_questions

import glob


def main():
    md_files = sorted(glob.glob(os.path.join(MODULES_DIR, '*.md')))
    if not md_files:
        print(f'No markdown files found in {MODULES_DIR}')
        sys.exit(1)

    total_sections = 0
    total_questions = 0

    for filepath in md_files:
        filename = os.path.basename(filepath)
        print(f'\nParsing {filename}...')

        module = parse_module_file(filepath)
        save_module(module)

        questions = extract_questions(module)
        save_questions(module.id, questions)

        n_sections = len(module.sections)
        n_questions = len(questions)
        total_sections += n_sections
        total_questions += n_questions

        print(f'  Module {module.number:02d}: "{module.title}"')
        print(f'  Sections: {n_sections}')
        print(f'  Questions extracted: {n_questions}')

        # Show question type breakdown
        type_counts = {}
        for q in questions:
            type_counts[q.question_type] = type_counts.get(q.question_type, 0) + 1
        if type_counts:
            types_str = ', '.join(f'{t}: {c}' for t, c in sorted(type_counts.items()))
            print(f'  Types: {types_str}')

    print(f'\n{"="*50}')
    print(f'Total: {len(md_files)} modules, {total_sections} sections, {total_questions} questions')
    print('Done!')


if __name__ == '__main__':
    main()
