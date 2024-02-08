"""Test the part of the API to do with cases."""
import unittest
import os
import uuid
from datetime import datetime

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import NovaCase, CaseParty
from itk_dev_shared_components.kmd_nova import nova_cases


class NovaCasesTest(unittest.TestCase):
    """Test the part of the API to do with cases."""
    @classmethod
    def setUpClass(cls):
        credentials = os.getenv('nova_api_credentials')
        credentials = credentials.split(',')
        cls.nova_access = NovaAccess(client_id=credentials[0], client_secret=credentials[1])

    def test_get_cases(self):
        """Test the API for getting cases on a given case number."""
        cpr = "6101009805"
        case_title = "Meget_Unik_Case_Overskrift"
        case_number = "S2023-61078"

        cases = nova_cases.get_cases(cpr=cpr, nova_access=self.nova_access)
        self.assertIsInstance(cases[0], NovaCase)
        self.assertEqual(cases[0].case_parties[0].identification, cpr)

        cases = nova_cases.get_cases(case_number=case_number, nova_access=self.nova_access)
        self.assertEqual(cases[0].case_number, case_number)

        cases = nova_cases.get_cases(case_title=case_title, nova_access=self.nova_access)
        self.assertEqual(cases[0].title, case_title)

        cases = nova_cases.get_cases(cpr=cpr, case_title=case_title, nova_access=self.nova_access)
        self.assertEqual(cases[0].case_parties[0].identification, cpr)
        self.assertEqual(cases[0].title, case_title)

        cases = nova_cases.get_cases(cpr=cpr, case_number=case_number, nova_access=self.nova_access)
        self.assertEqual(cases[0].case_parties[0].identification, cpr)
        self.assertEqual(cases[0].case_number, case_number)

        cases = nova_cases.get_cases(case_number=case_number, case_title=case_title, nova_access=self.nova_access)
        self.assertEqual(cases[0].case_number, case_number)
        self.assertEqual(cases[0].title, case_title)

        with self.assertRaises(ValueError):
            nova_cases.get_cases(nova_access=self.nova_access)

    def test_add_case(self):
        """Test adding a case to Nova."""
        party = CaseParty(
            role="Primær",
            identification_type="CprNummer",
            identification="6101009805",
            name="Test Test"
        )

        case = NovaCase(
            uuid=str(uuid.uuid4()),
            title=f"Test {datetime.now()}",
            case_date=datetime.now(),
            progress_state="Opstaaet",
            case_parties=[party],
            kle_number="23.05.01",
            proceeding_facet="G01",
            sensitivity="Fortrolige"
        )

        nova_cases.add_case(case, self.nova_access)


if __name__ == '__main__':
    unittest.main()
