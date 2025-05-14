# generate_demo_courses.py
import hashlib

from faker import Faker
import random

from werkzeug.security import generate_password_hash

from backend.app import db
from backend.app.app import app
from backend.app.models.comment import Comment
from backend.app.models.course import Course, CourseStatus
from backend.app.models.course_rating import CourseRating
from backend.app.models.favourite_courses import FavouriteCourses
from backend.app.models.file import File
from backend.app.models.message import Message
from backend.app.models.user import User, UserType
from backend.test.admin_user import generate_admin

fake = Faker()


# ---------- RESET DATA ----------

def clear_all_data():
    with app.app_context():
        print("🧨 Clearing existing data...")
        db.session.execute(FavouriteCourses.delete())

        Comment.query.delete()
        CourseRating.query.delete()
        Message.query.delete()
        File.query.delete()

        User.query.delete()
        Course.query.delete()

        db.session.commit()
        print("✅ All data cleared.\n")


# ---------- GENERATE COURSES ----------
def generate_structure():
    return {
        "finalExam": {"enabled": True, "weight": random.choice([40, 50])},
        "midSemesterExam": {"enabled": True, "weight": random.choice([10, 20])},
        "projectWork": {"enabled": True, "weight": random.choice([20, 30])},
        "assignment": {"enabled": True, "weight": random.choice([10, 20])},
        "attendance": {"enabled": random.choice([True, False]), "weight": random.choice([0, 5, 10])}
    }


def generate_courses(n=10):
    with app.app_context():
        courses = []
        for i in range(n):
            course = Course(
                code=f"CITS{random.randint(1000, 9999)}",
                name=fake.sentence(nb_words=3).replace('.', ''),
                exam_type=random.choice(["Open Book", "Closed Exam", "Take-home"]),
                description=fake.paragraph(),
                status=CourseStatus.ACTIVE,
                agree_votes=random.randint(0, 50),
                disagree_votes=random.randint(0, 10),
                structure=generate_structure()
            )
            courses.append(course)

        db.session.add_all(courses)
        db.session.commit()
        print(f"✅ Successfully inserted {n} demo courses.")


def hash_password(raw_password):
    return generate_password_hash(raw_password)


def generate_users(n=10):
    with app.app_context():
        courses = Course.query.all()
        if not courses:
            print("⚠️ Cannot assign favourites: no courses in database.")
            return

        users = []
        for _ in range(n):
            name = fake.name()
            email = f"{fake.unique.user_name()}@uwa.edu.au"
            user = User(
                name=name,
                email=email,
                _password=hash_password("password123"),
                department=fake.job(),
                role=UserType.USER,
                field=random.choice(["Computer Science", "Business", "Mathematics", "Design"])
            )

            # For each user, randomly select 3 courses as favourites
            favourite = random.sample(courses, min(3, len(courses)))
            for course in favourite:
                user.favourite_courses.append(course)

            users.append(user)

        db.session.add_all(users)
        db.session.commit()
        print(f"✅ Inserted {n} users with 3 favourite courses each.")


def generate_course_interactions():
    with app.app_context():
        users = User.query.all()
        courses = Course.query.all()

        if not users or not courses:
            print("⚠️ Missing users or courses for interaction.")
            return

        ratings = []
        comments = []

        for user in users:
            for course in courses:
                ratings.append(CourseRating(
                    user_id=user.id,
                    course_code=course.code,
                    rating=random.randint(1, 5),
                    comment=fake.sentence(nb_words=8)
                ))

                comments.append(Comment(
                    user_id=user.id,
                    course_code=course.code,
                    content=fake.sentence(nb_words=random.randint(10, 15))
                ))

        db.session.add_all(ratings + comments)
        db.session.commit()
        print(f"✅ Inserted {len(ratings)} ratings and {len(comments)} comments "
              f"({len(users)} users × {len(courses)} courses).\n")


def generate_messages(n=30):
    with app.app_context():
        users = User.query.all()
        if len(users) < 2:
            print("⚠️ Not enough users to generate messages.")
            return

        messages = []
        for _ in range(n):
            sender, receiver = random.sample(users, 2)  # 确保 sender ≠ receiver

            message = Message(
                sender_id=sender.id,
                receiver_id=receiver.id,
                content=fake.sentence(nb_words=random.randint(5, 15)),
                is_read=random.choice([True, False])
            )
            messages.append(message)

        db.session.add_all(messages)
        db.session.commit()
        print(f"✅ Inserted {n} user-to-user messages.\n")


def generate_course_files_per_course(num_files_per_course=3):
    with app.app_context():
        users = User.query.all()
        courses = Course.query.all()

        if not users or not courses:
            print("⚠️ Cannot generate files: missing users or courses.")
            return

        files = []

        for course in courses:
            sampled_users = random.sample(users, min(num_files_per_course, len(users)))
            for user in sampled_users:
                fake_filename = fake.file_name(extension=random.choice(["pdf", "docx", "pptx", "txt"]))
                fake_content = fake.text()
                fake_hash = hashlib.sha256(fake_content.encode('utf-8')).hexdigest()

                file = File(
                    uploader_id=user.id,
                    course_code=course.code,
                    filename=fake_filename,
                    description=fake.sentence(nb_words=8),
                    hash=fake_hash,
                    file_path=f"/mock_storage/{course.code}/{fake_filename}"
                )
                files.append(file)

        db.session.add_all(files)
        db.session.commit()
        print(f"✅ Inserted {len(files)} files: {len(courses)} courses × {num_files_per_course} users each.\n")


if __name__ == "__main__":
    # Clear existing data
    clear_all_data()
    # Generate admin user
    generate_admin()
    # Generate demo data
    generate_courses(10)
    generate_users(10)
    generate_course_interactions()
    generate_messages(30)
    generate_course_files_per_course(3)
    # Generate favourite courses

