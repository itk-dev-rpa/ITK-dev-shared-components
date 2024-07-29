"""Test the part of the API to do with documents."""
import unittest
import os
import uuid
import json
from datetime import datetime
from io import StringIO, BytesIO

from dotenv import load_dotenv
from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import Document, Caseworker
from itk_dev_shared_components.kmd_nova import nova_cases, nova_documents

load_dotenv()


class NovaDocumentsTest(unittest.TestCase):
    """Test the part of the API to do with documents."""

    @classmethod
    def setUpClass(cls):
        credentials = os.getenv('NOVA_CREDENTIALS')
        credentials = credentials.split(',')
        cls.nova_access = NovaAccess(client_id=credentials[0], client_secret=credentials[1])

    def test_get_documents(self):
        """Test getting documents from a case."""
        case = self._get_test_case()
        documents = nova_documents.get_documents(case.uuid, self.nova_access)
        self.assertGreater(len(documents), 0)
        self.assertIsInstance(documents[0], Document)

    def test_document_upload_download(self):
        """Test upload and download of documents by uploading a file and downloading it again."""
        case = self._get_test_case()

        # Create a virtual file to upload
        text = f"This is a test {uuid.uuid4()}"
        file = StringIO(text)

        doc_uuid = nova_documents.upload_document(file, "Filename.txt", self.nova_access)

        caseworker_dict = json.loads(os.environ['NOVA_USER'])
        caseworker = Caseworker(
            name = caseworker_dict['name'],
            ident = caseworker_dict['ident'],
            uuid = caseworker_dict['uuid']
        )

        title = f"Test document {datetime.now()}"
        document = Document(
            uuid=doc_uuid,
            title=title,
            sensitivity='Fortrolige',
            document_type="Internt",
            description="Description",
            approved=True,
            category_uuid='aa015e27-669c-4934-a661-46900351f0aa',
            caseworker=caseworker
        )

        nova_documents.attach_document_to_case(case.uuid, document, self.nova_access)

        # Check if the document was uploaded correctly by getting it from Nova
        documents = nova_documents.get_documents(case.uuid, self.nova_access)

        nova_document = None
        for doc in documents:
            if doc.title == title:
                nova_document = doc
                break

        self.assertIsNotNone(nova_document)

        # Check document metadata
        self.assertEqual(document.uuid, nova_document.uuid)
        self.assertEqual(document.title, nova_document.title)
        self.assertEqual(document.approved, nova_document.approved)
        self.assertEqual(document.category_uuid, nova_document.category_uuid)
        self.assertEqual(document.description, nova_document.description)
        self.assertEqual(document.sensitivity, nova_document.sensitivity)
        self.assertEqual(document.caseworker.ident, nova_document.caseworker.ident)

        # Download the document file and check its contents
        file_bytes = nova_documents.download_document_file(document.uuid, self.nova_access)
        nova_file = BytesIO(file_bytes)
        self.assertEqual(nova_file.read().decode(), text)

    def _get_test_case(self):
        return nova_cases.get_cases(self.nova_access, case_number="S2023-61078")[0]


if __name__ == '__main__':
    unittest.main()
