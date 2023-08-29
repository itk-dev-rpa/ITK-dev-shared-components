import unittest
import os
from ITK_dev_shared_components.SAP import sap_login

class test_sap_login(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sap_login.kill_sap()

    @classmethod
    def tearDownClass(cls):
        sap_login.kill_sap()
    
    def setUp(self) -> None:
        pass

    def test_login_with_cli(self):
        user, password = os.environ['SAP Login'].split(';') 
        sap_login.login_using_cli(user, password)

        sap_login.kill_sap()

        with self.assertRaises(TimeoutError):
            sap_login.login_using_cli(user, password, timeout=0)
        
        with self.assertRaises(ValueError):
            sap_login.login_using_cli("Foo", "Bar")

if __name__ == '__main__':
    unittest.main()