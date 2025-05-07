from enum import Enum
from sqlalchemy import Enum as SqlEnum
from werkzeug.security import generate_password_hash, check_password_hash

from backend.app.models import db
from backend.app.models.basemodel import BaseModel
from backend.app.models.favourite_courses import FavouriteCourses


class UserType(Enum):
    USER = "user"
    ADMIN = "admin"


class User(BaseModel):
    __tablename__ = 'user'

    email = db.Column(db.String(128), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    role = db.Column(SqlEnum(UserType), default=UserType.USER, nullable=False)
    field = db.Column(db.String(255), nullable=True)
    favourite_courses = db.relationship(
        'Course',
        secondary=FavouriteCourses,  # used to get list of courses liked by user
        # backref='liked_by_users'  # used to get list of users that like a course
    )

    @property
    def student_id(self):
        # Extract the student ID from the email if the email is in the expected format
        if '@student.uwa.edu.au' in self.email:
            return self.email.split('@')[0]
        return None

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return check_password_hash(self._password, plaintext)
