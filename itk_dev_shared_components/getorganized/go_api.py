"""Functions for working with the GetOrganized API."""

import json
from urllib.parse import urljoin
from typing import Literal

from requests import Session
from requests_ntlm import HttpNtlmAuth


def create_session(username: str, password: str) -> Session:
    """Create a session for accessing GetOrganized API.

    Args:
        apiurl: URL for the API.
        username: Username for login.
        password: Password for login.

    Returns:
        Return the session object
    """
    session = Session()
    session.headers.setdefault("Content-Type", "application/json")
    session.auth = HttpNtlmAuth(username, password)
    return session


def upload_document(*, apiurl: str, file: bytearray, case: str, filename: str, agent_name: str | None = None, date_string: str | None = None, session: Session, doc_category: str | None = None, case_type: str = Literal["EMN", "GEO"]) -> tuple[str, Session]:
    """Upload a document to Get Organized.

    Args:
        apiurl: Base url for API.
        session: Session token for request.
        file: Bytearray of file to upload.
        case: Case name already present in GO.
        filename: Name of file when saved in GO.
        agent_name: Agent name, used for creating a folder in GO. Defaults to None.
        date_string: A date to add as metadata to GetOrganized. Defaults to None.

    Returns:
        Return response text and session token.
    """
    url = apiurl + "/_goapi/Documents/AddToCase"
    payload = {
        "Bytes": list(file),
        "CaseId": case,
        "SiteUrl": urljoin(apiurl, f"/case{case_type}/{case}"),
        "ListName": "Dokumenter",
        "FolderPath": agent_name,
        "FileName": filename,
        "Metadata": f"<z:row xmlns:z='#RowsetSchema' ows_Dato='{date_string}' ows_Kategori='{doc_category}'/>",
        "Overwrite": True
    }
    response = session.post(url, data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    return response.text


def delete_document(apiurl: str, document_id: int, session: Session) -> tuple[str, Session]:
    """Delete a document from GetOrganized.

    Args:
        apiurl: Url of the GetOrganized API.
        session: Session object used for logging in.
        document_id: ID of the document to delete.

    Returns:
        Return the response and session objects
    """
    url = urljoin(apiurl, "/_goapi/Documents/ByDocumentId/")
    payload = {
        "DocId": document_id,
        "ForceDelete": True
    }
    response = session.delete(url, timeout=60, data=json.dumps(payload))
    response.raise_for_status()
    return response


def create_case(session: Session, apiurl: str, title: str, case_type: str = Literal["EMN", "GEO"]) -> tuple[str, Session]:
    """Create a case in GetOrganized.

    Args:
        apiurl: Url for the GetOrganized API.
        session: Session object to access API.
        title: Title of the case being created.

    Returns:
        Return the response and session objects.
    """
    url = urljoin(apiurl, "/_goapi/Cases/")
    payload = {
        'CaseTypePrefix': case_type,
        'MetadataXml': f'<z:row xmlns:z="#RowsetSchema" ows_Title="{title}" ows_CaseStatus="Åben" ows_CaseCategory="Åben for alle" ows_Afdeling="916;#Backoffice - Drift og Økonomi" ows_KLENummer="318;#25.02.00 Ejendomsbeskatning i almindelighed"/>',
        'ReturnWhenCaseFullyCreated': False
    }
    response = session.post(url, data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    return response.json()["CaseID"]


def case_metadata(session: Session, apiurl: str, case_id: str):
    """Get metadata for a GetOrganized case, to look through parameters and values.

    Args:
        session: Session token.
        apiurl: Base URL for the API.
        case_id: Case ID to get metadata on.

    Returns:
        Return the response and session objects.
    """
    url = urljoin(apiurl, f"/_goapi/Cases/Metadata/{case_id}")
    response = session.get(url, timeout=60)
    response.raise_for_status()
    return response.json()["Metadata"]


def find_case(session: Session, apiurl: str, case_title: str, case_type: str = Literal["EMN", "GEO"]) -> str | list[str] | None:
    """Search for an existing case in GO with the given case title.
    The search finds any case that contains the given title in its title.

    Args:
        case_title: The title to search for.
        session: Session object to access the API.

    Returns:
        The case id of the found case(s) if any.
    """
    url = apiurl + "/_goapi/Cases/FindByCaseProperties"
    payload = {
        "FieldProperties": [
            {
                "InternalName": "ows_Title",
                "Value": case_title,
                "ComparisonType": "Contains",
            }
        ],
        "CaseTypePrefixes": [case_type],
        "LogicalOperator": "AND",
        "ExcludeDeletedCases": True
    }
    response = session.post(url, data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    cases = response.json()['CasesInfo']

    if len(cases) == 0:
        return None
    if len(cases) == 1:
        return cases[0]['CaseID']

    return [case['CaseID'] for case in cases]
