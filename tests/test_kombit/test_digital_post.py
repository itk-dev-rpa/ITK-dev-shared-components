"""Tests of the Kombit Digital Post API."""
import unittest
import os

from dotenv import load_dotenv

from itk_dev_shared_components.kombit.authentication import KombitAccess
from itk_dev_shared_components.kombit import digital_post


load_dotenv()


class DigitalPostTest(unittest.TestCase):
    """Test Digital Post functionality in the Kombit API."""

    def test_is_registered(self):
        """Test authentication."""
        cvr = os.environ["KOMBIT_TEST_CVR"]
        cert_path = os.environ["KOMBIT_TEST_CERT_PATH"]
        ka = KombitAccess(cvr=cvr, cert_path=cert_path, test=True)

        # Fictional test cpr
        cpr = "2611740000"

        result = digital_post.is_registered(cpr=cpr, service="digitalpost", kombit_access=ka)
        self.assertTrue(result)

        result = digital_post.is_registered(cpr=cpr, service="nemsms", kombit_access=ka)
        self.assertFalse(result)

        # Test with nonsense.
        # This should result in False
        result = digital_post.is_registered(cpr="FooBar", service="digitalpost", kombit_access=ka)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
