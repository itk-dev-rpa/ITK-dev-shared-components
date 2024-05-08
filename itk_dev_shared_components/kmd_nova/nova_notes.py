"""This module has functions to do with journal note related calls to the KMD Nova api."""

import base64
import uuid
import urllib.parse
from datetime import datetime

import requests

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import JournalNote


def add_text_note(case_uuid: str, note_title: str, note_text: str, approved: bool, nova_access: NovaAccess) -> str:
    """Add a text based journal note to a Nova case.

    Args:
        case_uuid: The uuid of the case to add the journal note to.
        note_title: The title of the note.
        note_text: The text content of the note.
        approved: Whether the journal note should be marked as approved in Nova.
        nova_access: The NovaAccess object used to authenticate.

    Returns:
        The uuid of the created journal note.
    """
    note_uuid = str(uuid.uuid4())

    url = urllib.parse.urljoin(nova_access.domain, "api/Case/Update")
    params = {"api-version": "1.0-Case"}

    payload = {
        "common": {
            "transactionId": str(uuid.uuid4()),
            "uuid": case_uuid
        },
        "journalNotes": [
            {
                "uuid": note_uuid,
                "approved": approved,
                "journalNoteAttributes": {
                    "journalNoteDate": datetime.today().isoformat(),
                    "title": note_title,
                    "journalNoteType": "Bruger",
                    "format": "Text",
                    "note": _encode_text(note_text)
                }
            }
        ]
    }

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}

    response = requests.patch(url, params=params, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    return note_uuid


def _encode_text(string: str) -> str:
    """Encode a string to a base64 string.
    Ensure the base64 string doesn't contain padding by inserting spaces at the end of the input string.
    There is a bug in the Nova api that corrupts the string if it contains padding.
    The extra spaces will not show up in the Nova user interface.

    Args:
        string: The string to encode.

    Returns:
        A base64 string containing no padding.
    """
    def b64(s: str) -> str:
        """Helper function to convert a string to base64."""
        return base64.b64encode(s.encode()).decode()

    while (s := b64(string)).endswith("="):
        string += ' '

    return s


def get_notes(case_uuid: str, nova_access: NovaAccess, offset: int = 0, limit: int = 100) -> tuple[JournalNote, ...]:
    """Get all journal notes from the given case.

    Args:
        case_uuid: The uuid of the case to get notes from.
        nova_access: The NovaAccess object used to authenticate.
        offset: The number of journal notes to skip.
        limit: The maximum number of journal notes to get (1-500).

    Returns:
        A tuple of JournalNote objects.
    """
    url = urllib.parse.urljoin(nova_access.domain, "api/Case/GetList")
    params = {"api-version": "1.0-Case"}

    payload = {
        "common": {
            "transactionId": str(uuid.uuid4()),
            "uuid": case_uuid
        },
        "paging": {
            "startRow": offset+1,
            "numberOfRows": limit
        },
        "caseGetOutput": {
            "journalNotes": {
                "uuid": True,
                "approved": True,
                "journalNoteAttributes": {
                    "title": True,
                    "format": True,
                    "note": True,
                    "createdTime": True
                }
            }
        }
    }

    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {nova_access.get_bearer_token()}"}

    response = requests.put(url, params=params, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    note_dicts = response.json()['cases'][0]['journalNotes']['journalNotes']

    notes_list = []

    for note_dict in note_dicts:
        notes_list.append(
            JournalNote(
                uuid=note_dict['uuid'],
                title=note_dict['journalNoteAttributes']['title'],
                approved=note_dict['approved'],
                journal_date=note_dict['journalNoteAttributes']['createdTime'],
                note=note_dict['journalNoteAttributes']['note'],
                note_format=note_dict['journalNoteAttributes']['format']
            )
        )

    return tuple(notes_list)
