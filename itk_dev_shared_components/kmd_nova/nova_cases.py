"""This module has functions to do with case related calls
to the KMD Nova api."""

import uuid
import base64
import urllib.parse

import requests

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import NovaCase, CaseParty, JournalNote, Caseworker, Department
from itk_dev_shared_components.kmd_nova.util import datetime_from_iso_string


def get_cases(nova_access: NovaAccess, cpr: str = None, case_number: str = None, case_title: str = None, limit: int = 100) -> list[NovaCase]:
    """Search for cases on different search terms.
    Currently supports search on cpr number, case number and case title. At least one search term must be given.

    Args:
        nova_access: The NovaAccess object used to authenticate.
        cpr: The cpr number to search on. E.g. "0123456789"
        case_number: The case number to search on. E.g. "S2022-12345"
        case_title: The case title to search on.
        limit: The maximum number of cases to find (1-500).

    Returns:
        A list of NovaCase objects.

    Raises:
        ValueError: If no search terms are given.
    """

    if not any((cpr, case_number, case_title)):
        raise ValueError("No search terms given.")

    payload = _create_payload(cpr, "CprNummer", case_number, case_title, limit)
    return _get_nova_cases(nova_access, payload)


def get_cvr_cases(nova_access: NovaAccess, cvr: str = None,  case_number: str = None, case_title: str = None, limit: int = 100) -> list[NovaCase]:
    """Search for cases on different search terms.
    Currently supports search on cvr number, case number and case title. At least one search term must be given.

    Args:
        nova_access: The NovaAccess object used to authenticate.
        cvr: The cvr number to search on. E.g. "01234567"
        case_number: The case number to search on. E.g. "S2022-12345"
        case_title: The case title to search on.
        limit: The maximum number of cases to find (1-500).

    Returns:
        A list of NovaCase objects.

    Raises:
        ValueError: If no search terms are given.
    """

    if not any((cvr, case_number, case_title)):
        raise ValueError("No search terms given.")

    payload = _create_payload(cvr, "CvrNummer", case_number, case_title, limit)
    return _get_nova_cases(nova_access, payload)


def _get_nova_cases(nova_access: NovaAccess, payload: dict) -> list[NovaCase]:
    """Search for cases with a payload of search terms.

    Args:
        nova_access: The NovaAccess object used to authenticate.
        payload: A dictionary containing case identifier, identifier type, case number case title and limit

    Returns:
        A list of NovaCase objects.

    Raises:
        requests.exceptions.HTTPError: If the request failed.
    """
    url = urllib.parse.urljoin(nova_access.domain, "api/Case/GetList")
    params = {"api-version": "1.0-Case"}

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}

    response = requests.put(url, params=params, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    if response.json()['pagingInformation']['numberOfRows'] == 0:
        return []

    # Convert json to NovaCase objects
    cases = []
    for case_dict in response.json()['cases']:
        security_unit, responsible_department = _extract_departments(case_dict)
        case = NovaCase(
            uuid = case_dict['common']['uuid'],
            title = case_dict['caseAttributes']['title'],
            case_date = datetime_from_iso_string(case_dict['caseAttributes']['caseDate']),
            case_number = case_dict['caseAttributes']['userFriendlyCaseNumber'],
            active_code = case_dict['state']['activeCode'],
            progress_state = case_dict['state']['progressState'],
            case_parties = _extract_case_parties(case_dict),
            document_count = case_dict['numberOfDocuments'],
            note_count = case_dict['numberOfJournalNotes'],
            kle_number = case_dict['caseClassification']['kleNumber']['code'],
            proceeding_facet = case_dict['caseClassification']['proceedingFacet']['code'],
            sensitivity = case_dict["sensitivity"]["sensitivity"],
            caseworker = _extract_case_worker(case_dict),
            security_unit=security_unit,
            responsible_department=responsible_department
        )

        cases.append(case)

    return cases


def _create_payload(identification: str = None, identification_type: str = "CprNummer", case_number: str = None, case_title: str = None, limit: int = 100) -> dict:
    return {
        "common": {
            "transactionId": str(uuid.uuid4())
        },
        "paging": {
            "startRow": 1,
            "numberOfRows": limit
        },
        "caseAttributes": {
            "userFriendlyCaseNumber": case_number,
            "title": case_title
        },
        "caseParty": {
            "identificationType": identification_type,
            "identification": identification
        },
        "caseGetOutput": {
            "numberOfSecondaryParties": True,
            "caseParty": {
                "identificationType": True,
                "identification": True,
                "participantRole": True,
                "name": True,
                "index": True
            },
            "caseAttributes": {
                "title": True,
                "userFriendlyCaseNumber": True,
                "caseDate": True
            },
            "state": {
                "activeCode": True,
                "progressState": True
            },
            "numberOfDocuments": True,
            "numberOfJournalNotes": True,
            "caseClassification": {
                "kleNumber": {
                    "code": True
                },
                "proceedingFacet": {
                    "code": True
                }
            },
            "sensitivity": {
                "sensitivity": True
            },
            "caseworker": {
                "kspIdentity": {
                    "novaUserId": True,
                    "fullName": True,
                    "racfId": True
                }
            },
            "responsibleDepartment": {
                "losIdentity": {
                    "novaUnitId": True,
                    "administrativeUnitId": True,
                    "fullName": True,
                    "userKey": True
                }
            },
            "securityUnit": {
                "losIdentity": {
                    "novaUnitId": True,
                    "administrativeUnitId": True,
                    "fullName": True,
                    "userKey": True
                }
            },
        }
    }


def _extract_departments(case_dict: dict) -> tuple[Department, Department]:
    """Extract the departments from a HTTP request response.

    Args:
        case_dict: The dictionary describing the case.

    Returns:
        The security unit and the responsible department.
    """
    security_unit = Department(
        id=case_dict['securityUnit']['losIdentity']['administrativeUnitId'],
        name=case_dict['securityUnit']['losIdentity']['fullName'],
        user_key=case_dict['securityUnit']['losIdentity']['userKey']
    )

    responsible_department = Department(
        id=case_dict['responsibleDepartment']['losIdentity']['administrativeUnitId'],
        name=case_dict['responsibleDepartment']['losIdentity']['fullName'],
        user_key=case_dict['responsibleDepartment']['losIdentity']['userKey']
    )

    return security_unit, responsible_department


def _extract_case_worker(case_dict: dict) -> Caseworker | None:
    """Extract the case worker from a HTTP request response.
    If the case worker is in a unexpected format, None is returned.

    Args:
        case_dict: The dictionary describing the case.

    Returns:
        A case worker object describing the case worker if any.
    """
    if 'caseworker' in case_dict:
        try:
            return Caseworker(
                uuid = case_dict['caseworker']['kspIdentity']['novaUserId'],
                name = case_dict['caseworker']['kspIdentity']['fullName'],
                ident = case_dict['caseworker']['kspIdentity']['racfId']
            )
        except KeyError:
            return None

    return None


def _extract_case_parties(case_dict: dict) -> list[CaseParty]:
    """Extract the case parties from a HTTP request response.

    Args:
        case_dict: The dictionary describing the case party.

    Returns:
        A case party object describing the case party.
    """
    parties = []
    for party_dict in case_dict['caseParties']:
        party = CaseParty(
            uuid = party_dict['index'],
            identification_type = party_dict['identificationType'],
            identification = party_dict['identification'],
            role = party_dict['participantRole'],
            name = party_dict.get('name', None)
        )
        parties.append(party)

    return parties


def _extract_journal_notes(case_dict: dict) -> list:
    """Extract the journal notes from a HTTP request response.

    Args:
        case_dict: The dictionary describing the journal note.

    Returns:
        A journal note object describing the journal note.
    """
    notes = []
    for note_dict in case_dict['journalNotes']['journalNotes']:
        note = JournalNote(
            uuid = note_dict['uuid'],
            title = note_dict['journalNoteAttributes']['title'],
            journal_date = note_dict['journalNoteAttributes']['journalNoteDate'],
            note_format = note_dict['journalNoteAttributes']['format'],
            note = base64.b64decode(note_dict['journalNoteAttributes']['note']),
            approved = note_dict['journalNoteAttributes'].get('approved', False)
        )
        notes.append(note)
    return notes


def add_case(case: NovaCase, nova_access: NovaAccess):
    """Add a case to KMD Nova. The case will be created as 'Active'.

    Args:
        case: The case object describing the case.
        nova_access: The NovaAccess object used to authenticate.
        security_unit_id: The id of the security unit that has access to the case. Defaults to 818485.
        security_unit_name: The name of the security unit that has access to the case. Defaults to "Borgerservice".

    Raises:
        requests.exceptions.HTTPError: If the request failed.
    """
    url = urllib.parse.urljoin(nova_access.domain, "api/Case/Import")
    params = {"api-version": "1.0-Case"}

    payload = {
        "common": {
            "transactionId": str(uuid.uuid4()),
            "uuid": case.uuid
        },
        "caseAttributes": {
            "title": case.title,
            "caseDate": case.case_date.isoformat()
        },
        "caseClassification": {
                "kleNumber": {
                    "code": case.kle_number
                },
                "proceedingFacet": {
                    "code": case.proceeding_facet
                }
        },
        "state": case.progress_state,
        "sensitivity": case.sensitivity,
        "caseParties": [
            {
                "name": party.name,
                "identificationType": party.identification_type,
                "identification": party.identification,
                "participantRole": party.role
            } for party in case.case_parties
        ],
        "securityUnit": {
            "losIdentity": {
                "administrativeUnitId": case.security_unit.id,
                "fullName": case.security_unit.name,
                "userKey": case.security_unit.user_key
            }
        },
        "responsibleDepartment": {
            "losIdentity": {
                "administrativeUnitId": case.responsible_department.id,
                "fullName": case.responsible_department.name,
                "userKey": case.responsible_department.user_key
            }
        },
        "SensitivityCtrlBy": "Bruger",
        "SecurityUnitCtrlBy": "Regler",
        "ResponsibleDepartmentCtrlBy": "Regler",
        "caseAvailability": {
            "unit": "År",
            "scale": 5
        },
        "AvailabilityCtrlBy": "Regler"
    }

    if case.caseworker:
        payload['caseworker'] = {
            "kspIdentity": {
                "racfId": case.caseworker.ident,
                "fullName": case.caseworker.name
            }
        }

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}

    response = requests.post(url, params=params, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
