from datetime import datetime, UTC

from backend.app import db
from backend.app.models.basemodel import BaseModel


class File(BaseModel):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.Text, nullable=False)  # e.g., OSS link or file path
    uploaded_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))

    course = db.relationship('Course', backref='files')
