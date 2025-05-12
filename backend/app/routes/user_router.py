from flask import Blueprint, jsonify, session, request

from backend.app.services.user_service import get_user_profile, update_user_profile, send_message, get_inbox_messages
from backend.app.utils.auth_utils import login_required

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route('/check_login', methods=['GET'])
def check_login_status():
    if 'user_id' not in session:
        return jsonify({"logged_in": False}), 401
    return jsonify({"logged_in": True})


@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile_route():
    user_id = session.get("user_id")
    success, result = get_user_profile(user_id)

    if not success:
        return jsonify({"success": False, "message": result}), 404

    return jsonify({"success": True, "user": result})


@user_bp.route('/profile', methods=['POST'])  # or PUT
@login_required
def update_profile_route():
    user_id = session.get("user_id")
    data = request.get_json()

    name = data.get("name", "").strip()
    department = data.get("department", "").strip()

    if not name or not department:
        return jsonify({"success": False, "message": "Name and department are required"}), 400

    success, result = update_user_profile(user_id, name, department)
    if not success:
        return jsonify({"success": False, "message": result}), 500

    return jsonify({"success": True, "message": "Profile updated successfully"})


@user_bp.route('/message/send', methods=['POST'])
@login_required
def send_message_route():
    data = request.get_json() or {}
    receiver_email = data.get("receiver_email")
    content = data.get("content")
    sender_id = session.get("user_id")

    if not receiver_email or not content:
        return jsonify({"success": False, "message": "Missing receiver email or content"}), 400

    success, result = send_message(sender_id, receiver_email, content)
    if success:
        return jsonify({"success": True, "message_id": result})
    else:
        return jsonify({"success": False, "message": result}), 400


@user_bp.route('/message/inbox', methods=['GET'])
@login_required
def inbox_route():
    user_id = session.get("user_id")
    messages = get_inbox_messages(user_id)
    return jsonify({"success": True, "messages": messages})
