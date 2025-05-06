from flask import Blueprint, jsonify, session

from backend.app.services.user_service import get_user_profile
from backend.app.utils.auth_utils import login_required

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile_route():
    user_id = session.get("user_id")
    success, result = get_user_profile(user_id)

    if not success:
        return jsonify({"success": False, "message": result}), 404

    return jsonify({"success": True, "user": result})
