"""Integration test of KMD Nova API"""
import unittest
import os

from dotenv import load_dotenv

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess

load_dotenv()


class NovaAuthTest(unittest.TestCase):
    """Test authentication against the Nova API."""

    def test_nova_access(self):
        """Integration test of the API.
        Add the API credentials to your environment variables before running this test.
        nova_api_credentials: "<client_id>,<client_secret>"

        The test attempts to obtain a bearer token.
        """
        credentials = os.getenv('NOVA_CREDENTIALS')
        credentials = credentials.split(',')
        nova_access = NovaAccess(client_id=credentials[0], client_secret=credentials[1])
        self.assertNotEqual("", nova_access.get_bearer_token())


if __name__ == '__main__':
    unittest.main()
