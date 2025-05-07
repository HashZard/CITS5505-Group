from backend.app.models import db
from backend.app.models.user import User, UserType
import bcrypt


def register_user(email: str, password: str, role: UserType = UserType.USER) -> dict:
    if User.query.filter_by(email=email).first():
        return {"success": False, "message": "Email already exists"}

    new_user = User(email=email, role=role)
    new_user.password = password
    db.session.add(new_user)
    db.session.commit()
    return {"success": True, "message": "Registration successful"}


def verify_user(email: str, password: str) -> dict:
    user = User.query.filter_by(email=email).first()
    print("Password from form:", password)
    print("Hashed password in DB:", user._password)
    print("Check result:", user.check_password(password))
    if user.check_password(password):
        return {"success": True, "user": user}
    return {"success": False, "message": "Password is incorrect"}


def force_reset_password(email: str, new_password: str) -> dict:
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"success": False, "message": "User not found"}

    hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    user.password = hashed_pw
    db.session.commit()

    return {"success": True, "message": "Password reset successfully"}
