"""Tests relating to the module smtp.smtp_util."""

import unittest
from io import BytesIO
import os

import requests

from itk_dev_shared_components.smtp import smtp_util
from itk_dev_shared_components.smtp.smtp_util import EmailAttachment


class TestTreeUtil(unittest.TestCase):
    """Tests relating to the module smtp.smtp_util."""
    smtp_server = os.getenv("mailpit_host", "localhost")
    smtp_port = os.getenv("mailpit_smtp_port", "1025")
    http_port = os.getenv("mailpit_http_port", "8025")

    def setUp(self) -> None:
        url = url = f"http://localhost:{self.http_port}/api/v1/messages"
        response = requests.delete(url, timeout=2)
        response.raise_for_status()

    def test_send_simple(self):
        """Test sending a simple email."""
        smtp_util.send_email("test@receiver.com", "idsc@test.dk", "Test simple", "Test body", smtp_server=self.smtp_server, smtp_port=self.smtp_port)

        message = self.get_message("Test simple")
        self.assertEqual(message["From"]["Address"], "idsc@test.dk")
        self.assertEqual(message["To"][0]["Address"], "test@receiver.com")
        self.assertEqual(message["Snippet"], "Test body")

    def test_send_html(self):
        """Test sending an html email."""
        html = "<html><head><style> table {font-family: arial, sans-serif; border-collapse: collapse; width: 100%;} td, th { border: 1px solid #dddddd; text-align: left; padding: 8px;}</style></head><body><h2>HTML Table</h2><table><tr><th>Company</th><th>Contact</th><th>Country</th></tr><tr><td>Alfreds Futterkiste</td><td>Maria Anders</td><td>Germany</td></tr><tr><td>Centro comercial Moctezuma</td><td>Francisco Chang</td><td>Mexico</td></tr></table></body></html>"
        smtp_util.send_email("test@receiver.com", "idsc@test.dk", "Test html", html, html_body=True, smtp_server=self.smtp_server, smtp_port=self.smtp_port)

        message = self.get_message("Test html")
        self.assertTrue(message["Snippet"].startswith("HTML Table"))

    def test_send_attachments(self):
        """Test sending an email with multiple attachments."""
        attachments = []

        # Generate some attachment files
        for i in range(3):
            file = BytesIO(b"Hello"*(i+1))
            file_name = f"file{i}.txt"

            attachments.append(
                EmailAttachment(file, file_name)
            )

        smtp_util.send_email("test@receiver.com", "idsc@test.dk", "Test files", "This email has three attached txt files.", attachments=attachments, smtp_server=self.smtp_server, smtp_port=self.smtp_port)

        message = self.get_message("Test files")
        self.assertEqual(message["Attachments"], 3)

    def test_send_multiple(self):
        """Test sending to multiple receivers."""
        smtp_util.send_email(["test@receiver.com", "test@receiver.com"], "idsc@test.dk", "Test multiple", "This email has multiple receivers.", smtp_server=self.smtp_server, smtp_port=self.smtp_port)

        message = self.get_message("Test multiple")
        self.assertEqual(len(message["To"]), 2)

    def get_message(self, subject: str):
        """Get a message from the Mailpit api with the given subject.
        https://mailpit.axllent.org/docs/api-v1/view.html#tag--messages

        Args:
            subject: The email subject to search for.

        Returns:
            A dict representing the message from Mailpit.
        """
        url = f"http://localhost:{self.http_port}/api/v1/messages"
        response = requests.get(url, timeout=2).json()

        message = None
        for msg in response["messages"]:
            if msg["Subject"] == subject:
                message = msg
                break

        self.assertIsNotNone(message)
        return message


if __name__ == '__main__':
    unittest.main()
