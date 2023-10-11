"""Tests relating to the module SAP.sap_login."""

import unittest
from tkinter import simpledialog

from ITK_dev_shared_components.SAP import sap_login

class TestSapLogin(unittest.TestCase):
    """Tests relating to the module SAP.sap_login."""

    @classmethod
    def setUpClass(cls) -> None:
        """Show popups that asks for username, password and new password
        used in the following tests.
        """
        cls.username = simpledialog.askstring("Enter username", "Enter the SAP username to be used in tests.")
        cls.password = simpledialog.askstring("Enter password", "Enter the SAP password to be used in tests.")
        cls.new_password = simpledialog.askstring("Enter password", "Enter the new password to be used in tests.\nRemember to write down the new password!\nLeave empty to skip test_change_password.")

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
        If no new_password is entered in the setup
        """
        if not self.new_password:
            raise ValueError("Test not run because new_password was missing.")

        sap_login.change_password(self.username, self.password, self.new_password)
        self.password = self.new_password

        with self.assertRaises(ValueError):
            sap_login.change_password(self.username, "Foo", self.new_password)

        with self.assertRaises(ValueError):
            sap_login.change_password(self.username, self.password, "")


if __name__ == '__main__':
    unittest.main()
