"""Tests relating to the module smtp.smtp_util."""

import unittest
from io import BytesIO

from itk_dev_shared_components.smtp import smtp_util
from itk_dev_shared_components.smtp.smtp_util import EmailAttachment


class TestTreeUtil(unittest.TestCase):
    """Tests relating to the module smtp.smtp_util."""

    def test_send_simple(self):
        """Test sending a simple email."""
        smtp_util.send_email("itk-rpa@mkb.aarhus.dk", "idsc@test.dk", "Test simple", "Test body")

    def test_send_html_email(self):
        """Test sending an html email."""
        html = "<html><head><style> table {font-family: arial, sans-serif; border-collapse: collapse; width: 100%;} td, th { border: 1px solid #dddddd; text-align: left; padding: 8px;}</style></head><body><h2>HTML Table</h2><table><tr><th>Company</th><th>Contact</th><th>Country</th></tr><tr><td>Alfreds Futterkiste</td><td>Maria Anders</td><td>Germany</td></tr><tr><td>Centro comercial Moctezuma</td><td>Francisco Chang</td><td>Mexico</td></tr></table></body></html>"
        smtp_util.send_email("itk-rpa@mkb.aarhus.dk", "idsc@test.dk", "Test html", html, html_body=True)

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

        smtp_util.send_email("itk-rpa@mkb.aarhus.dk", "idsc@test.dk", "Test files", "This email has three attached txt files.", attachments=attachments)

    def test_send_multiple(self):
        """Test sending to multiple receivers."""
        smtp_util.send_email(["itk-rpa@mkb.aarhus.dk", "itk-rpa@mkb.aarhus.dk"], "idsc@test.dk", "Test multiple", "This email has multiple receivers.")


if __name__ == '__main__':
    unittest.main()
