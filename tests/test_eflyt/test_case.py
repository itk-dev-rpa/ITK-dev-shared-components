'''Tests related to the Case module'''

import os
import unittest

from dotenv import load_dotenv

from itk_dev_shared_components.eflyt.login import login

load_dotenv()


class CaseTest(unittest.TestCase):
    '''Test the Case functionality of Eflyt integration'''

    @classmethod
    def setUpClass(cls):
        '''Setup test class'''
        eflyt_credentials = os.getenv("EFLYT_LOGIN").split(",")
        cls.browser = login(eflyt_credentials[0], eflyt_credentials[1])
        cls.browser.find_element()

    def test_find_data(self):
        '''Look for data and verify format'''
