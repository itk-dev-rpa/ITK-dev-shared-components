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
        html = """
        <html>
            <body>

            <h2>HTML Table</h2>

            <table>
                <tr>
                    <th>Company</th>
                    <th>Contact</th>
                    <th>Country</th>
                </tr>
                <tr>
                    <td>Alfreds Futterkiste</td>
                    <td>Maria Anders</td>
                    <td>Germany</td>
                </tr>
            </table>

            </body>
        </html>"""
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

        smtp_util.send_email("itk-rpa@mkb.aarhus.dk", "idsc@test.dk", "Test files", "Three attached txt files.", attachments=attachments)


if __name__ == '__main__':
    unittest.main()
