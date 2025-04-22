from datetime import UTC, datetime

from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class Comment(BaseModel):
    __tablename__ = 'comment'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))

    user = db.relationship('User', backref='comments')
    course = db.relationship('Course', backref='comments')
