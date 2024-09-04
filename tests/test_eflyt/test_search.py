"""Tests related to the Eflyt Search module"""

import os
import unittest
from datetime import date, timedelta

from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from itk_dev_shared_components.eflyt.eflyt_login import login
from itk_dev_shared_components.eflyt import eflyt_search

load_dotenv()


class SearchTest(unittest.TestCase):
    """Test the Move Search functionality of Eflyt integration"""

    @classmethod
    def setUpClass(cls):
        """Setup test class"""
        eflyt_credentials = os.getenv("EFLYT_LOGIN").split(",")
        cls.browser = login(eflyt_credentials[0], eflyt_credentials[1])

    def test_extract_cases(self):
        """Extract cases and check we found what we expected"""
        eflyt_search.search(self.browser, date.today() - timedelta(days=2), date.today())
        cases = eflyt_search.extract_cases(self.browser)

        self.assertGreater(len(cases), 0)
        case = cases[0]

        self.assertIsInstance(case.case_number, str)
        self.assertIsInstance(case.case_types, list)
        self.assertIsInstance(case.deadline, (date, type(None)))
        self.assertIsInstance(case.status, (str, type(None)))
        self.assertIsInstance(case.cpr, (str, type(None)))
        self.assertIsInstance(case.name, (str, type(None)))
        self.assertIsInstance(case.case_worker, (str, type(None)))

    def test_open_case(self):
        """Open a case and check the browser opened the case view"""
        test_case = os.getenv("TEST_CASE")
        eflyt_search.open_case(self.browser, test_case)

        # Check to see the view changed
        open_case = self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_stcPersonTab1_lblMainheading").text
        self.assertTrue(test_case in open_case)


if __name__ == '__main__':
    unittest.main()
