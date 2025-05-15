import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# This is a test file for the user service in a backend application.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from backend.app.services.instructor_service import (
    create_instructor,
    create_instructor_rating,
    create_instructor_course_assignment,
    get_instructor_courses
)


class TestInstructorService(unittest.TestCase):

    def setUp(self):
        self.valid_data = {
            "name": "Dr. Smith",
            "title": "Professor",
            "bio": "Expert in Computer Science"
        }
        self.rating_data = {
            "rating": 4
        }
        self.assignment_data = {
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "is_active": True
        }

    @patch("backend.app.services.instructor_service.db")
    @patch("backend.app.services.instructor_service.Instructor")
    def test_create_instructor_success(self, mock_instructor_class, mock_db):
        mock_instance = MagicMock(id=1)
        mock_instructor_class.return_value = mock_instance

        success, result = create_instructor(self.valid_data)
        self.assertTrue(success)
        self.assertEqual(result, 1)
        mock_db.session.add.assert_called_once()
        mock_db.session.commit.assert_called_once()

    def test_create_instructor_missing_fields(self):
        incomplete_data = {"name": "X"}  # missing title, bio
        success, msg = create_instructor(incomplete_data)
        self.assertFalse(success)
        self.assertEqual(msg, "Missing instructor fields")

    @patch("backend.app.services.instructor_service.db")
    @patch("backend.app.services.instructor_service.InstructorRating")
    def test_create_instructor_rating_valid(self, mock_rating_class, mock_db):
        mock_instance = MagicMock()
        mock_rating_class.return_value = mock_instance

        success, result = create_instructor_rating(1, 2, self.rating_data)
        self.assertTrue(success)
        self.assertEqual(result, "success")
        mock_db.session.add.assert_called_once()
        mock_db.session.commit.assert_called_once()

    def test_create_instructor_rating_invalid(self):
        data = {"rating": 6}  # invalid
        success, msg = create_instructor_rating(1, 2, data)
        self.assertFalse(success)
        self.assertEqual(msg, "Invalid rating")

    def test_create_instructor_rating_missing(self):
        data = {}  # no rating
        success, msg = create_instructor_rating(1, 2, data)
        self.assertFalse(success)
        self.assertEqual(msg, "Invalid rating")

    @patch("backend.app.services.instructor_service.db")
    @patch("backend.app.services.instructor_service.CourseInstructor")
    def test_create_instructor_course_assignment_success(self, mock_ci_class, mock_db):
        mock_instance = MagicMock()
        mock_ci_class.return_value = mock_instance

        success, result = create_instructor_course_assignment(1, 101, self.assignment_data)
        self.assertTrue(success)
        self.assertEqual(result, "success")
        mock_db.session.add.assert_called_once()
        mock_db.session.commit.assert_called_once()

    def test_create_instructor_course_assignment_missing_fields(self):
        bad_data = {"start_date": "2024-01-01"}  # missing is_active
        success, msg = create_instructor_course_assignment(1, 101, bad_data)
        self.assertFalse(success)
        self.assertEqual(msg, "Missing course_instructor fields")

    @patch("backend.app.services.instructor_service.db")
    @patch("backend.app.services.instructor_service.Course")
    @patch("backend.app.services.instructor_service.CourseInstructor")
    def test_get_instructor_courses_success(self, mock_ci_class, mock_course_class, mock_db):
        mock_query = MagicMock()
        mock_db.session.query.return_value = mock_query
        mock_query.join.return_value.filter.return_value.all.return_value = ["course1", "course2"]

        result = get_instructor_courses(1)
        self.assertEqual(result, ["course1", "course2"])


if __name__ == "__main__":
    unittest.main()
