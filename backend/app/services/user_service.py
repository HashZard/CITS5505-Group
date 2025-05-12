# backend/app/services/user_service.py
from backend.app.models import db
from backend.app.models.message import Message
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


def send_message(sender_id, receiver_email, content):
    if not content.strip():
        return False, "Message content cannot be empty"

    receiver = User.query.filter_by(email=receiver_email).first()
    if not receiver:
        return False, "Receiver not found"

    message = Message(
        sender_id=sender_id,
        receiver_id=receiver.id,
        content=content.strip(),
        is_read=False
    )
    db.session.add(message)
    db.session.commit()
    return True, message.id


def get_inbox_messages(user_id):
    messages = (Message.query
                .filter_by(receiver_id=user_id)
                .order_by(Message.created_gmt.desc())
                .all())

    result = []
    for msg in messages:
        result.append({
            "id": msg.id,
            "sender": msg.sender.email,
            "content": msg.content,
            "timestamp": msg.created_gmt.strftime("%Y-%m-%d %H:%M"),
            "is_read": msg.is_read
        })
    return result
