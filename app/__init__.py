from flask import Flask
from markupsafe import Markup
from app.config import BASE_DIR
import markdown as md
import os


def create_app():
    app = Flask(__name__,
                static_folder=os.path.join(BASE_DIR, 'app', 'static'),
                template_folder=os.path.join(BASE_DIR, 'app', 'templates'))
    app.secret_key = 'interview-prep-dev-key'

    # Jinja2 filter: render markdown inline (backticks, bold, etc.)
    @app.template_filter('md')
    def markdown_filter(text):
        if not text:
            return ''
        html = md.markdown(text, extensions=['tables', 'fenced_code'])
        return Markup(html)

    # Jinja2 filter: render markdown but strip wrapping <p> for inline use
    @app.template_filter('md_inline')
    def markdown_inline_filter(text):
        if not text:
            return ''
        html = md.markdown(text, extensions=['fenced_code'])
        # Strip outer <p></p> wrapper for inline contexts
        html = html.strip()
        if html.startswith('<p>') and html.endswith('</p>'):
            html = html[3:-4]
        return Markup(html)

    @app.template_test('looks_like_code')
    def looks_like_code(text):
        """Test if answer text is actual code vs prose that mentions code."""
        if not text:
            return False
        if '```' in text:
            return True
        lines = text.strip().split('\n')
        # Real code: multiple lines starting with SQL keywords or has semicolons
        sql_line_starts = ['SELECT', 'FROM', 'WHERE', 'GROUP', 'ORDER', 'WITH', 'INSERT',
                           'UPDATE', 'DELETE', 'CREATE', 'JOIN', 'LEFT', 'INNER', 'HAVING']
        code_lines = sum(1 for l in lines if any(l.strip().upper().startswith(k) for k in sql_line_starts))
        if code_lines >= 2:
            return True
        # Python: lines starting with def/import/class/for/if or has consistent indentation
        py_starts = ['def ', 'import ', 'class ', 'for ', 'if ', 'return ', 'from ']
        py_lines = sum(1 for l in lines if any(l.strip().startswith(k) for k in py_starts))
        if py_lines >= 2:
            return True
        # Single-line answers that look like just a statement aren't code
        if len(lines) <= 2 and len(text) < 200:
            return False
        return text.strip().endswith(';')

    from app.routes.main import main_bp
    from app.routes.study import study_bp
    from app.routes.quiz import quiz_bp
    from app.routes.progress import progress_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(admin_bp)

    return app
