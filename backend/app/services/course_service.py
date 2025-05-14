# backend/app/services/course_service.py
import hashlib
import os

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from sqlalchemy import func

from backend.app.models import db
from backend.app.models.course import Course, CourseStatus
from backend.app.models.instructor import Instructor
from backend.app.models.course_rating import CourseRating
from backend.app.models.course_instructor import CourseInstructor
from backend.app.models.comment import Comment
from backend.app.models.file import File
from datetime import datetime, UTC

from backend.app.models.user import User
from backend.app.utils.pagination_util import paginate_query


def create_course(data):
    required_fields = ["code", "name", "description"]
    if not all(field in data for field in required_fields):
        return False, "Missing course fields"

    # handle structure field
    raw_structure = data.get("scoreStructure", {})
    structure = {}

    for key, value in raw_structure.items():
        try:
            weight = int(value)
        except ValueError:
            return False, f"Invalid weight for {key}"

        structure[key] = {
            "enabled": weight > 0,
            "weight": weight
        }

    # Only required necessary fields for course creation
    course = Course(
        code=data["code"],
        name=data["name"],
        description=data["description"],
        structure=structure,
        status=CourseStatus.PENDING
    )
    try:
        db.session.add(course)
        db.session.commit()
        return True, course.code
    except:
        print("Error while trying to insert data in course table")


def vote_on_course(course_code, agree=True, threshold=5):
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        return False, "Course not found"

    if course.status != CourseStatus.PENDING:
        return False, f"Voting closed. Current status: {course.status.value}"

    # update vote counts
    if agree:
        course.agree_votes += 1
    else:
        course.disagree_votes += 1

    # check if the course should be activated or rejected
    if course.agree_votes >= threshold:
        course.status = CourseStatus.ACTIVE
    elif course.disagree_votes >= threshold:
        course.status = CourseStatus.REJECTED

    db.session.commit()
    return True, {
        "status": course.status.value,
        "agree_votes": course.agree_votes,
        "disagree_votes": course.disagree_votes
    }


def search_courses(keyword, page=1, per_page=10):
    if not keyword:
        return False, "Keyword is required", []

    like_pattern = f"%{keyword}%"

    query = Course.query.filter(
        (Course.name.ilike(like_pattern)) |
        (Course.code.ilike(like_pattern)) |
        (Course.description.ilike(like_pattern))
    )

    result = paginate_query(query, page, per_page)
    return True, result


def get_latest_courses(limit=3):
    try:
        courses = Course.query.order_by(Course.created_gmt.desc()).limit(limit).all()
        return True, [course.to_dict() for course in courses]
    except Exception as e:
        return False, str(e)


def get_top_rated_courses(limit=3):
    try:
        subquery = (
            db.session.query(
                CourseRating.course_code,
                func.count().label('rating_count'),
                func.avg(CourseRating.rating).label('avg_rating')
            )
            .group_by(CourseRating.course_code)
            # .having(func.count() >= 2)
            .subquery()
        )

        results = (
            db.session.query(
                Course.code,
                Course.name,
                subquery.c.avg_rating,
                subquery.c.rating_count
            )
            .join(subquery, Course.code == subquery.c.course_code)
            .order_by(subquery.c.avg_rating.desc())
            .limit(limit)
            .all()
        )

        top_courses = [{
            "code": row.code,
            "name": row.name,
            "avg_rating": round(row.avg_rating, 2),
            "rating_count": row.rating_count
        } for row in results]

        return True, top_courses

    except Exception as e:
        return False, str(e)


def get_course_detail(code):
    course = Course.query.filter_by(code=code).first()
    if not course:
        return False, None

    return True, course.to_dict()


def upsert_course_rating(user_id, course_code, data):
    rating = data.get("rating")
    comment = data.get("comment", "")

    if not rating or not (1 <= rating <= 5):
        return False, "Invalid rating"

    try:
        # check if the user has already rated this course
        existing = CourseRating.query.filter_by(user_id=user_id, course_code=course_code).first()

        if existing:
            # update existing rating
            existing.rating = rating
            existing.comment = comment
            message = "Rating updated"
        else:
            # create new rating
            new_rating = CourseRating(
                course_code=course_code,
                user_id=user_id,
                rating=rating,
                comment=comment
            )
            db.session.add(new_rating)
            message = "Rating created"

        db.session.commit()
        return True, message

    except Exception as e:
        print(f"Error during upsert course_rating: {e}")
        db.session.rollback()
        return False, "Database error"


def get_rating_distribution(course_code):
    result = db.session.query(
        CourseRating.rating,
        func.count().label("count")
    ).filter_by(course_code=course_code).group_by(CourseRating.rating).all()

    # return a dictionary with rating as key and count as value
    return {rating: count for rating, count in result}


def add_course_comment(user_id, course_code, data):
    content = data.get("content")
    if not content:
        return False, "Comment cannot be empty"

    comment = Comment(
        course_code=course_code,
        user_id=user_id,
        content=content,
        created_at=datetime.now(UTC)
    )
    try:
        db.session.add(comment)
        db.session.commit()
        return True, "Success"
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return False, "Database error"


def get_course_comments(course_code, page=1, per_page=5):
    query = Comment.query.filter_by(course_code=course_code).order_by(Comment.created_at.desc())
    return paginate_query(query, page, per_page)


def get_course_files(course_code):
    files = File.query.filter_by(course_code=course_code).all()
    return [{
        "id": f.id,
        "filename": f.filename,
        "description": f.description,
        "uploaded_at": f.updated_gmt.strftime("%Y-%m-%d %H:%M"),
        "uploader": f.uploader.email,
        "download_url": f"/uploads/{f.course_code}/{f.filename}"  # adjust if needed
    } for f in files]


UPLOAD_FOLDER = "backend/uploads"


def get_course_file(course_code, filename):
    safe_filename = secure_filename(filename)
    course_folder = os.path.join(UPLOAD_FOLDER, course_code)
    full_path = os.path.join(course_folder, safe_filename)

    if not os.path.isfile(full_path):
        return None

    return {
        "directory": course_folder,
        "filename": safe_filename
    }


def upload_course_file(user_id, course_code, uploaded_file, descriptions):
    if not uploaded_file:
        return False, "No file provided"

    file_hash = get_file_hash(uploaded_file)

    # check for duplicate file content
    existing = File.query.filter_by(course_code=course_code, hash=file_hash).first()
    if existing:
        return False, "Duplicate file content detected"

    filename = secure_filename(uploaded_file.filename)
    course_folder = os.path.join(UPLOAD_FOLDER, course_code)
    os.makedirs(course_folder, exist_ok=True)

    save_path = os.path.join(course_folder, filename)
    uploaded_file.save(save_path)

    file_record = File(
        uploader_id=user_id,  # Placeholder for uploader ID
        course_code=course_code,
        filename=filename,
        description=descriptions,
        hash=file_hash,
        file_path=save_path,
    )

    try:
        db.session.add(file_record)
        db.session.commit()
        return True, file_record.to_dict()
    except:
        import traceback
        print("Error while trying to insert data in file table")
        traceback.print_exc()  # ✅ 打印堆栈信息
        db.session.rollback()
    return False, "Database error"


def get_file_hash(file):
    """read file in chunks to avoid memory issues"""
    sha256 = hashlib.sha256()
    while chunk := file.read(8192):
        sha256.update(chunk)
    file.seek(0)  # reset file pointer to the beginning
    return sha256.hexdigest()


def get_course_instructors(course_code):
    instructors = (
        db.session.query(Instructor)
        .join(CourseInstructor, Instructor.id == CourseInstructor.instructor_id)
        .filter(CourseInstructor.course_code == course_code)
        .all()
    )
    return instructors


def add_course_to_favorites(user_id, course_code):
    user = User.query.get(user_id)
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        return False, "Course not found"

    if course in user.favourite_courses:
        user.favourite_courses.remove(course)
        db.session.commit()
        return True, "removed"

    user.favourite_courses.append(course)
    db.session.commit()
    return True, "added"
