"""This module contains functions to look up addresses in DAWA.
https://dawadocs.dataforsyningen.dk/dok/api/
"""

from dataclasses import dataclass, field

import requests


@dataclass
# pylint: disable-next=too-many-instance-attributes
class Address:
    """A dataclass representing an address."""
    street: str
    number: str
    floor: str
    door: str
    minor_city: str
    postal_city: str
    postal_code: str
    municipality_code: str
    address_text: str
    id: str = field(repr=False)


def search_address(query: str | None = None, street: str | None = None, number: str | None = None,
                   postal_code: str | None = None, municipality_code: str | None = None,
                   results_per_page: int = 100, page: int = 1) -> list[Address]:
    """Search for an address in the DAWA API.

    Args:
        query: The free text to search for.
        street: The exact street of the address.
        number: The exact number of the address.
        postal_code: The exact postal code of the address.
        municipality_code: The exact municipality code of the address.
        results_per_page: The number of results to fetch per page.
        page: The 1-based page of results to fetch.

    Returns:
        A list of address objects describing the addresses found.
    """
    url = "https://api.dataforsyningen.dk/adresser"

    params = {
        'struktur': 'mini',
        'per_side': results_per_page,
        'side': page
    }
    if query:
        params['q'] = query
    if street:
        params['vejnavn'] = street
    if number:
        params['husnr'] = number
    if postal_code:
        params['postnr'] = postal_code
    if municipality_code:
        params['kommunekode'] = municipality_code

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    addresses = []
    for a in response.json():
        address = Address(
            street=a['vejnavn'],
            number=a['husnr'],
            floor=a['etage'],
            door=a['dør'],
            minor_city=a['supplerendebynavn'],
            postal_city=a['postnrnavn'],
            postal_code=a['postnr'],
            municipality_code=a['kommunekode'],
            address_text=a['betegnelse'],
            id=a['id']
        )
        addresses.append(address)

    return addresses
