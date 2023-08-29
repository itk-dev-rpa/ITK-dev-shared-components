import unittest
import os
import threading
from ITK_dev_shared_components.SAP import sap_login, multi_session, opret_kundekontakt

class test_multi_session(unittest.TestCase):
    def setUp(self):
        sap_login.kill_sap()
        user, password = os.environ['SAP Login'].split(';')
        sap_login.login_using_cli(user, password)

    def tearDown(self):
        sap_login.kill_sap()


    def test_spawn_sessions(self):
        with self.assertRaises(ValueError):
            multi_session.spawn_sessions(0)

        with self.assertRaises(ValueError):
            multi_session.spawn_sessions(7)    

        sessions = multi_session.spawn_sessions(1)
        self.assertEqual(len(sessions), 1)

        sessions = multi_session.spawn_sessions(6)
        self.assertEqual(len(sessions), 6)

        sessions = multi_session.get_all_SAP_sessions()
        self.assertEqual(len(sessions), 6)


    def test_run_batches(self):
        # This also tests:
            # run_batch, run_with_session, ExThread
        num_sessions = 6

        multi_session.spawn_sessions(num_sessions)
    
        #Data
        lock = threading.Lock()

        data = [
            ("25564617", None, 'Orientering', f"Hej {i}", lock) for i in range(12)
        ]

        # Test with 12 cases
        multi_session.run_batches(opret_kundekontakt.opret_kundekontakter, data, num_sessions)
        
        # Test with 5 cases
        multi_session.run_batches(opret_kundekontakt.opret_kundekontakter, data[0:5], num_sessions)

        # Test with 1 case
        multi_session.run_batches(opret_kundekontakt.opret_kundekontakter, data[0:1], num_sessions)

if __name__ == '__main__':
    unittest.main()