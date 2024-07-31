'''Tests related to the Move Search Eflyt module'''

import os
import unittest
from datetime import date

from dotenv import load_dotenv

from itk_dev_shared_components.eflyt.eflyt_login import login
from itk_dev_shared_components.eflyt import eflyt_search

load_dotenv()
test_cpr = os.getenv("TEST_CPR")
test_case = os.getenv("TEST_CASE")
from_date = date(1991, 1, 1)
to_date = date(2024, 1, 1)


class MoveSearchTest(unittest.TestCase):
    '''Test the Move Search functionality of Eflyt integration'''

    @classmethod
    def setUpClass(cls):
        '''Setup test class'''
        eflyt_credentials = os.getenv("EFLYT_LOGIN").split(",")
        cls.browser = login(eflyt_credentials[0], eflyt_credentials[1])

    def test_search(self):
        '''Lookup cases and check that they are found'''
        eflyt_search.search(self.browser, from_date, to_date)

    def test_extract_cases(self):
        """Extract cases and check we found what we expected"""
        eflyt_search.search(self.browser, from_date, to_date)
        eflyt_search.extract_cases(self.browser)

    def test_open_case(self):
        """Open a case and check we moved to another view"""
        eflyt_search.open_case(self.browser, test_case)


if __name__ == '__main__':
    unittest.main()
