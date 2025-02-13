"""This module contains helper functions regarding the KMD Nova API."""

from datetime import datetime
from typing import Optional

from itk_dev_shared_components.kmd_nova.nova_objects import Caseworker


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


def datetime_to_iso_string(datetime_: Optional[datetime]) -> Optional[str]:
    """A helper function to convert a datetime to an ISO formatted string.
    If the the datetime is None, None is returned.

    Args:
        datetime_: The datetime object to convert.

    Returns:
        A datetime string in ISO format.
    """
    if datetime_:
        return datetime_.isoformat()

    return None


def extract_caseworker(response_dict: dict) -> Caseworker | None:
    """Extract the case worker from a HTTP request response.
    If the case worker is in a unexpected format, None is returned.

    Args:
        response_dict: The dictionary describing the response object.

    Returns:
        A case worker object describing the case worker if any.
    """
    try:
        if 'caseworker' in response_dict:
            if 'kspIdentity' in response_dict['caseworker']:
                return Caseworker(
                    uuid = response_dict['caseworker']['kspIdentity']['novaUserId'],
                    name = response_dict['caseworker']['kspIdentity']['fullName'],
                    ident = response_dict['caseworker']['kspIdentity']['racfId'],
                    type='user'
                )

            if 'losIdentity' in response_dict['caseworker']:
                return Caseworker(
                    uuid = response_dict['caseworker']['losIdentity']['novaUnitId'],
                    name = response_dict['caseworker']['losIdentity']['fullName'],
                    ident = str(response_dict['caseworker']['losIdentity']['administrativeUnitId']),
                    type='group'
                )

    except KeyError:
        pass

    return None
