"""This module provides an API to KMD Nova ESDH"""

import datetime
import uuid
import json
import requests

from itk_dev_shared_components.kmd_nova.case import NovaCase, CaseParty


class NovaESDH:
    """
    This class gives access to the KMD Nova ESDH API. Get read/write access to documents and journal notes in the system.
    A bearer token is automatically created and updated when the class is instantiated.
    Using api version 1.0.
    The api docs can be found here: https://novaapi.kmd.dk/swagger/index.html
    """

    DOMAIN = "https://cap-novaapi.kmd.dk"
    TIMEOUT = 60

    def __init__(self, client_id: str, client_secret: str) -> None:
        """
        Args:
            client_id: string
            client_secret: string
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self._bearer_token, self.token_expiry_date = self._get_new_token()

    def _get_new_token(self) -> tuple[str, datetime.datetime]:
        """
        This method requests a new token from the API.
        When the token expiry date is passed, requests with the token to the API will return HTTP 401 status code.

        Returns:
            tuple: token and expiry datetime

        Raises:
            requests.exceptions.HTTPError if the request failed.
        """

        url = "https://novaauth.kmd.dk/realms/NovaIntegration/protocol/openid-connect/token"
        payload = f"client_secret={self.client_secret}&grant_type=client_credentials&client_id={self.client_id}&scope=client"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url, headers=headers, data=payload, timeout=self.TIMEOUT)
        response.raise_for_status()
        bearer_token = response.json()['access_token']
        token_life_seconds = response.json()['expires_in']
        token_expiry_date = datetime.datetime.now() + datetime.timedelta(seconds=int(token_life_seconds))
        return bearer_token, token_expiry_date

    def get_bearer_token(self) -> str:
        """Return the bearer token. If the token is about to expire,
         a new token is requested form the auth service.

         Returns: Bearer token
         """

        if self.token_expiry_date + datetime.timedelta(seconds=30) < datetime.datetime.now():
            self._bearer_token, self.token_expiry_date = self._get_new_token()

        return self._bearer_token

    def get_address_by_cpr(self, cpr: str) -> dict:
        """Gets the street address of a citizen by their CPR number.
        Args:
            cpr: CPR of the citizen

        Returns:
            dict with the address information

        Raises:
            requests.exceptions.HTTPError if the request failed.
        """

        url = (f"{self.DOMAIN}/api/Cpr/GetAddressByCpr"
               f"?TransactionId={uuid.uuid4()}"
               f"&Cpr={cpr}"
               f"&api-version=1.0-Cpr")
        headers = {'Authorization': f"Bearer {self.get_bearer_token()}"}

        response = requests.get(url, headers=headers, timeout=self.TIMEOUT)
        response.raise_for_status()
        address = response.json()
        return address

    def get_cases(self, cpr: str = None, case_number: str = None, case_title: str = None) -> list[NovaCase]:
        """Search for cases on different search terms.
        Currently supports search on cpr number, case number and case title. At least one search term should be given.
        Currently limited to find 100 cases.

        Args:
            cpr: The cpr number to search on. E.g. "0123456789"
            case_number: The case number to search on. E.g. "S2022-12345"
            case_title: The case title to search on.

        Returns:
            A list of NovaCase objects.

        Raises:
            ValueError: If no search terms are given.
        """

        if not any((cpr, case_number, case_title)):
            raise ValueError("No search terms given.")

        url = f"{self.DOMAIN}/api/Case/GetList?api-version=1.0-Case"

        payload = {
            "common":
                {
                    "transactionId": str(uuid.uuid4())
                },
            "paging":
                {
                    "startRow": 1,
                    "numberOfRows": 100
                },
            "caseAttributes":
                {
                    "userFriendlyCaseNumber": case_number,
                    "title": case_title
                },
            "caseParty":
                {
                    "identificationType": "CprNummer",
                    "identification": cpr
                },
            "caseGetOutput":
                {
                    "numberOfSecondaryParties": True,
                    "caseParty":
                        {
                            "identificationType": True,
                            "identification": True,
                            "partyRole": True,
                            "name": True
                        },
                    "caseAttributes":
                        {
                            "title": True,
                            "userFriendlyCaseNumber": True,
                            "caseDate": True
                        }
                }
        }

        payload = json.dumps(payload)

        headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {self.get_bearer_token()}"}

        response = requests.put(url, headers=headers, data=payload, timeout=self.TIMEOUT)
        response.raise_for_status()

        # Convert json to NovaCase objects
        cases = []
        for case_dict in response.json()['cases']:
            parties = []
            for party_dict in case_dict['caseParties']:
                party = CaseParty(
                    identification_type = party_dict['identificationType'],
                    identification = party_dict['identification'],
                    role = party_dict['partyRole'],
                    name = party_dict['name'],
                )
                parties.append(party)

            case = NovaCase(
                uuid = case_dict['common']['uuid'],
                title = case_dict['caseAttributes']['title'],
                case_date = case_dict['caseAttributes']['caseDate'],
                case_number = case_dict['caseAttributes']['userFriendlyCaseNumber'],
                case_parties=parties
            )

            cases.append(case)

        return cases
