"""Tests relating to the graph.mail module."""

import unittest
import json
import os
import types

from dotenv import load_dotenv

from itk_dev_shared_components.graph import authentication, mail

load_dotenv()


class EmailTest(unittest.TestCase):
    """Tests relating to the graph.mail module."""
    @classmethod
    def setUpClass(cls) -> None:
        # Get Graph credentials from the environment variables.
        credentials = json.loads(os.environ['GRAPH_API'])
        client_id = credentials['client_id']
        tenant_id = credentials['tenant_id']
        username = credentials['username']
        password = credentials['password']

        cls.graph_access = authentication.authorize_by_username_password(username, password, tenant_id=tenant_id, client_id=client_id)

        # Define mail user and folders
        cls.user = os.environ['MAIL_USER']
        cls.folder_prefix = os.environ['MAIL_FOLDER_PREFIX']
        cls.folder_count = os.environ['MAIL_FOLDER_COUNT']
        cls.folder1 = os.environ['MAIL_FOLDER1']
        cls.folder2 = os.environ['MAIL_FOLDER2']
        cls.folder_many = os.environ['MAIL_FOLDER_MANY']

    def _get_test_email(self) -> mail.Email:
        """Get the single test email from the test folder."""
        emails = mail.get_emails_from_folder(self.user, self.folder1, self.graph_access)
        self.assertNotEqual(len(emails), 0, "No emails found in test folder!")
        self.assertEqual(len(emails), 1, "More than 1 email found in test folder!")
        return emails[0]

    def test_get_emails_from_folder(self):
        """Test getting a single email from a folder and reading its subject and body."""
        email = self._get_test_email()
        self.assertEqual(email.subject, "Test subject")
        self.assertTrue(email.get_text().startswith("Test text"))

    def test_get_emails_from_folder_generator(self):
        """Test that limit=None returns a generator that yields all emails in the folder."""
        emails = mail.get_emails_from_folder(self.user, self.folder_many, self.graph_access, limit=None)
        self.assertIsInstance(emails, types.GeneratorType)

        emails = list(emails)
        self.assertEqual(len(emails), 20, "Expected exactly 20 emails in test folder!")
        # self.assertEqual(emails[0].subject, "Test subject")

    def test_get_emails_from_many_folders(self):
        """Test that getting emails works across more than 10 folders (pagination)."""
        for i in range(int(self.folder_count)):
            mail.get_emails_from_folder(self.user, f"{self.folder_prefix}{i}", self.graph_access)

    def test_list_email_attachments(self):
        """Test listing the attachments of an email."""
        email = self._get_test_email()
        attachments = mail.list_email_attachments(email, self.graph_access)
        self.assertEqual(len(attachments), 3)

        # Get attachment object 'Test document.pdf'
        attachment = next((att for att in attachments if att.name == "Test document.pdf"), None)
        self.assertIsNotNone(attachment)

    def test_get_attachment_data(self):
        """Test getting the raw data of an attachment."""
        email = self._get_test_email()
        attachments = mail.list_email_attachments(email, self.graph_access)
        attachment = next((att for att in attachments if att.name == "Test document.pdf"), None)
        self.assertIsNotNone(attachment)

        # Get attachment file and read first 4 bytes
        file = mail.get_attachment_data(attachment, self.graph_access)
        self.assertEqual(file.read(4), b'%PDF')

    def test_get_email_as_mime(self):
        """Test getting an email as a MIME file."""
        email = self._get_test_email()

        # Get email as MIME and read first 8 bytes
        file = mail.get_email_as_mime(email, self.graph_access)
        self.assertEqual(file.read(8), b'Received')

    def test_move_and_delete_email(self):
        """Test moving and deleting an email, then restoring it to the test folder.
        Delete email permanently is not tested.
        """
        email = self._get_test_email()

        # Move the email
        mail.move_email(email, self.folder2, self.graph_access)

        # Delete to deleted items folder
        mail.delete_email(email, self.graph_access)

        # Move email back
        mail.move_email(email, self.folder1, self.graph_access)

    def test_wrong_usage(self):
        """Test that raised errors actually get raised."""
        with self.assertRaises(ValueError):
            mail.get_folder_id_from_path(self.user, "Foo/Bar", self.graph_access)

        with self.assertRaises(ValueError):
            mail.get_folder_id_from_path(self.user, "Indbakke/FooBar", self.graph_access)


if __name__ == "__main__":
    unittest.main()
