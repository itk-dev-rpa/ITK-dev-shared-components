'''Tests related to the Move Search Eflyt module'''

import os
import unittest

from dotenv import load_dotenv

from itk_dev_shared_components.eflyt.login import login

load_dotenv()


class MoveSearchTest(unittest.TestCase):
    '''Test the Move Search functionality of Eflyt integration'''

    @classmethod
    def setUpClass(cls):
        '''Setup test class'''
        eflyt_credentials = os.getenv("EFLYT_LOGIN").split(",")
        cls.browser = login(eflyt_credentials[0], eflyt_credentials[1])

    def test_lookup(self):
        '''Lookup a CPR and check that it is found'''
