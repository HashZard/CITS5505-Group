from datetime import datetime, UTC

from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class InstructorRating(BaseModel):
    __tablename__ = 'instructor_rating'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # e.g., 1–5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))

    user = db.relationship('User', backref='instructor_ratings')
    instructor = db.relationship('Instructor', backref='ratings')
