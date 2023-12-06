"""Integration test of opening fp in SAP"""
import unittest
import os
from itk_dev_shared_components.sap import sap_login, open_fp, multi_session


class IntegratonTestFp(unittest.TestCase):
    """Integration test of opening fp in SAP"""
    def setUp(self):
        sap_login.kill_sap()
        user, password = os.environ['SAP Login'].split(';')
        sap_login.login_using_cli(user, password)

    def tearDown(self):
        sap_login.kill_sap()

    def test_open_fp(self):
        """Test opening Forretnignspartneroversigt in SAP"""
        session = multi_session.get_all_sap_sessions()[0]
        test_fp = ""
        open_fp.find_forretningspartner(session, test_fp)


if __name__ == '__main__':
    unittest.main()
