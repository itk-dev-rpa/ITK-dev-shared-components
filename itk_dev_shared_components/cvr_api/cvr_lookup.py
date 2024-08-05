"""This module has functions related to calls
to the Virk CVR API."""

from dataclasses import dataclass
from datetime import date, datetime

import requests
from requests.auth import HTTPBasicAuth


@dataclass
class Company:
    cvr: str
    name: str
    founded_date: date
    address: str
    postal_code: str
    city: str
    company_type: str


def cvr_lookup(cvr: str, username: str, password: str) -> Company:
    """Look up a company based on a CVR number.

    Args:
        cvr: The cvr number of the company to look up.
        username: The username to the cvr api.
        password: The password to the cvr api.

    Raises:
        ValueError: If no company is found on the given cvr number.
        ValueError: If more than one company is found on the given cpr number.
        RuntimeError: If a company with a different cvr number is found.

    Returns:
        A company object describing the found company.
    """
    url = "http://distribution.virk.dk/cvr-permanent/virksomhed/_search"
    headers = {
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth(username, password)

    data = {
        "_source": ["Vrvirksomhed.virksomhedMetadata", "Vrvirksomhed.cvrNummer"],
        "query": {
            "term": {
                "Vrvirksomhed.cvrNummer": cvr
            }
        }
    }

    response = requests.post(url, headers=headers, auth=auth, json=data, timeout=5)
    response.raise_for_status()

    response_json = response.json()

    if response_json['hits']['total'] == 0:
        raise ValueError("No companies found on the given cvr.")
    if response_json['hits']['total'] > 1:
        raise ValueError("More than one company found on the given cvr.")

    cvr_result = str(response_json['hits']['hits'][0]['_source']['Vrvirksomhed']['cvrNummer'])
    if cvr_result != cvr:
        raise RuntimeError("The resulting cvr number didn't match the searched cvr number.")

    company_dict = response_json['hits']['hits'][0]['_source']['Vrvirksomhed']['virksomhedMetadata']
    return _unpack_company_dict(company_dict, cvr_result)


def _unpack_company_dict(company_dict: dict, cvr: str) -> Company:
    """Unpack a response dict to a company object.

    Args:
        company_dict: The company dict from the cvr api.
        cvr: The cvr number of the company.

    Returns:
        A company object describing the found company.
    """
    address, postal_code, city = _parse_address(company_dict['nyesteBeliggenhedsadresse'])
    return Company(
        cvr=cvr,
        name=company_dict['nyesteNavn']['navn'],
        founded_date=datetime.strptime(company_dict['stiftelsesDato'], "%Y-%m-%d").date(),
        address=address,
        postal_code=postal_code,
        city=city,
        company_type=company_dict['nyesteVirksomhedsform']['langBeskrivelse']
    )


def _parse_address(address_dict: dict) -> tuple[str, str, str]:
    """Parse and format the address of a company.

    Args:
        address_dict: The dictionary describing the address.

    Returns:
        A tuple of address, postal code and city.
    """
    address = ""

    if address_dict['conavn']:
        address += f"C/O {address_dict['conavn']}, "

    address += address_dict['vejnavn']
    address += f" {address_dict['husnummerFra']}"

    if address_dict['husnummerTil']:
        address += f"-{address_dict['husnummerTil']}"

    if address_dict['bogstavFra']:
        address += address_dict['bogstavFra']
    if address_dict['bogstavTil']:
        address += f"-{address_dict['bogstavTil']}"

    if address_dict['etage']:
        address += f", {address_dict['etage']}."
    if address_dict['sidedoer']:
        address += f" {address_dict['sidedoer']}"

    return address, str(address_dict['postnummer']), address_dict['postdistrikt']
