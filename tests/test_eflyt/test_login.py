'''Tests related to login in Eflyt'''

import os
import unittest

from dotenv import load_dotenv

from itk_dev_shared_components.eflyt.login import login

load_dotenv()


class LoginTest(unittest.TestCase):
    '''Test login functionality in the Eflyt module'''

    def test_login(self):
        '''Test to see if we can login'''
        eflyt_credentials = os.getenv("EFLYT_LOGIN")

        # Test login
        login(eflyt_credentials[0], eflyt_credentials[1])

        # Test login runtime error
        with self.assertRaises(RuntimeError):
            login("foo", "bar")


if __name__ == '__main__':
    unittest.main()
