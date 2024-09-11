"""Tests relating to the module SAP.sap_login."""

import os
import unittest

from dotenv import load_dotenv, set_key

from itk_dev_shared_components.sap import sap_login

load_dotenv()


class TestSapLogin(unittest.TestCase):
    """Tests relating to the module SAP.sap_login."""

    @classmethod
    def setUpClass(cls) -> None:
        """Show popups that asks for username, password and new password
        used in the following tests.
        """
        cls.username, cls.password = os.environ['SAP_LOGIN'].split(';')

    def setUp(self) -> None:
        sap_login.kill_sap()

    def tearDown(self) -> None:
        sap_login.kill_sap()

    def test_login_with_cli(self):
        """Test login using the SAP cli interface.
        Username and password is found in a environment variable.
        """
        sap_login.login_using_cli(self.username, self.password)

        sap_login.kill_sap()

        with self.assertRaises(ValueError):
            sap_login.login_using_cli("Foo", "Bar")

    def test_change_password(self):
        """Test the function change password.
        Due to a limit in SAP you can only run this function once per day.
        If no new_password is entered in the setup, test is skipped.
        """
        new_password = os.getenv('SAP_NEW_PASSWORD')
        if not new_password:
            raise unittest.SkipTest("Test skipped because SAP_NEW_PASSWORD was missing.")

        sap_login.change_password(self.username, self.password, new_password)

        # Change password for all coming tests
        self.password = new_password
        set_key(".env", 'SAP_LOGIN', f"{self.username};{self.password}")
        set_key(".env", 'SAP_NEW_PASSWORD', '')

        with self.assertRaises(ValueError):
            sap_login.change_password(self.username, "Foo", new_password)

        with self.assertRaises(ValueError):
            sap_login.change_password(self.username, self.password, "")


if __name__ == '__main__':
    unittest.main()
