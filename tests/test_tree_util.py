import unittest
import os
from ITK_dev_shared_components.SAP import tree_util, sap_login, multi_session

class test_tree_util(unittest.TestCase):
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

    
    def test_get_node_key_by_text(self):
        session = multi_session.get_all_SAP_sessions()[0]
        tree = session.findById("wnd[0]/shellcont/shell")

        result = tree_util.get_node_key_by_text(tree, "25564617")
        self.assertEqual(result, "GP0000000001")

        result = tree_util.get_node_key_by_text(tree, "556461", True)
        self.assertEqual(result, "GP0000000001")

        with self.assertRaises(ValueError):
            tree_util.get_node_key_by_text(tree, "Foo Bar")
        
        with self.assertRaises(ValueError):
            tree_util.get_node_key_by_text(tree, "Foo Bar", True)
    

    def test_get_item_by_text(self):
        session = multi_session.get_all_SAP_sessions()[0]
        tree = session.findById("wnd[0]/shellcont/shell")

        result = tree_util.get_item_by_text(tree, "25564617")
        self.assertEqual(result, ("GP0000000001", "Column1"))

        result = tree_util.get_item_by_text(tree, "556461", True)
        self.assertEqual(result, ("GP0000000001", "Column1"))

        with self.assertRaises(ValueError):
            tree_util.get_item_by_text(tree, "Foo Bar")

        with self.assertRaises(ValueError):
            tree_util.get_item_by_text(tree, "Foo Bar", True)
    

    def test_check_uncheck_all_check_boxes(self):
        session = multi_session.get_all_SAP_sessions()[0]
        session.findById("wnd[0]/shellcont/shell").nodeContextMenu("GP0000000001")
        session.findById("wnd[0]/shellcont/shell").selectContextMenuItem("FLERE")
        tree = session.findById("wnd[1]/usr/cntlCONTAINER_PSOBKEY/shellcont/shell/shellcont[1]/shell[1]")

        # Test in different orders
        tree_util.check_all_check_boxes(tree)
        tree_util.uncheck_all_check_boxes(tree)
        tree_util.uncheck_all_check_boxes(tree)
        tree_util.check_all_check_boxes(tree)
        tree_util.check_all_check_boxes(tree)

        session.findById("wnd[1]/usr/cntlCONTAINER_PSOBKEY/shellcont/shell/shellcont[1]/shell[0]").pressButton("CANCEL")

        # Test on tree without checkboxes
        tree = session.findById("wnd[0]/shellcont/shell")
        tree_util.check_all_check_boxes(tree)
        tree_util.uncheck_all_check_boxes(tree)


if __name__ == '__main__':
    unittest.main()