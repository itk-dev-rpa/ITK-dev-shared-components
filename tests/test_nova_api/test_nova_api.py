"""Integration test of KMD Nova API"""
import unittest
import os
from itk_dev_shared_components.kmd_nova import api


class IntegrationTestNovaApi(unittest.TestCase):
    """Integration test of KMD Nova API"""
    def setUp(self):
        credentials = os.getenv('nova_api_credentials')
        credentials = credentials.split(',')
        nova = api.NovaESDH(client_id=credentials[0], client_secret=credentials[1])
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
        cpr = "6101009805"
        case_title = "Meget_Unik_Case_Overskrift"
        case_number = "S2023-61078"

        def assert_case(cases_response: dict):
            self.assertIn('cases', cases_response)
            self.assertEqual(len(cases_response['cases']), 1)
            self.assertEqual(cases_response['cases'][0]['caseParties'][0]['identification'], cpr)
            self.assertEqual(cases_response['cases'][0]['caseAttributes']['userFriendlyCaseNumber'], case_number)
            self.assertEqual(cases_response['cases'][0]['caseAttributes']['title'], case_title)

        cases_response = self.nova.get_cases(cpr=cpr)
        assert_case(cases_response)

        cases_response = self.nova.get_cases(case_number=case_number)
        assert_case(cases_response)

        cases_response = self.nova.get_cases(case_title=case_title)
        assert_case(cases_response)

        cases_response = self.nova.get_cases(cpr=cpr, case_title=case_title)
        assert_case(cases_response)

        cases_response = self.nova.get_cases(cpr=cpr, case_number=case_number)
        assert_case(cases_response)

        with self.assertRaises(ValueError):
            self.nova.get_cases()


if __name__ == '__main__':
    unittest.main()
