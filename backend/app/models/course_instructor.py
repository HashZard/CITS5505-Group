from datetime import datetime, UTC

from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class CourseInstructor(BaseModel):  # ✅ ✅ 继承 BaseModel
    __tablename__ = 'course_instructor'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)

    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))
    end_date = db.Column(db.DateTime)  # null means ongoing
    is_active = db.Column(db.Boolean, default=True)

    course = db.relationship('Course', backref='instructor_history')
    instructor = db.relationship('Instructor', backref='teaching_history')
