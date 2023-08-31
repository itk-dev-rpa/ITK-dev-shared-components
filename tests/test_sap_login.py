import unittest
import time
import os
from ITK_dev_shared_components.SAP import sap_login

class test_sap_login(unittest.TestCase):
    def setUp(self) -> None:
        sap_login.kill_sap()
    
    def tearDown(self) -> None:
        sap_login.kill_sap()

    def test_login_with_cli(self):
        user, password = os.environ['SAP Login'].split(';') 
        sap_login.login_using_cli(user, password)

        sap_login.kill_sap()

        with self.assertRaises(ValueError):
            sap_login.login_using_cli("Foo", "Bar")
    

    @unittest.skip("Should be run manually")
    def test_change_password(self):
        username = "az12345"
        password = "Hunter2"
        new_password = "Hunter3"

        sap_login.change_password(username, password, new_password)
        
        with self.assertRaises(ValueError):
            sap_login.change_password(username, "Foo", new_password)

        with self.assertRaises(ValueError):
            sap_login.change_password(username, password, "")


if __name__ == '__main__':
    unittest.main()