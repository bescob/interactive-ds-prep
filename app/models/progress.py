from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta
from app.config import SM2_INTERVALS


@dataclass
class QuestionProgress:
    question_id: str
    status: str = 'unseen'  # unseen, attempted, correct, needs_review
    attempts: int = 0
    streak: int = 0
    last_grade: Optional[str] = None  # 'correct', 'partial', 'incorrect'
    last_attempt: Optional[str] = None  # ISO datetime
    next_review: Optional[str] = None  # ISO date
    interval_index: int = 0  # index into SM2_INTERVALS

    def record_attempt(self, grade: str):
        self.attempts += 1
        self.last_grade = grade
        self.last_attempt = datetime.now().isoformat()

        if grade == 'correct':
            self.streak += 1
            self.status = 'correct'
            self.interval_index = min(self.interval_index + 1, len(SM2_INTERVALS) - 1)
        elif grade == 'partial':
            self.streak = 0
            self.status = 'attempted'
            self.interval_index = max(self.interval_index - 1, 0)
        else:  # incorrect
            self.streak = 0
            self.status = 'needs_review'
            self.interval_index = 0

        days = SM2_INTERVALS[self.interval_index]
        self.next_review = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            'question_id': self.question_id,
            'status': self.status,
            'attempts': self.attempts,
            'streak': self.streak,
            'last_grade': self.last_grade,
            'last_attempt': self.last_attempt,
            'next_review': self.next_review,
            'interval_index': self.interval_index,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


@dataclass
class ModuleProgress:
    module_id: str
    status: str = 'not_started'  # not_started, in_progress, completed
    sections_viewed: list = field(default_factory=list)
    total_sections: int = 0

    @property
    def completion_pct(self):
        if self.total_sections == 0:
            return 0
        return int(len(self.sections_viewed) / self.total_sections * 100)

    def to_dict(self):
        return {
            'module_id': self.module_id,
            'status': self.status,
            'sections_viewed': self.sections_viewed,
            'total_sections': self.total_sections,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


@dataclass
class UserProgress:
    modules: dict = field(default_factory=dict)  # module_id -> ModuleProgress
    questions: dict = field(default_factory=dict)  # question_id -> QuestionProgress
    daily_streak: int = 0
    last_study_date: Optional[str] = None  # ISO date
    study_history: list = field(default_factory=list)  # list of ISO dates

    def get_module_progress(self, module_id: str) -> ModuleProgress:
        if module_id not in self.modules:
            self.modules[module_id] = ModuleProgress(module_id=module_id)
        return self.modules[module_id]

    def get_question_progress(self, question_id: str, create: bool = True) -> QuestionProgress:
        if question_id not in self.questions:
            if not create:
                return QuestionProgress(question_id=question_id)
            self.questions[question_id] = QuestionProgress(question_id=question_id)
        return self.questions[question_id]

    def update_streak(self):
        today = datetime.now().strftime('%Y-%m-%d')
        if self.last_study_date == today:
            return
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if self.last_study_date == yesterday:
            self.daily_streak += 1
        else:
            self.daily_streak = 1
        self.last_study_date = today
        if today not in self.study_history:
            self.study_history.append(today)

    def due_for_review(self):
        today = datetime.now().strftime('%Y-%m-%d')
        due = []
        for qp in self.questions.values():
            if qp.next_review and qp.next_review <= today:
                due.append(qp.question_id)
        return due

    @property
    def total_attempted(self):
        return sum(1 for q in self.questions.values() if q.attempts > 0)

    @property
    def total_correct(self):
        return sum(1 for q in self.questions.values() if q.status == 'correct')

    def to_dict(self):
        return {
            'modules': {k: v.to_dict() for k, v in self.modules.items()},
            'questions': {k: v.to_dict() for k, v in self.questions.items()},
            'daily_streak': self.daily_streak,
            'last_study_date': self.last_study_date,
            'study_history': self.study_history,
        }

    @classmethod
    def from_dict(cls, d):
        up = cls()
        up.modules = {k: ModuleProgress.from_dict(v) for k, v in d.get('modules', {}).items()}
        up.questions = {k: QuestionProgress.from_dict(v) for k, v in d.get('questions', {}).items()}
        up.daily_streak = d.get('daily_streak', 0)
        up.last_study_date = d.get('last_study_date')
        up.study_history = d.get('study_history', [])
        return up
