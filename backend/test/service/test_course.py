# tests/test_course_api.py
import random
import unittest

from backend.app import create_app
from backend.app.models.course import Course


class CourseApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def setUp(self):
        # Simulate login by setting session['user_id']
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1  # mock user

    def test_full_course_flow(self):
        # Step 1: Generate a course with CITS+4 digits and diverse metadata
        unique_code = f"CITS{random.randint(1000, 9999)}"
        name = random.choice([
            "AI for Business", "Secure Systems", "Cloud Infrastructure", "Data Mining"
        ])
        description = random.choice([
            "Project-heavy and practical.",
            "Covers both theory and application.",
            "Focused on industry use cases.",
            "Excellent preparation for internships."
        ])
        payload = {
            "code": unique_code,
            "name": name,
            "semester": "2025S1",
            "exam_type": random.choice(["open book", "closed book", "project"]),
            "description": description
        }

        # Step 2: Create course
        response = self.client.post("/api/courses/create", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("course_code", response.json)
        course_code = response.json["course_code"]

        # Step 3: Submit rating
        rate_payload = {
            "rating": random.randint(3, 5),
            "comment": random.choice([
                "Very practical and insightful.",
                "Could use more hands-on projects.",
                "Challenging but rewarding!"
            ])
        }
        rate_response = self.client.post(f"/api/courses/{course_code}/rate", json=rate_payload)
        self.assertEqual(rate_response.status_code, 200)
        self.assertTrue(rate_response.json.get("success"))

        # Step 4: Submit comment
        comment_payload = {
            "content": random.choice([
                "Expect weekly quizzes and a big project.",
                "Make sure to attend all lectures!",
                "Very collaborative environment."
            ])
        }
        comment_response = self.client.post(f"/api/courses/{course_code}/comment", json=comment_payload)
        self.assertEqual(comment_response.status_code, 200)
        self.assertTrue(comment_response.json.get("success"))

        # Step 5: Verify the course in DB
        with self.app.app_context():
            course = Course.query.get(course_code)
            self.assertIsNotNone(course)
            self.assertEqual(course.code, unique_code)
            self.assertEqual(course.name, name)
            self.assertEqual(course.description, description)


if __name__ == '__main__':
    unittest.main()
