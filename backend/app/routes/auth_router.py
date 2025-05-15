# backend/routes/auth.py
import random
from captcha.image import ImageCaptcha
from flask import Blueprint, request, jsonify, session, send_file, make_response, current_app
from backend.app.services.auth_service import register_user, verify_user

auth_bp = Blueprint('auth', __name__, url_prefix='/api')


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    code = data.get("code")

    if not email or not password or not code:
        return jsonify({"success": False, "message": "Incomplete information"}), 400

    if code != session.get("captcha_code"):
        return jsonify({"success": False, "message": "Incorrect captcha"}), 403
    session.pop("captcha_code", None)

    result = verify_user(email, password)
    if result["success"]:
        user = result["user"]
        email = user.email
        student_id = email.split('@')[0]

        response = make_response(jsonify({"success": True}))
        response.set_cookie("user_id", str(user.id), httponly=False, samesite="Lax")
        response.set_cookie("student_number", student_id, httponly=False, samesite="Lax")
        response.set_cookie("user_role", user.role.value, httponly=False, samesite="Lax")
        session['user_role'] = user.role.value
        session['user_id'] = user.id
        session['student_number'] = student_id
        return response
    else:
        return jsonify(result), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})


# Captcha generation endpoint
@auth_bp.route("/captcha", methods=["GET"])
def get_captcha():
    image = ImageCaptcha()
    if current_app.config["TESTING"]:
        code = "1111"
    else:
        code = str(random.randint(1000, 9999))
    session["captcha_code"] = code

    image_data = image.generate(code)
    return send_file(image_data, mimetype="image/png")


# Registration endpoint
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    code = data.get("code")

    if not email or not password or not code:
        return jsonify({"success": False, "message": "Incomplete information"}), 400

    if code != session.get("captcha_code"):
        return jsonify({"success": False, "message": "Incorrect captcha"}), 403
    session.pop("captcha_code", None)

    result = register_user(email, password)

    return jsonify(result), 200 if result["success"] else 409
