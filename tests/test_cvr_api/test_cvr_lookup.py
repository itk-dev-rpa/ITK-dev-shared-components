"""Tests relating to the module cvr_api.cvr_lookup."""

import unittest
import os
from datetime import date

from dotenv import load_dotenv

from itk_dev_shared_components.cvr_api import cvr_lookup
from itk_dev_shared_components.cvr_api.cvr_lookup import Company


load_dotenv()


class TestCvrLookup(unittest.TestCase):
    """Tests relating to the module cvr_api.cvr_lookup."""

    def test_cvr_lookup(self):
        """Test the function cvr_lookup."""
        username, password = os.environ['CVR_CREDS'].split(";")
        company = cvr_lookup.cvr_lookup("55133018", username, password)

        self.assertIsInstance(company, Company)
        self.assertEqual(company.cvr, "55133018")
        self.assertEqual(company.name, "Aarhus Kommune")
        self.assertEqual(company.address, "Rådhuspladsen 2")
        self.assertEqual(company.postal_code, "8000")
        self.assertEqual(company.city, "Aarhus C")
        self.assertEqual(company.founded_date, date(1976, 1, 1))
        self.assertEqual(company.company_type, "Primærkommune")

        with self.assertRaises(ValueError):
            cvr_lookup.cvr_lookup("12345", username, password)

    def test_cvr_mass_lookup(self):
        """Test the function cvr_mass_lookup."""
        username, password = os.environ['CVR_CREDS'].split(";")

        cvr_list = ["27966535", "55133018", "36435607"]

        companies = cvr_lookup.cvr_mass_lookup(cvr_list, True, username, password)

        self.assertEqual(len(companies), 3)

        # Check sort order
        for company, cvr in zip(companies, cvr_list):
            self.assertEqual(company.cvr, cvr)

        self.assertIsInstance(companies[1], Company)
        self.assertEqual(companies[1].cvr, "55133018")
        self.assertEqual(companies[1].name, "Aarhus Kommune")
        self.assertEqual(companies[1].address, "Rådhuspladsen 2")
        self.assertEqual(companies[1].postal_code, "8000")
        self.assertEqual(companies[1].city, "Aarhus C")
        self.assertEqual(companies[1].founded_date, date(1976, 1, 1))
        self.assertEqual(companies[1].company_type, "Primærkommune")

        # Test match_length
        with self.assertRaises(ValueError):
            cvr_lookup.cvr_mass_lookup(["12345"], True, username, password)

        companies = cvr_lookup.cvr_mass_lookup(["12345"], False, username, password)
        self.assertEqual(len(companies), 0)


if __name__ == '__main__':
    unittest.main()
