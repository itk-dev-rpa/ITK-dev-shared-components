"""Tests related to the Case module"""

import os
import unittest
from datetime import date

from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from itk_dev_shared_components.eflyt import eflyt_case, eflyt_login, eflyt_search

load_dotenv()


class CaseTest(unittest.TestCase):
    """Test the Case functionality of Eflyt integration"""

    @classmethod
    def setUpClass(cls):
        """Setup test class"""
        eflyt_credentials = os.getenv("EFLYT_LOGIN").split(",")
        cls.browser = eflyt_login.login(eflyt_credentials[0], eflyt_credentials[1])

    def setUp(self):
        """Go to a clean case state"""
        test_case = os.getenv("TEST_CASE")
        eflyt_search.open_case(self.browser, test_case)

    def test_get_beboere(self):
        """Test inhabitant functions"""

        inhabitants = eflyt_case.get_beboere(self.browser)
        test_no_inhabitants_case = os.getenv("TEST_CASE_NOONE")

        self.assertGreater(len(inhabitants), 0, "No inhabitants found on address")
        inhabitant = inhabitants[0]
        self.assertRegex(inhabitant.cpr, "\\d{10}")
        self.assertIsInstance(inhabitant.move_in_date, date)
        self.assertIsInstance(inhabitant.relations, list)
        self.assertIsInstance(inhabitant.name, str)

        for relation in inhabitant.relations:
            self.assertRegex(relation, r"\d{6}-\d{4}")

        eflyt_search.open_case(self.browser, test_no_inhabitants_case)
        inhabitants = eflyt_case.get_beboere(self.browser)

        self.assertEqual(len(inhabitants), 0, "Some inhabitants found when none was expected")

    def test_get_applicants(self):
        """Get list of applicants and make sure they match expected value"""

        applicants = eflyt_case.get_applicants(self.browser)
        test_cpr = os.getenv("TEST_CPR")
        found_expected = any(applicant.cpr == test_cpr for applicant in applicants)

        self.assertTrue(found_expected, f"Applicant {test_cpr} not found among case applicants. Make sure your .env is setup correctly with a case matching the test cpr")
        self.assertIsInstance(applicants[0].name, str)
        self.assertRegex(applicants[0].cpr, "\\d{10}")

    def test_change_tab(self):
        """Change tab and check the view changed"""

        # Change tab to beboer tab
        eflyt_case.change_tab(self.browser, 1)
        self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_becPersonTab_GridViewBeboere")

    def test_get_room_count(self):
        """Get room count and check it matches the expected value"""
        room_count = eflyt_case.get_room_count(self.browser)

        self.assertIsInstance(room_count, int, "Room count is not a number")
        self.assertGreater(room_count, 0, "Room count is less than 1")

    def test_write_note(self):
        """Test writing a note to a case. Check if the note is added and that the existing note is preserved.
        """
        existing_note = eflyt_case.get_note_text(self.browser)

        note_text = "Test"
        eflyt_case.add_note(self.browser, note_text)

        new_note = eflyt_case.get_note_text(self.browser)

        # Reset note to original text
        self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_ncPersonTab_ButtonVisOpdater").click()
        self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_ncPersonTab_txtVisOpdaterNote").clear()
        self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_ncPersonTab_txtVisOpdaterNote").send_keys(existing_note)
        self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_ncPersonTab_btnLongNoteUpdater").click()

        self.assertNotEqual(existing_note, new_note)
        self.assertEqual(existing_note, new_note[:len(existing_note)])
        self.assertEqual(note_text, new_note[-len(note_text):])

    @unittest.skip("No test system available for approving dummy cases.")
    def test_approve_case(self):
        """Empty test for approve_case"""


if __name__ == '__main__':
    unittest.main()
