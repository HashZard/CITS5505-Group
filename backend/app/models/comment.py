from datetime import UTC, datetime

from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class Comment(BaseModel):
    __tablename__ = 'comment'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_code = db.Column(db.String(20), db.ForeignKey('course.code'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))

    user = db.relationship('User', backref='comments')
    course = db.relationship('Course', backref='comments')

    def to_dict(self):
        from backend.app.models.user import User
        return {
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "username": User.query.get(self.user_id).email if self.user_id else "Anonymous"
        }
