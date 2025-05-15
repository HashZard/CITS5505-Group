import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# 确保项目根目录在导入路径中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from backend.app.services.user_service import (
    get_user_profile,
    update_user_profile,
    send_message,
    get_inbox_messages
)


class TestUserService(unittest.TestCase):

    def setUp(self):
        self.user_id = 1
        self.receiver_email = "user2@example.com"
        self.sender_id = 99
        self.message_content = "Hello!"

    @patch("backend.app.services.user_service.User")
    def test_get_user_profile_success(self, mock_user_class):
        mock_user = MagicMock()
        mock_user.id = self.user_id
        mock_user.name = "Alice"
        mock_user.department = "CS"
        mock_user.email = "alice@example.com"
        mock_user.field = "AI"
        mock_user.favourite_courses = [
            MagicMock(id=1, code="CS101", name="Intro to CS"),
            MagicMock(id=2, code="CS102", name="Data Structures")
        ]
        mock_user_class.query.get.return_value = mock_user

        success, data = get_user_profile(self.user_id)
        self.assertTrue(success)
        self.assertEqual(data["name"], "Alice")
        self.assertEqual(len(data["favourite_courses"]), 2)

    @patch("backend.app.services.user_service.User")
    def test_get_user_profile_not_found(self, mock_user_class):
        mock_user_class.query.get.return_value = None
        success, msg = get_user_profile(999)
        self.assertFalse(success)
        self.assertEqual(msg, "User not found")

    @patch("backend.app.services.user_service.save_user")
    @patch("backend.app.services.user_service.get_user_by_id")
    def test_update_user_profile_success(self, mock_get_user, mock_save_user):
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user

        success, error = update_user_profile(self.user_id, "Bob", "Math")
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(mock_user.name, "Bob")
        self.assertEqual(mock_user.department, "Math")
        mock_save_user.assert_called_once_with(mock_user)

    @patch("backend.app.services.user_service.get_user_by_id")
    def test_update_user_profile_user_not_found(self, mock_get_user):
        mock_get_user.return_value = None
        success, msg = update_user_profile(999, "Name", "Dept")
        self.assertFalse(success)
        self.assertEqual(msg, "User not found")

    @patch("backend.app.services.user_service.get_user_by_id")
    def test_update_user_profile_exception(self, mock_get_user):
        mock_get_user.side_effect = Exception("DB error")
        success, msg = update_user_profile(self.user_id, "X", "Y")
        self.assertFalse(success)
        self.assertEqual(msg, "DB error")

    @patch("backend.app.services.user_service.db")
    @patch("backend.app.services.user_service.User")
    @patch("backend.app.services.user_service.Message")
    def test_send_message_success(self, mock_message_class, mock_user_class, mock_db):
        mock_receiver = MagicMock(id=2)
        mock_user_class.query.filter_by.return_value.first.return_value = mock_receiver

        mock_message_instance = MagicMock(id=123)
        mock_message_class.return_value = mock_message_instance

        success, msg_id = send_message(self.sender_id, self.receiver_email, self.message_content)
        self.assertTrue(success)
        self.assertEqual(msg_id, 123)
        mock_db.session.add.assert_called_once()
        mock_db.session.commit.assert_called_once()

    @patch("backend.app.services.user_service.User")
    def test_send_message_empty_content(self, mock_user_class):
        success, msg = send_message(self.sender_id, self.receiver_email, "   ")
        self.assertFalse(success)
        self.assertEqual(msg, "Message content cannot be empty")

    @patch("backend.app.services.user_service.User")
    def test_send_message_receiver_not_found(self, mock_user_class):
        mock_user_class.query.filter_by.return_value.first.return_value = None
        success, msg = send_message(self.sender_id, "noone@example.com", "Hi")
        self.assertFalse(success)
        self.assertEqual(msg, "Receiver not found")

    @patch("backend.app.services.user_service.Message")
    def test_get_inbox_messages_success(self, mock_message_class):
        mock_msg1 = MagicMock(
            id=1,
            sender=MagicMock(email="sender1@example.com"),
            content="Msg 1",
            created_gmt=MagicMock(strftime=lambda fmt: "2024-05-01 10:00"),
            is_read=False
        )
        mock_msg2 = MagicMock(
            id=2,
            sender=MagicMock(email="sender2@example.com"),
            content="Msg 2",
            created_gmt=MagicMock(strftime=lambda fmt: "2024-05-02 14:30"),
            is_read=True
        )

        mock_query = MagicMock()
        mock_query.filter_by.return_value.order_by.return_value.all.return_value = [mock_msg1, mock_msg2]
        mock_message_class.query = mock_query

        result = get_inbox_messages(self.user_id)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["sender"], "sender1@example.com")
        self.assertEqual(result[1]["is_read"], True)


if __name__ == "__main__":
    unittest.main()
