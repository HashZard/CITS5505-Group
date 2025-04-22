from backend.app import db
from backend.app.models.basemodel import BaseModel


class Instructor(BaseModel):
    __tablename__ = 'instructor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    bio = db.Column(db.Text)
