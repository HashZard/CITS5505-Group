# create_admin_user.py

from backend.app import create_app
from backend.app.models import db
from backend.app.models.user import User, UserType
import bcrypt

def main():
    app = create_app()
    with app.app_context():
        email = "admin@example.com"
        password = "admin2025"

        existing = User.query.filter_by(email=email).first()
        if existing:
            print(f"⚠️ Admin account {email} already exists")
            return

        admin = User(email=email, password=password, role=UserType.ADMIN)

        db.session.add(admin)
        db.session.commit()
        print(f"✅ Admin account {email} created successfully")

if __name__ == "__main__":
    main()
