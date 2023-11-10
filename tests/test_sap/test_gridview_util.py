"""Tests relating to the module SAP.gridview_util."""

import unittest
import os
from itk_dev_shared_components.sap import gridview_util, sap_login, multi_session

class TestGridviewUtil(unittest.TestCase):
    """Tests relating to the module SAP.gridview_util."""
    @classmethod
    def setUpClass(cls):
        """Launch SAP and navigate to fmcacov on FP 25564617 (Test person)."""
        sap_login.kill_sap()

        user, password = os.environ['SAP Login'].split(';')
        sap_login.login_using_cli(user, password)
        session = multi_session.get_all_sap_sessions()[0]
        session.startTransaction("fmcacov")
        session.findById("wnd[0]/usr/ctxtGPART_DYN").text = "25564617"
        session.findById("wnd[0]").sendVKey(0)

    @classmethod
    def tearDownClass(cls):
        sap_login.kill_sap()

    def setUp(self) -> None:
        # Find SAP gridview (table) object for testing
        session = multi_session.get_all_sap_sessions()[0]
        self.table = session.findById("wnd[0]/usr/tabsDATA_DISP/tabpDATA_DISP_FC1/ssubDATA_DISP_SCA:RFMCA_COV:0202/cntlRFMCA_COV_0100_CONT5/shellcont/shell")

    def test_scroll_entire_table(self):
        """Test scroll_entire_table. Assume success if no errors."""
        gridview_util.scroll_entire_table(self.table)
        gridview_util.scroll_entire_table(self.table, True)

    def test_get_all_rows(self):
        """Test get all rows of table. 
        Assume success if any rows and columns are loaded.
        """
        result = gridview_util.get_all_rows(self.table)
        self.assertGreater(len(result), 0)
        self.assertGreater(len(result[0]), 0)

    def test_get_row(self):
        """Test getting a single row.
        Assume success if any columns are loaded.
        """
        result = gridview_util.get_row(self.table, 0, False)
        self.assertGreater(len(result), 0)

        result = gridview_util.get_row(self.table, 0, True)
        self.assertGreater(len(result), 0)

    def test_iterate_rows(self):
        """Test iterating through all rows.
        Assume success if any columns are loaded for each row.
        """
        for row in gridview_util.iterate_rows(self.table):
            self.assertGreater(len(row), 0)

    def test_get_column_titles(self):
        """Test getting column titles.
        Assume success if any titles are loaded.
        """
        result = gridview_util.get_column_titles(self.table)
        self.assertGreater(len(result), 0)

    def test_find_row_index_by_value(self):
        """Test finding a single row by column value."""
        # Test finding an actual value.
        index = gridview_util.find_row_index_by_value(self.table, "TXTU2", "Test Deltrans")
        self.assertNotEqual(index, -1)

        # Test NOT finding a wrong value.
        index = gridview_util.find_row_index_by_value(self.table, "TXTU2", "Foo")
        self.assertEqual(index, -1)

        # Test error on wrong column name.
        with self.assertRaises(ValueError):
            gridview_util.find_row_index_by_value(self.table, "Foo", "Bar")

    def test_find_all_row_indices_by_value(self):
        """Test finding all rows by column value."""
        # Test finding an actual value.
        indices = gridview_util.find_all_row_indices_by_value(self.table, "TXTU2", "Gebyr")
        self.assertGreater(len(indices), 0)

        # Test NOT finding a wrong value.
        indices = gridview_util.find_all_row_indices_by_value(self.table, "TXTU2", "Foo")
        self.assertEqual(len(indices), 0)

        # Test error on wrong column name.
        with self.assertRaises(ValueError):
            gridview_util.find_all_row_indices_by_value(self.table, "Foo", "Bar")
