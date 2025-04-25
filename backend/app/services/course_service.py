# backend/app/services/course_service.py
import hashlib
import os

from werkzeug.utils import secure_filename

from backend.app.models import db
from backend.app.models.course import Course
from backend.app.models.instructor import Instructor
from backend.app.models.course_rating import CourseRating
from backend.app.models.course_instructor import CourseInstructor
from backend.app.models.comment import Comment
from backend.app.models.file import File
from datetime import datetime, UTC


def create_course(data):
    required_fields = ["code", "name", "semester", "exam_type", "description"]
    if not all(field in data for field in required_fields):
        return False, "Missing course fields"

    course = Course(
        code=data["code"],
        name=data["name"],
        semester=data["semester"],
        exam_type=data["exam_type"],
        description=data["description"]
    )
    try:
        db.session.add(course)
        db.session.commit()
        return True, course.id
    except:
        print("Error while trying to insert data in course table")


def create_course_rating(user_id, course_id, data):
    rating = data.get("rating")
    comment = data.get("comment", "")

    if not rating or not (1 <= rating <= 5):
        return False, "Invalid rating"

    course_rating = CourseRating(
        course_id=course_id,
        user_id=user_id,
        rating=rating,
        comment=comment,
        created_at=datetime.now(UTC)
    )
    try:
        db.session.add(course_rating)
        db.session.commit()
        return True, "Success"
    except:
        print("Error while trying to insert data in course_rating table")


def add_course_comment(user_id, course_id, data):
    content = data.get("content")
    if not content:
        return False, "Comment cannot be empty"

    comment = Comment(
        course_id=course_id,
        user_id=user_id,
        content=content,
        created_at=datetime.now(UTC)
    )
    try:
        db.session.add(comment)
        db.session.commit()
        return True, "Success"
    except:
        print("Error while trying to insert data in comment table")


def get_course_files(course_id):
    files = File.query.filter_by(course_id=course_id).all()
    return [
        {"name": f.name, "url": f.url, "uploaded_at": f.uploaded_at.isoformat()}
        for f in files
    ]


UPLOAD_FOLDER = "backend/uploads"


def upload_course_file(course_id, uploaded_file):
    if not uploaded_file:
        return False, "No file provided"

    url = f"/upload/{uploaded_file.filename}"

    file_hash = get_file_hash(uploaded_file)

    # check for duplicate file content
    from backend.app.models import File
    existing = File.query.filter_by(course_id=course_id, hash=file_hash).first()
    if existing:
        return False, "Duplicate file content detected"

    filename = secure_filename(uploaded_file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    uploaded_file.save(save_path)
    url = f"/uploads/{filename}"

    file_record = File(
        course_id=course_id,
        hash=file_hash,
        name=uploaded_file.filename,
        url=url,
        uploaded_at=datetime.now(UTC)
    )
    try:
        db.session.add(file_record)
        db.session.commit()
        return True, url
    except:
        print("Error while trying to insert data in file table")


def get_file_hash(file):
    """read file in chunks to avoid memory issues"""
    sha256 = hashlib.sha256()
    while chunk := file.read(8192):
        sha256.update(chunk)
    file.seek(0)  # reset file pointer to the beginning
    return sha256.hexdigest()


def get_course_instructors(course_id):
    instructors = (
        db.session.query(Instructor)
            .join(CourseInstructor, Instructor.id == CourseInstructor.instructor_id)
            .filter(CourseInstructor.course_id == course_id)
            .all()
    )
    return instructors
