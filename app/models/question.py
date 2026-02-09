from dataclasses import dataclass, field
from typing import Optional
import uuid


QUESTION_TYPES = [
    'code_practice',
    'flashcard',
    'free_text',
    'fill_blank',
    'multiple_choice',
    'star_practice',
]


@dataclass
class Question:
    id: str
    module_id: str
    section_title: str
    category: str  # 'sql', 'python', 'stats', 'ml', 'terminology', 'behavioral'
    question_type: str  # one of QUESTION_TYPES
    prompt: str
    answer: str
    code_language: Optional[str] = None  # for code_practice
    options: list = field(default_factory=list)  # for multiple_choice
    blanks: list = field(default_factory=list)  # for fill_blank: list of correct answers
    rubric: list = field(default_factory=list)  # for star_practice / free_text: key points
    source: str = 'auto'  # 'auto' or 'manual'

    @classmethod
    def create(cls, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())[:8]
        return cls(**kwargs)

    def to_dict(self):
        d = {
            'id': self.id,
            'module_id': self.module_id,
            'section_title': self.section_title,
            'category': self.category,
            'question_type': self.question_type,
            'prompt': self.prompt,
            'answer': self.answer,
            'source': self.source,
        }
        if self.code_language:
            d['code_language'] = self.code_language
        if self.options:
            d['options'] = self.options
        if self.blanks:
            d['blanks'] = self.blanks
        if self.rubric:
            d['rubric'] = self.rubric
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d['id'],
            module_id=d['module_id'],
            section_title=d.get('section_title', ''),
            category=d.get('category', ''),
            question_type=d['question_type'],
            prompt=d['prompt'],
            answer=d['answer'],
            code_language=d.get('code_language'),
            options=d.get('options', []),
            blanks=d.get('blanks', []),
            rubric=d.get('rubric', []),
            source=d.get('source', 'auto'),
        )
