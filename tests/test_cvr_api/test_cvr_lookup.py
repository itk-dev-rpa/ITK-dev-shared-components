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


if __name__ == '__main__':
    unittest.main()
