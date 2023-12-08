"""Integration test of KMD Nova API"""
import unittest
import os
from itk_dev_shared_components.kmd_nova import api

class IntegrationTestNovaApi(unittest.TestCase):
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
        self.assertNotEqual("", self.nova.bearer_token)

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


class TestMockedRequests(unittest.TestCase):
    def test_refresh_token(self):
        # TODO mock api and ensure retry happens.
        pass

if __name__ == '__main__':
    unittest.main()
