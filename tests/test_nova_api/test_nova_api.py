"""Integration test of KMD Nova API"""
import unittest
import os

from itk_dev_shared_components.kmd_nova.api import NovaESDH
from itk_dev_shared_components.kmd_nova.nova_objects import NovaCase


class IntegrationTestNovaApi(unittest.TestCase):
    """Integration test of KMD Nova API"""
    def setUp(self):
        credentials = os.getenv('nova_api_credentials')
        credentials = credentials.split(',')
        nova = NovaESDH(client_id=credentials[0], client_secret=credentials[1])
        self.nova = nova

    def test_endpoint(self):
        """Integration test of the API.
        Add the API credentials to your environment variables before running this test.
        nova_api_credentials: "<client_id>,<client_secret>"

        The test attempts to obtain a bearer token.
        """
        self.assertNotEqual("", self.nova.get_bearer_token())

    @unittest.skip("Needs test data")
    def test_get_address(self):
        """Test the API for getting an address.
        Enter a valid CPR and assert the response.
        Expects response of this layout
        {
            "address":
            {
                "addressLine1": "<name>",
                "addressLine2": "<road>",
                "addressLine3": "<city>"
            },
            "name": "<name>"
        }
        """
        cpr = ""
        address_response = self.nova.get_address_by_cpr(cpr)

        self.assertTrue('name' in address_response)
        self.assertTrue('address' in address_response)

    def test_get_cases(self):
        """
        Test the API for getting cases on a given case number.
        """
        cpr = "8412893981"
        case_title = "Meget_Unik_Case_Overskrift"
        case_number = "S2023-61078"

        def assert_cases(cases: list[NovaCase]):
            self.assertEqual(len(cases), 1)
            self.assertIsInstance(cases[0], NovaCase)
            self.assertEqual(cases[0].case_parties[0].identification, cpr)
            self.assertEqual(cases[0].case_number, case_number)
            self.assertEqual(cases[0].title, case_title)

        cases = self.nova.get_cases(cpr=cpr)
        assert_cases(cases)

        cases = self.nova.get_cases(case_number=case_number)
        assert_cases(cases)

        cases = self.nova.get_cases(case_title=case_title)
        assert_cases(cases)

        cases = self.nova.get_cases(cpr=cpr, case_title=case_title)
        assert_cases(cases)

        cases = self.nova.get_cases(cpr=cpr, case_number=case_number)
        assert_cases(cases)

        cases = self.nova.get_cases(case_number=case_number, case_title=case_title)
        assert_cases(cases)

        with self.assertRaises(ValueError):
            self.nova.get_cases()


if __name__ == '__main__':
    unittest.main()
