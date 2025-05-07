from backend.app.models import db
from backend.app.models.basemodel import BaseModel


class CourseRating(BaseModel):
    __tablename__ = 'course_rating'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_code = db.Column(db.String(20), db.ForeignKey('course.code'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1~5
    comment = db.Column(db.Text)

    user = db.relationship('User', backref='course_ratings')
    course = db.relationship('Course', backref='ratings')
