import os

from flask import Blueprint, request, jsonify, session, abort, send_from_directory
from backend.app.services.course_service import (
    create_course,
    upsert_course_rating,
    add_course_comment,
    get_course_files,
    upload_course_file,
    get_course_instructors, search_courses, get_course_detail, get_course_comments, get_rating_distribution,
    add_course_to_favorites, get_course_file, vote_on_course, get_latest_courses, get_top_rated_courses
)
from backend.app.utils.auth_utils import login_required

course_bp = Blueprint('course', __name__, url_prefix='/api/courses')


@course_bp.route("/create", methods=["POST"])
@login_required
def create_course_route():
    data = request.json
    success, result = create_course(data)
    if not success:
        return jsonify({"success": False, "message": result}), 400
    return jsonify({"success": True, "course_code": result})


@course_bp.route("/<string:course_code>/vote", methods=["POST"])
def vote_course_route(course_code):
    data = request.get_json() or {}
    agree = data.get("agree")

    if agree is None:
        return jsonify({"success": False, "message": "Missing 'agree' field"}), 400

    success, result = vote_on_course(course_code, agree=bool(agree))
    if not success:
        return jsonify({"success": False, "message": result}), 400

    return jsonify({"success": True, "result": result})


@course_bp.route('/search', methods=['GET'])
def search_courses_route():
    keyword = request.args.get('keyword', '').strip()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    success, result = search_courses(keyword, page, per_page)
    if not success:
        return jsonify({"success": False, "message": result, "data": []}), 400

    return jsonify({"success": True, **result})


@course_bp.route('/latest', methods=['GET'])
def latest_courses_route():
    limit = int(request.args.get('limit', 3))

    success, result = get_latest_courses(limit)
    if not success:
        return jsonify({"success": False, "message": result}), 500

    return jsonify({"success": True, "courses": result})


@course_bp.route('/top-rated', methods=['GET'])
def top_rated_courses_route():
    limit = int(request.args.get('limit', 3))
    success, result = get_top_rated_courses(limit)
    if not success:
        return jsonify({"success": False, "message": result}), 500
    return jsonify({"success": True, "courses": result})


@course_bp.route('/detail', methods=['GET'])
def course_detail_route():
    code = request.args.get('code')
    if not code:
        return jsonify({"success": False, "message": "Missing course code"}), 400

    success, course_data = get_course_detail(code)
    if not success:
        return jsonify({"success": False, "message": "Course not found"}), 404

    return jsonify({"success": True, "data": course_data})


@course_bp.route("/<string:course_code>/rate", methods=["POST"])
@login_required
def rate_course(course_code):
    user_id = session.get("user_id")
    data = request.json
    success, message = upsert_course_rating(user_id, course_code, data)
    return jsonify({"success": success, "message": message}), (200 if success else 400)


@course_bp.route("/<string:course_code>/ratings/distribution", methods=["GET"])
def rating_distribution(course_code):
    try:
        data = get_rating_distribution(course_code)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@course_bp.route("/<string:course_code>/comment", methods=["POST"])
@login_required
def comment_course_route(course_code):
    user_id = session.get("user_id")
    data = request.json
    success, message = add_course_comment(user_id, course_code, data)
    if not success:
        return jsonify({"success": False, "message": message}), 400
    return jsonify({"success": True})


@course_bp.route("/<string:course_code>/comments", methods=["GET"])
def get_course_comments_route(course_code):
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
        result = get_course_comments(course_code, page, per_page)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        print("Error in get_course_comments_route:", e)
        return jsonify({"success": False, "message": "Failed to load comments"}), 500


@course_bp.route("/<string:course_code>/files", methods=["GET"])
def get_course_files_route(course_code):
    return jsonify({"success": True, "files": get_course_files(course_code)})


@course_bp.route("/<string:course_code>/files/download/<path:filename>", methods=["GET"])
def download_course_file(course_code, filename):
    file_info = get_course_file(course_code, filename)

    if not file_info:
        print("File not found in database")
        abort(404, description="File not found")

    return send_from_directory(
        directory=os.path.abspath(file_info["directory"]),
        path=file_info["filename"],
        as_attachment=True
    )


@course_bp.route("/<string:course_code>/files/upload", methods=["POST"])
# @login_required
def course_file(course_code):
    user_id = session.get("user_id")
    uploaded_file = request.files.get("file")
    descriptions = request.form.get("description")
    success, result = upload_course_file(user_id, course_code, uploaded_file, descriptions)
    if not success:
        return jsonify({"success": False, "message": result}), 400
    return jsonify({"success": True, "file_url": result})


@course_bp.route("/<string:course_code>/instructors", methods=["GET"])
def get_course_instructors_route(course_code):
    instructors = get_course_instructors(course_code)
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


@course_bp.route("/<string:course_code>/favorite", methods=["POST"])
@login_required
def favorite_course_route(course_code):
    user_id = session.get("user_id")
    success, status = add_course_to_favorites(user_id, course_code)
    if not success:
        return jsonify({"success": False, "message": status}), 400
    return jsonify({"success": True, "status": status})
