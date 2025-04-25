# backend/app/services/instructor_service.py
import hashlib
import os

from backend.app.models import db
from backend.app.models.course import Course
from backend.app.models.instructor import Instructor
from backend.app.models.instructor_rating import InstructorRating
from backend.app.models.course_instructor import CourseInstructor
from datetime import datetime, UTC


def create_instructor(data):
    required_fields = ["name", "title", "bio"]
    if not all(field in data for field in required_fields):
        return False, "Missing instructor fields"

    instructor = Instructor(
        name=data["name"],
        title=data["title"],
        bio=data["bio"]
    )
    try:
        db.session.add(instructor)
        db.session.commit()
        return True, instructor.id
    except:
        print("Error while trying to insert data in instructor table")


def create_instructor_rating(user_id, instructor_id, data):
    rating = data.get("rating")

    if not rating or not (1 <= rating <= 5):
        return False, "Invalid rating"

    instructor_rating = InstructorRating(
        user_id=user_id,
        instructor_id=instructor_id,
        rating=rating,
        created_at=datetime.now(UTC)
    )
    try:
        db.session.add(instructor_rating)
        db.session.commit()
        return True, "success"
    except:
        print("Error while trying to insert data in instructor_rating table")


def create_instructor_course_assignment(instructor_id, course_id, data):
    required_fields = ["start_date", "is_active"]
    if not all(field in data for field in required_fields):
        return False, "Missing course_instructor fields"

    course_instructor = CourseInstructor(
        instructor_id=instructor_id,
        course_id=course_id,
        start_date=data["start_date"],
        end_date=data["end_date"],
        is_active=data["is_active"]
    )
    try:
        db.session.add(course_instructor)
        db.session.commit()
        return True, "success"
    except:
        print("Error while trying to insert data in course_instructor table")


def get_instructor_courses(instructor_id):
    courses = (
        db.session.query(Course)
            .join(CourseInstructor, Course.id == CourseInstructor.course_id)
            .filter(CourseInstructor.instructor_id == instructor_id)
            .all()
    )
    return courses

# def add_instructor_comment(user_id, instructor_id, data):
# ...
