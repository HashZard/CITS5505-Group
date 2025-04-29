from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class Course(BaseModel):
    __tablename__ = 'course'

    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g., CITS5501
    name = db.Column(db.String(100), nullable=False)
    # semester = db.Column(db.String(20))  # e.g., 2024S2
    exam_type = db.Column(db.String(100))  # e.g., open book, closed exam
    description = db.Column(db.Text)
