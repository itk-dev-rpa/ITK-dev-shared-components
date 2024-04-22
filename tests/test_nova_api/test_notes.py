"""Test the part of the API to do with journal notes."""
import unittest
import os
from datetime import datetime
import base64

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import JournalNote
from itk_dev_shared_components.kmd_nova import nova_notes, nova_cases


class NovaNotesTest(unittest.TestCase):
    """Test the part of the API to do with notes."""
    @classmethod
    def setUpClass(cls):
        credentials = os.getenv('nova_api_credentials')
        credentials = credentials.split(',')
        cls.nova_access = NovaAccess(client_id=credentials[0], client_secret=credentials[1])

    def test_add_note(self):
        """Test adding a text note."""
        case = self._get_test_case()

        title = f"Test title {datetime.today()}"
        text = f"Test note {datetime.today()}"

        nova_notes.add_text_note(case.uuid, title, text, False, self.nova_access)

        # Get the note back from Nova
        notes = nova_notes.get_notes(case.uuid, self.nova_access, limit=10)

        nova_note = None
        for note in notes:
            if note.title == title:
                nova_note = note
                break

        self.assertIsNotNone(nova_note)
        self.assertEqual(nova_note.title, title)
        self.assertEqual(nova_note.note_format, "Text")
        self.assertIsNotNone(nova_note.journal_date)

        # Decode note text and remove trailing spaces
        nova_text = nova_note.note
        nova_text = base64.b64decode(nova_text).decode()
        nova_text = nova_text.rstrip()
        self.assertEqual(nova_text, text)

    def test_get_notes(self):
        """Test getting notes from a case."""
        case = self._get_test_case()
        notes = nova_notes.get_notes(case.uuid, self.nova_access, limit=10)
        self.assertGreater(len(notes), 0)
        self.assertIsInstance(notes[0], JournalNote)

    def test_encoding(self):
        """Test encoding strings to base 64."""
        test_data = (
            ("Hello", "SGVsbG8g"),
            (".", "LiAg"),
            ("This is a longer test string", "VGhpcyBpcyBhIGxvbmdlciB0ZXN0IHN0cmluZyAg")
        )

        for string, result in test_data:
            self.assertEqual(nova_notes._encode_text(string), result)  # pylint: disable=protected-access

    def _get_test_case(self):
        return nova_cases.get_cases(self.nova_access, case_number="S2023-61078")[0]


if __name__ == '__main__':
    unittest.main()
