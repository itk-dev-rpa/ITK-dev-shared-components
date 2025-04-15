import unittest
import os

from dotenv import load_dotenv

from itk_dev_shared_components.getorganized import go_api

load_dotenv()


class CaseTest(unittest.TestCase):
    """Test the Case functionality of GetOrganized integration"""

    def test_create_case(self):
        """Test creating a case."""
        user, password = os.getenv("GO_LOGIN").split(",")

        session = go_api.create_session(user, password)

        go_api.create_case(session=session, apiurl=os.getenv("GO_APIURL"), title="TestCase", case_type="EMN")


if __name__ == '__main__':
    unittest.main()
