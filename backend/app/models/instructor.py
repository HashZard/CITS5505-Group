from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class Instructor(BaseModel):
    __tablename__ = 'instructor'

    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    bio = db.Column(db.Text)
