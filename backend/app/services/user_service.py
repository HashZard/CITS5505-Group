# backend/app/services/user_service.py

from backend.app.models.user import User


def get_user_profile(user_id):
    user = User.query.get(user_id)

    if not user:
        return False, "User not found"

    user_data = {
        "email": user.email,
        "student_id": user.student_id,
        "field": user.field,
        "favourite_courses": [
            {
                "id": course.id,
                "code": course.code,
                "name": course.name
            }
            for course in user.favourite_courses
        ]
    }

    return True, user_data
