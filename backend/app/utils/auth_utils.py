from functools import wraps
from flask import session, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"success": False, "message": "Authentication required"}), 401
        return f(user_id=user_id, *args, **kwargs)
    return decorated_function
