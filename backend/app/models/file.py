from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class File(BaseModel):
    __tablename__ = 'file'

    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_code = db.Column(db.String(20), db.ForeignKey('course.code'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    hash = db.Column(db.String(64), nullable=False)

    # Optional: path or storage URL
    file_path = db.Column(db.String(255), nullable=False)

    course = db.relationship('Course', backref='files')

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "description": self.description,
        }
