'''Tests related to the Super Search Eflyt module'''

import os
import unittest

from dotenv import load_dotenv
from datetime import date

from selenium.webdriver.common.by import By
from itk_dev_shared_components.eflyt.login import login
from itk_dev_shared_components.eflyt import super_search

load_dotenv()


class SuperSearchTest(unittest.TestCase):
    """Test the Super Search functionality of Eflyt integration"""

    @classmethod
    def setUpClass(cls):
        """Setup test class"""
        eflyt_credentials = os.getenv("EFLYT_LOGIN").split(",")
        cls.browser = login(eflyt_credentials[0], eflyt_credentials[1])
        cls.browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_imgLogo").click()

    def test_lookup(self):
        """Lookup a CPR and a case and check that it is found"""
        test_cpr = os.getenv("TEST_CPR")
        test_case = os.getenv("TEST_CASE")
        from_date = date(1991, 1, 1)
        to_date = date(2024, 1, 1)

        rows = super_search.super_search(self.browser, from_date, to_date, cpr_number=test_cpr)
        self.assertGreater(len(rows), 0)

        rows = super_search.super_search(self.browser, from_date, to_date, case_number=test_case)
        self.assertEqual(len(rows), 1)

    def test_selection(self):
        """Go to the first entry"""
        super_search.select_first_entry(self.browser)


if __name__ == '__main__':
    unittest.main()
