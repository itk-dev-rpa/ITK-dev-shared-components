'''Tests related to the Super Search Eflyt module'''

import unittest


class SuperSearchTest(unittest.testcase):
    '''Test the Super Search functionality of Eflyt integration'''

    def test_lookup(self):
        '''Lookup a CPR and check that it is found'''
