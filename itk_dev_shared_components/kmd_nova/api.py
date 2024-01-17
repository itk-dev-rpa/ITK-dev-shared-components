"""This module provides an API to KMD Nova ESDH"""

from datetime import datetime, timedelta
import uuid
import json
import mimetypes
import os
import io

import requests
from itk_dev_shared_components.kmd_nova.nova_objects import NovaCase, CaseParty, Document


class NovaESDH:
    """
    This class gives access to the KMD Nova ESDH API. Get read/write access to documents and journal notes in the system.
    A bearer token is automatically created and updated when the class is instantiated.
    Using api version 1.0.
    The api docs can be found here: https://novaapi.kmd.dk/swagger/index.html
    """

    DOMAIN = "https://cap-novaapi.kmd.dk"
    TIMEOUT = 60

    def __init__(self, client_id: str, client_secret: str) -> None:
        """
        Args:
            client_id: string
            client_secret: string
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self._bearer_token, self.token_expiry_date = self._get_new_token()

    def _get_new_token(self) -> tuple[str, datetime]:
        """
        This method requests a new token from the API.
        When the token expiry date is passed, requests with the token to the API will return HTTP 401 status code.

        Returns:
            tuple: token and expiry datetime

        Raises:
            requests.exceptions.HTTPError if the request failed.
        """

        url = "https://novaauth.kmd.dk/realms/NovaIntegration/protocol/openid-connect/token"
        payload = f"client_secret={self.client_secret}&grant_type=client_credentials&client_id={self.client_id}&scope=client"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url, headers=headers, data=payload, timeout=self.TIMEOUT)
        response.raise_for_status()
        bearer_token = response.json()['access_token']
        token_life_seconds = response.json()['expires_in']
        token_expiry_date = datetime.now() + timedelta(seconds=int(token_life_seconds))
        return bearer_token, token_expiry_date

    def get_bearer_token(self) -> str:
        """Return the bearer token. If the token is about to expire,
         a new token is requested form the auth service.

         Returns: Bearer token
         """

        if self.token_expiry_date + timedelta(seconds=30) < datetime.now():
            self._bearer_token, self.token_expiry_date = self._get_new_token()

        return self._bearer_token

    def upload_document(self, document_path: str) -> str:
        """Upload a document to Nova.

        Args:
            document_path: The path to the file.

        Returns:
            The uuid identifying the document in Nova.
        """
        transaction_id = str(uuid.uuid4())
        document_id = str(uuid.uuid4())

        url = f"{self.DOMAIN}/api/Document/UploadFile/{transaction_id}/{document_id}?api-version=1.0-Case"

        headers = {'Authorization': f"Bearer {self.get_bearer_token()}", 'accept': '*/*'}

        file_name = os.path.basename(document_path)
        mime_type = mimetypes.guess_type(document_path)[0]

        if mime_type is None:
            mime_type = 'application/octet-stream'

        with open(document_path, 'rb') as file:
            files = {"file": (file_name, file, mime_type)}
            response = requests.post(url, headers=headers, timeout=self.TIMEOUT, files=files)

        response.raise_for_status()

        return document_id

    def attach_document_to_case(self, case_uuid: str, document: Document, security_unit_id: int = 818485, security_unit_name: str = "Borgerservice") -> None:
        """Attach a document to a case in Nova.
        The document file first needs to be uploaded using upload_document.

        Args:
            case_uuid: The uuid of the case to attach the document to.
            document: The document object to attach to the case.
            security_unit_id: The id of the security unit that has access to the document. Defaults to 818485.
            security_unit_name: The name of the security unit that has access to the document. Defaults to "Borgerservice".
        """
        url = f"{self.DOMAIN}/api/Document/Import?api-version=1.0-Case"

        payload = {
            "common": {
                "transactionId": str(uuid.uuid4()),
                "uuid": document.uuid
            },
            "caseUuid": case_uuid,
            "title": document.title,
            "sensitivity": document.sensitivity,
            "documentDate": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "documentType": document.document_type,
            "description": document.description,
            "securityUnit": {
                "losIdentity": {
                    "administrativeUnitId": security_unit_id,
                    "fullName": security_unit_name,
                }
            },
            "approved": document.approved,
            "accessToDocuments": True
        }

        payload = json.dumps(payload)
        headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {self.get_bearer_token()}"}
        response = requests.post(url, headers=headers, data=payload, timeout=self.TIMEOUT)
        response.raise_for_status()


if __name__ == '__main__':
    def main():
        credentials = os.getenv('nova_api_credentials')
        credentials = credentials.split(',')
        nova = NovaESDH(client_id=credentials[0], client_secret=credentials[1])

        case = nova.get_cases(case_number="S2023-61078")[0]

        # document_id = nova.upload_document(r"C:\Users\az68933\Desktop\NovaTest V2.txt")
        # print(document_id)
        # nova.attach_document_to_case(case.uuid, document_id)

        # documents = nova.get_documents("S2023-61078")
        # doc_file = nova.download_document_file(documents[0].uuid)
        # with open(r"C:\Users\az68933\Desktop\temp\temp.txt", 'wb') as file:
        #     file.write(doc_file.read())

        print("Hej")

    main()
