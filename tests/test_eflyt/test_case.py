"""Tests related to the Case module"""

import os
import unittest

from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from itk_dev_shared_components.eflyt.eflyt_login import login
from itk_dev_shared_components.eflyt.eflyt_search import open_case
from itk_dev_shared_components.eflyt import eflyt_case

load_dotenv()
test_cpr = os.getenv("TEST_CPR")
test_case = os.getenv("TEST_CASE")


class CaseTest(unittest.TestCase):
    """Test the Case functionality of Eflyt integration"""

    @classmethod
    def setUpClass(cls):
        """Setup test class"""
        eflyt_credentials = os.getenv("EFLYT_LOGIN").split(",")
        cls.browser = login(eflyt_credentials[0], eflyt_credentials[1])

    def setUp(self):
        """Go to a clean case state"""
        open_case(self.browser, test_case)

    def test_get_beboere(self):
        """Test inhabitant functions"""
        inhabitants = eflyt_case.get_beboere(self.browser)
        self.assertGreater(len(inhabitants), 0, "No inhabitants found on address")

    def test_get_applicants(self):
        """Get list of applicants and make sure they match expected value"""
        applicants = eflyt_case.get_applicants(self.browser)
        found_expected = any(applicant.cpr == test_cpr for applicant in applicants)
        self.assertTrue(found_expected, f"Applicant {test_cpr} not found among case applicants. Make sure your .env is setup correctly with a case matching the test cpr")

    def test_change_tab(self):
        """Change tab and check the view changed"""
        eflyt_case.change_tab(self.browser, 1)
        self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_becPersonTab_GridViewBeboere")

    def test_get_room_count(self):
        """Get room count and check it matches the expected value"""
        room_count = eflyt_case.get_room_count(self.browser)
        self.assertIsInstance(room_count, int, "Room count is not a number")
        self.assertGreater(room_count, 0, "Room count is less than 1")


if __name__ == '__main__':
    unittest.main()
