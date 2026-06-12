"""This module has functions related to calls
to the Virk CVR API."""

from dataclasses import dataclass
from datetime import date, datetime

import requests
from requests.auth import HTTPBasicAuth


@dataclass
class Company:
    """A dataclass representing a company."""
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
        ValueError: If more than one company is found on the given cvr number.
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

    company_dict = response_json['hits']['hits'][0]['_source']['Vrvirksomhed']
    return _unpack_company_dict(company_dict)


def cvr_mass_lookup(cvr_list: list[str], match_length: bool, username: str, password: str) -> list[Company]:
    """Look up multiple companies based on a list of cvr numbers.

    Args:
        cvr_list: The list of cvr numbers to look up.
        match_length: Whether the number results must match the number of inputs.
        username: The username to the cvr api.
        password: The password to the cvr api.

    Raises:
        ValueError: If match_length is true and the number of results doesn't match.

    Returns:
        A list of company objects describing the found companies.
        The list is sorted to match the input list.
    """
    url = "http://distribution.virk.dk/cvr-permanent/virksomhed/_search"
    headers = {
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth(username, password)

    data = {
        "_source": ["Vrvirksomhed.virksomhedMetadata", "Vrvirksomhed.cvrNummer"],
        "query": {
            "terms": {
                "Vrvirksomhed.cvrNummer": cvr_list
            }
        }
    }

    response = requests.post(url, headers=headers, auth=auth, json=data, timeout=5)
    response.raise_for_status()

    response_json = response.json()

    if match_length and response_json['hits']['total'] != len(cvr_list):
        raise ValueError(f"The number of companies found didn't match the input list: {len(cvr_list)} != {response_json['hits']['total']}")

    companies = []

    for hit in response_json['hits']['hits']:
        company_dict = hit['_source']['Vrvirksomhed']
        companies.append(_unpack_company_dict(company_dict))

    # Sort to match input list
    companies.sort(key=lambda c: cvr_list.index(c.cvr))

    return companies


def _unpack_company_dict(company_dict: dict) -> Company:
    """Unpack a response dict to a company object.

    Args:
        company_dict: The company dict from the cvr api.
        cvr: The cvr number of the company.

    Returns:
        A company object describing the found company.
    """
    cvr = str(company_dict['cvrNummer'])
    company_dict = company_dict['virksomhedMetadata']
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
