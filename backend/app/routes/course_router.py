from flask import Blueprint, request, jsonify
from backend.app.services.course_service import (
    create_course,
    create_course_rating,
    add_course_comment,
    get_course_files,
    upload_course_file,
    get_course_instructors, search_courses, get_course_detail
)
from backend.app.utils.auth_utils import login_required

course_bp = Blueprint('course', __name__, url_prefix='/api/courses')


@course_bp.route("/create", methods=["POST"])
@login_required
def create_course_route(user_id):
    data = request.json
    success, result = create_course(data)
    if not success:
        return jsonify({"success": False, "message": result}), 400
    return jsonify({"success": True, "course_id": result})


@course_bp.route('/search', methods=['GET'])
def search_courses_route():
    keyword = request.args.get('keyword', '').strip()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    success, result = search_courses(keyword, page, per_page)
    if not success:
        return jsonify({"success": False, "message": result, "data": []}), 400

    return jsonify({"success": True, **result})


@course_bp.route('/detail', methods=['GET'])
def course_detail_route():
    code = request.args.get('code')
    if not code:
        return jsonify({"success": False, "message": "Missing course code"}), 400

    success, course_data = get_course_detail(code)
    if not success:
        return jsonify({"success": False, "message": "Course not found"}), 404

    return jsonify({"success": True, "data": course_data})


@course_bp.route("/<int:course_id>/rate", methods=["POST"])
@login_required
def rate_course_route(course_id, user_id):
    data = request.json
    success, message = create_course_rating(user_id, course_id, data)
    if not success:
        return jsonify({"success": False, "message": message}), 400
    return jsonify({"success": True, "message": message})


@course_bp.route("/<int:course_id>/comment", methods=["POST"])
@login_required
def comment_course_route(course_id, user_id):
    data = request.json
    success, message = add_course_comment(user_id, course_id, data)
    if not success:
        return jsonify({"success": False, "message": message}), 400
    return jsonify({"success": True})


@course_bp.route("/<int:course_id>/files", methods=["GET"])
def get_course_files_route(course_id):
    return jsonify({"files": get_course_files(course_id)})


@course_bp.route("/<int:course_id>/files/upload", methods=["POST"])
@login_required
def upload_course_file_route(course_id, user_id):
    uploaded_file = request.files.get("file")
    success, result = upload_course_file(course_id, uploaded_file)
    if not success:
        return jsonify({"success": False, "message": result}), 400
    return jsonify({"success": True, "file_url": result})


@course_bp.route("/<int:course_id>/instructors", methods=["GET"])
def get_course_instructors_route(course_id):
    instructors = get_course_instructors(course_id)
    instructor_data = [
        {
            "id": instructor.id,
            "name": instructor.name,
            "title": instructor.title,
            "bio": instructor.bio
        }
        for instructor in instructors
    ]
    return jsonify({"success": True, "instructors": instructor_data})
