"""Test the part of the API to do with cases."""
import unittest
import os
import uuid
from datetime import datetime
import time
import json

from dotenv import load_dotenv

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import NovaCase, CaseParty, Caseworker, Department
from itk_dev_shared_components.kmd_nova import nova_cases

load_dotenv()


class NovaCasesTest(unittest.TestCase):
    """Test the part of the API to do with cases."""
    @classmethod
    def setUpClass(cls):
        credentials = os.getenv('NOVA_CREDENTIALS').split(',')
        cls.nova_access = NovaAccess(client_id=credentials[0], client_secret=credentials[1])

    def test_get_cases(self):
        """Test the API for getting cases on a given case number."""
        cpr_case = json.loads(os.environ['NOVA_CPR_CASE'])
        cpr = cpr_case['cpr']
        case_title = cpr_case['case_title']
        case_number = cpr_case['case_number']

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

    def test_get_cvr_cases(self):
        """Test the API for getting cases on a given case number."""
        cvr_case = json.loads(os.environ['NOVA_CVR_CASE'])
        cvr = cvr_case['cvr']
        case_title = cvr_case['case_title']
        case_number = cvr_case['case_number']

        # This test is too slow
        # cases = nova_cases.get_cvr_cases(cvr=cvr, nova_access=self.nova_access)
        # self.assertIsInstance(cases[0], NovaCase)
        # self.assertEqual(cases[0].case_parties[0].identification, cvr)

        cases = nova_cases.get_cvr_cases(case_number=case_number, nova_access=self.nova_access)
        self.assertEqual(cases[0].case_number, case_number)

        cases = nova_cases.get_cvr_cases(case_title=case_title, nova_access=self.nova_access)
        self.assertEqual(cases[0].title, case_title)

        cases = nova_cases.get_cvr_cases(cvr=cvr, case_title=case_title, nova_access=self.nova_access)
        self.assertEqual(cases[0].case_parties[0].identification, cvr)
        self.assertEqual(cases[0].title, case_title)

        cases = nova_cases.get_cvr_cases(cvr=cvr, case_number=case_number, nova_access=self.nova_access)
        self.assertEqual(cases[0].case_parties[0].identification, cvr)
        self.assertEqual(cases[0].case_number, case_number)

        cases = nova_cases.get_cvr_cases(case_number=case_number, case_title=case_title, nova_access=self.nova_access)
        self.assertEqual(cases[0].case_number, case_number)
        self.assertEqual(cases[0].title, case_title)

        with self.assertRaises(ValueError):
            nova_cases.get_cvr_cases(nova_access=self.nova_access)

    def test_add_case(self):
        """Test adding a case to Nova.
        Also tests getting a case on uuid.
        """
        nova_party = os.getenv('NOVA_PARTY').split(',')
        party = CaseParty(
            role="Primær",
            identification_type="CprNummer",
            identification=nova_party[0],
            name=nova_party[1]
        )

        caseworker_dict = json.loads(os.environ['NOVA_USER'])
        caseworker = Caseworker(
            **caseworker_dict
        )

        department_dict = json.loads(os.environ['NOVA_DEPARTMENT'])
        department = Department(
            **department_dict
        )

        case = NovaCase(
            uuid=str(uuid.uuid4()),
            title=f"Test {datetime.now()}",
            case_date=datetime.now(),
            progress_state="Opstaaet",
            case_parties=[party],
            kle_number="23.05.01",
            proceeding_facet="G01",
            sensitivity="Fortrolige",
            caseworker=caseworker,
            responsible_department=department,
            security_unit=department
        )

        nova_cases.add_case(case, self.nova_access)

        # Wait up to 10 seconds for the case to be created in Nova
        nova_case = None
        for _ in range(10):
            time.sleep(1)
            try:
                nova_case = nova_cases.get_case(case.uuid, self.nova_access)
                break
            except ValueError:
                pass

        self.assertIsNotNone(nova_case)

        self.assertEqual(nova_case.uuid, case.uuid)
        self.assertEqual(nova_case.title, case.title)
        self.assertEqual(nova_case.progress_state, case.progress_state)
        self.assertEqual(nova_case.kle_number, case.kle_number)
        self.assertEqual(nova_case.proceeding_facet, case.proceeding_facet)
        self.assertEqual(nova_case.sensitivity, case.sensitivity)
        self.assertEqual(nova_case.caseworker.ident, case.caseworker.ident)
        self.assertEqual(nova_case.case_parties[0].identification, case.case_parties[0].identification)
        self.assertEqual(nova_case.responsible_department.id, case.responsible_department.id)
        self.assertEqual(nova_case.security_unit.id, case.security_unit.id)

    def test_user_groups(self):
        """Test getting and adding a case with a user group as caseworker."""
        # Get case
        group_case = json.loads(os.environ['NOVA_GROUP_CASE'])
        cpr = group_case['cpr']
        case_number = group_case['case_number']
        caseworker_dict = json.loads(os.environ['NOVA_USER_GROUP'])
        caseworker = Caseworker(
            type='group',
            **caseworker_dict
        )

        cases = nova_cases.get_cases(cpr=cpr, case_number=case_number, nova_access=self.nova_access)

        self.assertEqual(len(cases), 1)
        nova_case = cases[0]
        self.assertIsInstance(nova_case, NovaCase)

        self.assertEqual(nova_case.caseworker, caseworker)

        # Add case
        nova_party = os.getenv('NOVA_PARTY').split(',')
        party = CaseParty(
            role="Primær",
            identification_type="CprNummer",
            identification=nova_party[0],
            name=nova_party[1]
        )

        department_dict = json.loads(os.environ['NOVA_DEPARTMENT'])
        department = Department(
            **department_dict
        )

        case = NovaCase(
            uuid=str(uuid.uuid4()),
            title=f"Test {datetime.now()}",
            case_date=datetime.now(),
            progress_state="Opstaaet",
            case_parties=[party],
            kle_number="23.05.01",
            proceeding_facet="G01",
            sensitivity="Fortrolige",
            caseworker=caseworker,
            responsible_department=department,
            security_unit=department
        )

        nova_cases.add_case(case, self.nova_access)


if __name__ == '__main__':
    unittest.main()
