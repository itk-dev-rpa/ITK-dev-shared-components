"""This module has functions to do with cpr related calls
to the KMD Nova api."""

import uuid
import urllib.parse

import requests

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess


def get_address_by_cpr(cpr: str, nova_access: NovaAccess) -> dict:
    """Gets the street address of a citizen by their CPR number.

    Args:
        cpr: CPR number of the citizen.

    Returns:
        A dict with the address information.

    Raises:
        requests.exceptions.HTTPError: If the request failed.
    """

    url = urllib.parse.urljoin(nova_access.domain, "api/Cpr/GetAddressByCpr")
    params = {
        "TransactionId": str(uuid.uuid4()),
        "Cpr": cpr,
        "api-version": "1.0-Cpr"
    }
    headers = {'Authorization': f"Bearer {nova_access.get_bearer_token()}"}

    response = requests.get(url, params=params, headers=headers, timeout=60)
    response.raise_for_status()
    address = response.json()
    return address
