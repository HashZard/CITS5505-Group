from backend.app.models import db

FavouriteCourses = db.Table(
    'favourite_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('course_code', db.String(20), db.ForeignKey('course.code', ondelete='CASCADE'), primary_key=True)
)
