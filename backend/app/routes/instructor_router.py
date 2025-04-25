from flask import Blueprint, request, jsonify
from backend.app.services.instructor_service import (
    create_instructor,
    create_instructor_rating,
    create_instructor_course_assignment,
    get_instructor_courses,
    #add_instructor_comment
)
from backend.app.utils.auth_utils import login_required

instructor_bp = Blueprint('instructor', __name__, url_prefix='/api/instructors')

@instructor_bp.route("/create", methods=["POST"])
@login_required
def create_instructor_route(user_id):
    data = request.json
    success, result = create_instructor(data)
    if not success:
        return jsonify({"success": False, "message": result}), 400
    return jsonify({"success": True, "instructor_id": result})


@instructor_bp.route("/<int:instructor_id>/rate", methods=["POST"])
@login_required
def rate_instructor_route(instructor_id, user_id):
    data = request.json
    success, message = create_instructor_rating(user_id, instructor_id, data)
    if not success:
        return jsonify({"success": False, "message": message}), 400
    return jsonify({success: True, "message": message})


@instructor_bp.route("/<int:instructor_id>/course/<int:course_id>/assign", methods=["POST"])
@login_required
def assign_instructor_to_course_route(instructor_id, course_id, user_id):
    data = request.json
    success, message = create_instructor_course_assignment(instructor_id, course_id, data)
    if not success:
        return jsonify({"success": False, "message": message}), 400
    return jsonify({success: True, "message": message})


@instructor_bp.route("/<int:instructor_id>/courses", methods=["GET"])
def get_instructor_courses_route(instructor_id):
    courses = get_instructor_courses(instructor_id)
    course_data = [
        {
            "id": course.id,
            "code": course.code,
            "name": course.name,
            "semester": course.semester,
            "exam_type": course.exam_type,
            "description": course.description
        }
        for course in courses
    ]
    return jsonify({"success": True, "courses": course_data})
