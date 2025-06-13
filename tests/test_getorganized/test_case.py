import unittest
import os
import re
import json
from uuid import uuid4

from dotenv import load_dotenv

from itk_dev_shared_components.getorganized import go_api

load_dotenv()


class CaseTest(unittest.TestCase):
    """Test the Case functionality of GetOrganized integration"""
    test_case = None    

    @classmethod
    def setUpClass(cls):
        # Et ID der deles på tværs af alle tests i klassen
        user, password = os.getenv("GO_LOGIN").split(",")

        cls.session = go_api.create_session(user, password)
        uuid = uuid4()
        cls.test_case = go_api.create_case(session=cls.session, apiurl=os.getenv("GO_APIURL"), title=uuid, case_type="EMN")

    def test_case_created(self):
        """Test case is created."""
        self.assertIsNotNone(self.test_case)

    def test_document(self):
        """Test upload and delete of a document."""
        test_data = bytearray(b"Testdata")
        document = go_api.upload_document(session=self.session, apiurl=os.getenv("GO_APIURL"), case=self.test_case, filename="Testfil", file=test_data)
        self.assertIsNotNone(document)
        response = go_api.delete_document(session=self.session, apiurl=os.getenv("GO_APIURL"), document_id=json.loads(document)['DocId'])
        self.assertEqual(response.status_code, 200)

    def test_find_case(self):
        """Test finding a case and getting metadata."""
        metadata = go_api.case_metadata(self.session, os.getenv("GO_APIURL"), self.test_case)
        self.assertIsNotNone(metadata)

        test_case_title = re.match('.*ows_Title="([^"]+)"', metadata)[1]
        case_found = go_api.find_case(session=self.session, apiurl=os.getenv("GO_APIURL"), case_title=test_case_title, case_type="EMN")
        if isinstance(case_found, list):
            self.assertIn(self.test_case, case_found)
        else:
            self.assertEqual(self.test_case, case_found)


if __name__ == '__main__':
    unittest.main()
