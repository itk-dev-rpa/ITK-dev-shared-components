"""Tests relating to the module misc.address_lookup."""

import unittest
from datetime import date

from itk_dev_shared_components.misc import address_lookup
from itk_dev_shared_components.misc.address_lookup import Address


class TestAddressLookup(unittest.TestCase):
    """Tests relating to the module misc.address_lookup."""

    def test_search_exact_address(self):
        """Test searching for an exact address."""
        addresses = address_lookup.search_address(query=None, street="Sønder Allé", number="2", postal_code="8000", municipality_code="0751")
        self.assertEqual(len(addresses), 1)
        self.assertIsInstance(addresses[0], Address)
        self.assertEqual(addresses[0].street, "Sønder Allé")
        self.assertEqual(addresses[0].number, "2")
        self.assertEqual(addresses[0].floor, None)
        self.assertEqual(addresses[0].door, None)
        self.assertEqual(addresses[0].minor_city, None)
        self.assertEqual(addresses[0].postal_city, "Aarhus C")
        self.assertEqual(addresses[0].postal_code, "8000")
        self.assertEqual(addresses[0].municipality_code, "0751")
        self.assertEqual(addresses[0].address_text, "Sønder Allé 2, 8000 Aarhus C")
        self.assertEqual(addresses[0].id, "ab9dc59e-f232-4c9c-9e27-616743d21f8f")

    def test_query_search(self):
        """Test searching by query text."""
        addresses = address_lookup.search_address("Sønder Allé 2, 8000 Aarhus C")
        self.assertGreater(len(addresses), 0)
        self.assertTrue(any(a.id == "ab9dc59e-f232-4c9c-9e27-616743d21f8f") for a in addresses)

    def test_pagination(self):
        """Test pagination."""
        # Get 100 addresses at once
        addresses_1 = address_lookup.search_address(municipality_code="0751", results_per_page=100, page=1)

        # Get 100 addresses in chunks
        addresses_2 = []
        for i in range(1, 11):
            addresses_2 += address_lookup.search_address(municipality_code="0751", results_per_page=10, page=i)

        self.assertEqual(len(addresses_1), 100)
        self.assertEqual(len(addresses_2), 100)

        # Check that the lists are equal
        self.assertTrue(all(a.id == b.id for a, b in zip(addresses_1, addresses_2)))


if __name__ == '__main__':
    unittest.main()
