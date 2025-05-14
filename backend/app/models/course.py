from enum import Enum

from sqlalchemy import Enum as SQLAlchemyEnum, JSON

from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class CourseStatus(Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"


class Course(BaseModel):
    __tablename__ = 'course'

    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g., CITS5501
    name = db.Column(db.String(100), nullable=False)
    # semester = db.Column(db.String(20))  # e.g., 2024S2
    exam_type = db.Column(db.String(100))  # e.g., open book, closed exam
    description = db.Column(db.Text)

    status = db.Column(SQLAlchemyEnum(CourseStatus), default=CourseStatus.PENDING, nullable=False)
    agree_votes = db.Column(db.Integer, default=0)
    disagree_votes = db.Column(db.Integer, default=0)

    structure = db.Column(JSON, nullable=True)  # JSON structure for course content, e.g., {"weeks": [{"week": 1, "content": "Introduction"}]}

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "exam_type": self.exam_type,
            "status": self.status.value,
            "agree_votes": self.agree_votes,
            "disagree_votes": self.disagree_votes,
            "structure": self.structure or {}
        }
