"""This module has functions to do with document related calls
to the KMD Nova api."""

import uuid
from datetime import datetime
import mimetypes
from typing import BinaryIO
import urllib.parse

import requests

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import Document, Caseworker
from itk_dev_shared_components.kmd_nova. util import datetime_from_iso_string


def get_documents(case_uuid: str, nova_access: NovaAccess) -> list[Document]:
    """Get all documents attached to the given case.
    To get the actual document file use download_document_file.

    Args:
        case_uuid: The uuid of the case to get documents from.
        nova_access: The NovaAccess object used to authenticate.

    Returns:
        A list of Document objects describing the documents.

    Raises:
        requests.exceptions.HTTPError: If the request failed.
    """
    url = urllib.parse.urljoin(nova_access.domain, "api/Document/GetList")
    params = {"api-version": "1.0-Case"}

    payload = {
        "common": {
            "transactionId": str(uuid.uuid4())
        },
        "caseUuid": case_uuid,
        "getOutput": {
            "title": True,
            "sensitivity": True,
            "documentType": True,
            "description": True,
            "approved": True,
            "documentDate": True,
            "fileExtension": True,
            "documentCategory": True,
            "caseworker": True
        }
    }

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}

    response = requests.put(url, params=params, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    documents = []
    for document_dict in response.json()['documents']:

        if 'caseworker' in document_dict:
            caseworker = Caseworker(
                uuid = document_dict['caseworker']['kspIdentity']['novaUserId'],
                name = document_dict['caseworker']['kspIdentity']['fullName'],
                ident = document_dict['caseworker']['kspIdentity']['racfId']
            )
        else:
            caseworker = None

        doc = Document(
            uuid = document_dict['documentUuid'],
            document_number = document_dict['documentNumber'],
            title = document_dict['title'],
            sensitivity = document_dict['sensitivity'],
            document_type = document_dict['documentType'],
            description = document_dict.get('description', None),
            approved = document_dict['approved'],
            document_date = datetime_from_iso_string(document_dict['documentDate']),
            file_extension = document_dict['fileExtension'],
            category_name = document_dict.get('documentCategoryName'),
            category_uuid = document_dict.get('documentCategoryUuid'),
            caseworker=caseworker
        )
        documents.append(doc)

    return documents


def download_document_file(document_uuid: str, nova_access: NovaAccess, checkout: bool = False, checkout_comment: str = None) -> bytes:
    """Download the file attached to a KMD Nova Document.

    Args:
        document_uuid: The uuid of the Nova document.
        nova_access: The NovaAccess object used to authenticate.
        checkout: Whether to mark the document as checked out. Defaults to False.
        checkout_comment: A comment to the checkout. Defaults to None.

    Returns:
        The document file as raw bytes.

    Raises:
        requests.exceptions.HTTPError: If the request failed.
    """
    url = urllib.parse.urljoin(nova_access.domain, "api/Document/GetFile")
    params = {"api-version": "1.0-Case"}

    payload = {
        "common": {
            "transactionId": str(uuid.uuid4()),
            "uuid": document_uuid
        },
        "checkOutDocument": checkout,
        "checkOutComment": checkout_comment
    }

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}
    response = requests.put(url, params=params, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    return response.content


def upload_document(file: BinaryIO, file_name: str, nova_access: NovaAccess) -> str:
    """Upload a document to Nova. This only uploads the document file.
    To attach the document to a case use attach_document_to_case after calling this.
    The uuid returned should be used to create a new Document object.

    Args:
        file: The file to upload as a file-like object in binary mode.
        file_name: The name of the file including the file extension.
        nova_access: The NovaAccess object used to authenticate.

    Returns:
        The uuid identifying the document in Nova.

    Raises:
        requests.exceptions.HTTPError: If the request failed.
    """
    transaction_id = urllib.parse.quote(str(uuid.uuid4()))
    document_id = urllib.parse.quote(str(uuid.uuid4()))

    url = urllib.parse.urljoin(nova_access.domain, f"api/Document/UploadFile/{transaction_id}/{document_id}")
    params = {"api-version": "1.0-Case"}

    headers = {'Authorization': f"Bearer {nova_access.get_bearer_token()}", 'accept': '*/*'}

    mime_type = mimetypes.guess_type(file_name)[0]

    if mime_type is None:
        mime_type = 'application/octet-stream'

    files = {"file": (file_name, file, mime_type)}
    response = requests.post(url, params=params, headers=headers, files=files, timeout=60)

    response.raise_for_status()

    return document_id


def attach_document_to_case(case_uuid: str, document: Document, nova_access: NovaAccess, security_unit_id: int = 818485, security_unit_name: str = "Borgerservice") -> None:
    """Attach a document to a case in Nova.
    The document file first needs to be uploaded using upload_document,
    which also creates the document uuid.

    Args:
        case_uuid: The uuid of the case to attach the document to.
        document: The document object to attach to the case.
        nova_access: The NovaAccess object used to authenticate.
        security_unit_id: The id of the security unit that has access to the document. Defaults to 818485.
        security_unit_name: The name of the security unit that has access to the document. Defaults to "Borgerservice".

    Raises:
        requests.exceptions.HTTPError: If the request failed.
    """
    url = urllib.parse.urljoin(nova_access.domain, "api/Document/Import")
    params = {"api-version": "1.0-Case"}

    payload = {
        "common": {
            "transactionId": str(uuid.uuid4()),
            "uuid": document.uuid
        },
        "caseUuid": case_uuid,
        "title": document.title,
        "sensitivity": document.sensitivity,
        "documentDate": datetime.now().isoformat(),
        "documentType": document.document_type,
        "description": document.description,
        "documentCategoryUuid": document.category_uuid,
        "securityUnit": {
            "losIdentity": {
                "administrativeUnitId": security_unit_id,
                "fullName": security_unit_name,
            }
        },
        "approved": document.approved,
        "accessToDocuments": True
    }

    if document.caseworker:
        payload['caseworker'] = {
            "kspIdentity": {
                "racfId": document.caseworker.ident,
                "fullName": document.caseworker.name
            }
        }

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}
    response = requests.post(url, params=params, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
