"""Tests relating to the module SAP.fmcacov."""

import unittest
import os

from dotenv import load_dotenv

from itk_dev_shared_components.sap import fmcacov, sap_login, multi_session

load_dotenv()

# Some tests might look similar, and we want this. pylint: disable=duplicate-code


class TestFmcacov(unittest.TestCase):
    """Tests relating to the module SAP.fmcacov."""
    @classmethod
    def setUpClass(cls):
        """Launch SAP and get the main session."""
        sap_login.kill_sap()

        user, password = os.environ['SAP_LOGIN'].split(';')
        sap_login.login_using_cli(user, password)

        cls.session = multi_session.get_all_sap_sessions()[0]

    @classmethod
    def tearDownClass(cls):
        sap_login.kill_sap()

    def test_find_forretningspartner(self):
        """Find a test-person in fmcacov and check cpr and name.
        To properly test it the fp needs to match a cvr number, but that doesn't exist
        as test data.
        """
        fmcacov.open_forretningspartner(self.session, "25564617")

        cpr = self.session.findById("wnd[0]/usr/txtZDKD_BP_NUM").text
        self.assertEqual(cpr, '841289-3981')

        name = self.session.findById("wnd[0]/usr/subHEAD_DATA_SUBSCREEN:SAPLZDKD_SUBSCREENS:0100/txtBUS000FLDS-DESCRIP").text
        self.assertEqual(name, 'Testbruger Et')

        # Go back to home screen.
        self.session.findById("wnd[0]/tbar[0]/btn[12]").press()

    def test_dismiss_key_popup(self):
        """Try to find 'afstemningsnøgle'-popup and dismiss it.
        The popup only appears once a day after midnight.
        """
        fmcacov.dismiss_key_popup(self.session)


if __name__ == '__main__':
    unittest.main()
