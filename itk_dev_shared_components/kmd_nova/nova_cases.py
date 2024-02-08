"""This module has functions to do with case related calls
to the KMD Nova api."""

import uuid
import base64

import requests

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import NovaCase, CaseParty, JournalNote
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
        requests.exceptions.HTTPError: If the request failed.
    """

    if not any((cpr, case_number, case_title)):
        raise ValueError("No search terms given.")

    url = f"{nova_access.domain}/api/Case/GetList"
    params = {"api-version": "1.0-Case"}

    payload = {
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
            "identificationType": "CprNummer",
            "identification": cpr
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
            }
        }
    }

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}

    response = requests.put(url, params=params, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    if response.json()['pagingInformation']['numberOfRows'] == 0:
        return []

    # Convert json to NovaCase objects
    cases = []
    for case_dict in response.json()['cases']:
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
            sensitivity = case_dict["sensitivity"]["sensitivity"]
        )

        cases.append(case)

    return cases


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


def add_case(case: NovaCase, nova_access: NovaAccess, security_unit_id: int = 818485, security_unit_name: str = "Borgerservice"):
    """Add a case to KMD Nova. The case will be created as 'Active'.

    Args:
        case: The case object describing the case.
        nova_access: The NovaAccess object used to authenticate.
        security_unit_id: The id of the security unit that has access to the case. Defaults to 818485.
        security_unit_name: The name of the security unit that has access to the case. Defaults to "Borgerservice".

    Raises:
        requests.exceptions.HTTPError: If the request failed.
    """
    url = f"{nova_access.domain}/api/Case/Import"
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
                "administrativeUnitId": security_unit_id,
                "fullName": security_unit_name,
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

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}

    response = requests.post(url, params=params, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
