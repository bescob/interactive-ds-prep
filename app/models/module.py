from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ContentBlock:
    type: str  # 'text', 'code', 'table', 'list'
    content: str
    language: Optional[str] = None  # for code blocks: 'sql', 'python', etc.

    def to_dict(self):
        d = {'type': self.type, 'content': self.content}
        if self.language:
            d['language'] = self.language
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(type=d['type'], content=d['content'], language=d.get('language'))


@dataclass
class Section:
    title: str
    category: str  # 'sql', 'python', 'stats', 'ml', 'terminology', 'behavioral', 'product'
    blocks: list = field(default_factory=list)  # list of ContentBlock
    order: int = 0

    def to_dict(self):
        return {
            'title': self.title,
            'category': self.category,
            'blocks': [b.to_dict() for b in self.blocks],
            'order': self.order,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            title=d['title'],
            category=d['category'],
            blocks=[ContentBlock.from_dict(b) for b in d.get('blocks', [])],
            order=d.get('order', 0),
        )


@dataclass
class Module:
    id: str  # e.g. 'module-01'
    title: str  # e.g. 'Warm Up'
    number: int
    subtitle: str = ''  # Topics line
    sections: list = field(default_factory=list)  # list of Section
    source_file: str = ''

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'number': self.number,
            'subtitle': self.subtitle,
            'sections': [s.to_dict() for s in self.sections],
            'source_file': self.source_file,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d['id'],
            title=d['title'],
            number=d['number'],
            subtitle=d.get('subtitle', ''),
            sections=[Section.from_dict(s) for s in d.get('sections', [])],
            source_file=d.get('source_file', ''),
        )
