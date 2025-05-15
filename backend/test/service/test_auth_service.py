import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from backend.app.services.auth_service import register_user, verify_user, force_reset_password


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.email = "test@example.com"
        self.password = "secure123"
        self.hashed_password = "$2b$12$fakehashedpassword"

    @patch("backend.app.services.auth_service.User")
    @patch("backend.app.services.auth_service.db")
    def test_register_user_success(self, mock_db, mock_user_class):
        mock_user_class.query.filter_by.return_value.first.return_value = None
        mock_user_instance = MagicMock()
        mock_user_class.return_value = mock_user_instance

        result = register_user(self.email, self.password)

        mock_db.session.add.assert_called_once_with(mock_user_instance)
        mock_db.session.commit.assert_called_once()
        self.assertTrue(result["success"])

    @patch("backend.app.services.auth_service.User")
    def test_register_user_duplicate_email(self, mock_user_class):
        mock_user_class.query.filter_by.return_value.first.return_value = True

        result = register_user(self.email, self.password)

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Email already exists")

    @patch("backend.app.services.auth_service.User")
    def test_verify_user_success(self, mock_user_class):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_user._password = self.hashed_password
        mock_user_class.query.filter_by.return_value.first.return_value = mock_user

        result = verify_user(self.email, self.password)

        self.assertTrue(result["success"])
        self.assertEqual(result["user"], mock_user)

    @patch("backend.app.services.auth_service.User")
    def test_verify_user_wrong_password(self, mock_user_class):
        mock_user = MagicMock()
        mock_user.check_password.return_value = False
        mock_user._password = self.hashed_password
        mock_user_class.query.filter_by.return_value.first.return_value = mock_user

        result = verify_user(self.email, "wrongpass")

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Password is incorrect")

    @patch("backend.app.services.auth_service.db")
    @patch("backend.app.services.auth_service.bcrypt")
    @patch("backend.app.services.auth_service.User")
    def test_force_reset_password_success(self, mock_user_class, mock_bcrypt, mock_db):
        mock_user = MagicMock()
        mock_user_class.query.filter_by.return_value.first.return_value = mock_user
        mock_bcrypt.hashpw.return_value = b"newhashedpass"

        result = force_reset_password(self.email, "newpass")

        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Password reset successfully")
        mock_db.session.commit.assert_called_once()
        self.assertEqual(mock_user.password, "newhashedpass")

    @patch("backend.app.services.auth_service.User")
    def test_force_reset_password_user_not_found(self, mock_user_class):
        mock_user_class.query.filter_by.return_value.first.return_value = None

        result = force_reset_password("unknown@example.com", "newpass")

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "User not found")


if __name__ == "__main__":
    unittest.main()
