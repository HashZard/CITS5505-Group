from backend.app.models import db

FavouriteCourses = db.Table(
    'favourite_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', name='fk_fav_user_id'), primary_key=True),
    db.Column('course_code', db.String(20), db.ForeignKey('course.code', name='fk_fav_course_code'), primary_key=True),
    db.UniqueConstraint('user_id', 'course_code', name='uq_user_course')
)

