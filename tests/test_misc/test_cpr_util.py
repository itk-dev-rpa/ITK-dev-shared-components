"""Tests relating to the module misc.cpr_util."""

import unittest
from datetime import date

from itk_dev_shared_components.misc import cpr_util


class TestCprUtil(unittest.TestCase):
    """Tests relating to the module misc.cpr_util."""

    def test_get_age_from_cpr(self):
        """Test getting the age from a cpr number."""
        # A table of fictional cpr-numbers and the expected age at the date.
        test_data = (
            ("0101920000", 32),
            ("0101921000", 32),
            ("0101922000", 32),
            ("0101923000", 32),
            ("0101154000", 9),
            ("0101924000", 32),
            ("0101155000", 9),
            ("0101925000", 132),
            ("0101156000", 9),
            ("0101926000", 132),
            ("0101157000", 9),
            ("0101927000", 132),
            ("0101158000", 9),
            ("0101928000", 132),
            ("0101159000", 9),
            ("0101929000", 32),
        )

        date_ = date(2024, 2, 9)

        for cpr, age in test_data:
            with self.subTest(cpr=cpr, date=date_, age=age):
                self.assertEqual(cpr_util.get_age(cpr, date_), age)

        with self.assertRaises(ValueError):
            cpr_util.get_age("010190-1234")

        with self.assertRaises(ValueError):
            cpr_util.get_age("010190xxxx")


if __name__ == '__main__':
    unittest.main()
