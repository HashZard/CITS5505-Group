# backend/app/services/user_service.py

from backend.app.models.user import User, get_user_by_id, save_user


def get_user_profile(user_id):
    user = User.query.get(user_id)

    if not user:
        return False, "User not found"

    user_data = {
        "id": user.id,
        "name": user.name,
        "department": user.department,
        "email": user.email,
        "student_id": user.email.split('@')[0],
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


def update_user_profile(user_id, new_name, new_department):
    try:
        user = get_user_by_id(user_id)
        if not user:
            return False, "User not found"

        user.name = new_name
        user.department = new_department

        save_user(user)
        return True, None
    except Exception as e:
        return False, str(e)
