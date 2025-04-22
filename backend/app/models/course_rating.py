from datetime import datetime, UTC

from backend.app import db
from backend.app.models.basemodel import BaseModel


class CourseRating(BaseModel):
    __tablename__ = 'course_rating'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1~5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))

    user = db.relationship('User', backref='course_ratings')
    course = db.relationship('Course', backref='ratings')
