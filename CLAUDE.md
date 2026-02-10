# DS Interview Prep

Flask-based study tool for data science interview preparation. Modules parsed from markdown, stored as JSON, served with Jinja2 templates and HTMX for dynamic updates.

## Tech Stack

- Flask + Jinja2 + HTMX
- highlight.js for syntax highlighting
- JSON file storage (no database)
- gunicorn for production
- Render free tier (auto-deploys on push to main)

## Architecture

- `app/` - Flask app with factory pattern (`create_app()`)
- `app/routes/` - Blueprints: main, study, quiz, progress, admin, practice
- `app/storage/` - JSON persistence with in-memory caching
- `app/models/` - Dataclasses for Module, Question, Progress
- `app/parser/` - Markdown to structured data (module_parser, master_doc_parser, question_extractor)
- `data/modules/` - Parsed module JSON
- `data/questions/` - Extracted questions JSON per module
- `data/challenges/` - Standalone practice challenges (hand-authored JSON)
- `modules/` - Source markdown files

## Key Patterns

- SM2 spaced repetition with intervals [1, 3, 7, 14, 30]
- Question types: code_practice, flashcard, free_text, fill_blank, multiple_choice, star_practice
- Categories: sql, python, stats, ml, terminology, behavioral, product
- Challenges store both PostgreSQL-style answers (for display) and SQLite-compatible answers (for the interpreter)

## Permissions

- Git commit and push to main: yes
- Running dev server (`python3 run.py`): yes
- Running ingest scripts: yes
- pip installs: yes
- File reads: yes
