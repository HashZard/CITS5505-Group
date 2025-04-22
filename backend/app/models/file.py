from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class File(BaseModel):
    __tablename__ = 'file'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    hash = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.Text, nullable=False)  # e.g., OSS link or file path

    course = db.relationship('Course', backref='files')
