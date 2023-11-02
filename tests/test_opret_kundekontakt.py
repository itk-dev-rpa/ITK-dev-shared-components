"""Test relating to the module SAP.opret_kundekontakt."""

import unittest
import os
from ITK_dev_shared_components.SAP import sap_login, multi_session, opret_kundekontakt

class TestOpretKundekontakt(unittest.TestCase):
    """Test relating to the module SAP.opret_kundekontakt."""
    def setUp(self):
        sap_login.kill_sap()
        user, password = os.environ['SAP Login'].split(';')
        sap_login.login_using_cli(user, password)

    def tearDown(self):
        sap_login.kill_sap()


    def test_opret_kundekontakt(self):
        """Test the function opret_kundekontakter."""
        fp = "25564617"  # TODO find aftaler i SAP og hard code her
        aftaler = ("2544577", "1990437", "1473781")

        session = multi_session.get_all_SAP_sessions()[0]

        # Test with 3 aftaler
        opret_kundekontakt.opret_kundekontakter(session, fp, aftaler, 'Orientering', "Test 1")

        # Test with 1 aftale
        opret_kundekontakt.opret_kundekontakter(session, fp, aftaler[0:1], 'Automatisk', "Test 2")

        # Test with 0 aftaler
        opret_kundekontakt.opret_kundekontakter(session, fp, None, 'Returpost', "Test 3")


if __name__ == '__main__':
    unittest.main()
