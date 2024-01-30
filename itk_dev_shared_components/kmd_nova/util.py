"""This module contains helper functions regarding the KMD Nova API."""

from datetime import datetime
from typing import Optional


def datetime_from_iso_string(date_string: Optional[str]) -> Optional[datetime]:
    """A helper function to convert an ISO date string to a datetime.
    If the date string is None, None is returned.

    Args:
        date_string: A date string in ISO format.

    Returns:
        A datetime object representing the date string.
    """
    if not date_string:
        return None

    return datetime.fromisoformat(date_string)
