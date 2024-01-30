"""This module has functions to do with case related calls
to the KMD Nova api."""

import os
import uuid
import base64

import requests

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import NovaCase, CaseParty, JournalNote


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

    url = f"{nova_access.domain}/api/Case/GetList?api-version=1.0-Case"

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
                "partyRole": True,
                "name": True
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
                }
            }
        }
    }

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}

    response = requests.put(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    # Convert json to NovaCase objects
    cases = []
    for case_dict in response.json()['cases']:
        case = NovaCase(
            uuid = case_dict['common']['uuid'],
            title = case_dict['caseAttributes']['title'],
            case_date = case_dict['caseAttributes']['caseDate'],
            case_number = case_dict['caseAttributes']['userFriendlyCaseNumber'],
            active_code = case_dict['state']['activeCode'],
            progress_state = case_dict['state']['progressState'],
            case_parties = _extract_case_parties(case_dict),
            document_count = case_dict['numberOfDocuments'],
            note_count = case_dict['numberOfJournalNotes'],
            kle_number = case_dict['caseClassification']['kleNumber']['code']
        )

        cases.append(case)

    return cases


def _extract_case_parties(case_dict: dict) -> list[CaseParty]:
    parties = []
    for party_dict in case_dict['caseParties']:
        party = CaseParty(
            identification_type = party_dict['identificationType'],
            identification = party_dict['identification'],
            role = party_dict['partyRole'],
            name = party_dict.get('name', None)
        )
        parties.append(party)

    return parties


def _extract_journal_notes(case_dict: dict) -> list:
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


if __name__ == '__main__':
    def main():
        credentials = os.getenv('nova_api_credentials')
        credentials = credentials.split(',')
        nova_access = NovaAccess(client_id=credentials[0], client_secret=credentials[1])

        cases = get_cases(nova_access, case_number="S2023-61078")

        from itk_dev_shared_components.kmd_nova.nova_tasks import get_tasks
        get_tasks(cases[0].uuid, nova_access)

        print(cases)

    main()
