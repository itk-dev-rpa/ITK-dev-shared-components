import unittest
import os
from ITK_dev_shared_components.SAP import gridview_util, sap_login, multi_session

class test_gridview_util(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        user, password = os.environ['SAP Login'].split(';')
        sap_login.login_using_cli(user, password)
        session = multi_session.get_all_SAP_sessions()[0]
        session.startTransaction("fmcacov")
        session.findById("wnd[0]/usr/ctxtGPART_DYN").text = "25564617"
        session.findById("wnd[0]").sendVKey(0)   

    @classmethod
    def tearDownClass(cls):
        sap_login.kill_sap()
    
    def setUp(self) -> None:
        session = multi_session.get_all_SAP_sessions()[0]
        self.table = session.findById("wnd[0]/usr/tabsDATA_DISP/tabpDATA_DISP_FC1/ssubDATA_DISP_SCA:RFMCA_COV:0202/cntlRFMCA_COV_0100_CONT5/shellcont/shell")

    def test_scroll_entire_table(self):
        gridview_util.scroll_entire_table(self.table)
        gridview_util.scroll_entire_table(self.table, True)

    def test_get_all_rows(self):
        result = gridview_util.get_all_rows(self.table)
        self.assertGreater(len(result), 0)
        self.assertGreater(len(result[0]), 0)
    
    def test_get_row(self):
        result = gridview_util.get_row(self.table, 0, False)
        self.assertGreater(len(result), 0)

        result = gridview_util.get_row(self.table, 0, True)
        self.assertGreater(len(result), 0)
    
    def test_iterate_rows(self):
        for row in gridview_util.iterate_rows(self.table):
            self.assertGreater(len(row), 0)
    
    def test_get_column_titles(self):
        result = gridview_util.get_column_titles(self.table)
        self.assertGreater(len(result), 0)
    
    def test_find_row_index_by_value(self):
        result = gridview_util.find_row_index_by_value(self.table, "TXTU2", "Test Deltrans")
        self.assertNotEqual(result, -1)

        result = gridview_util.find_row_index_by_value(self.table, "TXTU2", "Foo")
        self.assertEqual(result, -1)

        with self.assertRaises(ValueError):
            gridview_util.find_row_index_by_value(self.table, "Foo", "Bar")


    def test_find_all_row_indecies_by_value(self):
        result = gridview_util.find_all_row_indecies_by_value(self.table, "TXTU2", "Gebyr")
        self.assertGreater(len(result), 0)

        result = gridview_util.find_all_row_indecies_by_value(self.table, "TXTU2", "Foo")
        self.assertEqual(len(result), 0)

        with self.assertRaises(ValueError):
            gridview_util.find_all_row_indecies_by_value(self.table, "Foo", "Bar")
    



        


if __name__ == '__main__':
    unittest.main()