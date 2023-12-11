"""This module provides an API to KMD Nova ESDH"""

import datetime
import uuid
import json
import requests


class NovaESDH:
    """
    This class gives access to the KMD Nova ESDH API. Get read/write access to documents and journal notes in the system.
    A bearer token is automatically created and updated when the class is instantiated.
    Using api version 1.0.
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
               f"?TransactionId=08d1bfed-703e-49a2-bf5c-933bc35ff127"
               f"&Cpr={cpr}"
               f"&api-version=1.0-Cpr")
        headers = {'Authorization': f"Bearer {self.get_bearer_token()}"}

        response = requests.get(url, headers=headers, timeout=self.TIMEOUT)
        response.raise_for_status()
        address = response.json()
        return address

    def get_cases_by_case_number(self, case_number: str, paginate_start=1, paginate_cound=5) -> dict:
        """
        Gets all the cases on a given case number. Default pagination is page 1 through 5.
        A UUID is generated as part of the request.
        Args:
            case_number: Case number from Nova ESDH. E.g. "S2022-12345"

        Returns: dict with the cases
        """

        url = f"{self.DOMAIN}/api/Case/GetList?api-version=1.0-Case"

        payload = json.dumps({
            "common":
                {
                    "transactionId": str(uuid.uuid4())
                },
            "paging":
                {
                    "startRow": paginate_start,
                    "numberOfRows": paginate_cound
                },
            "caseAttributes":
                {
                    "userFriendlyCaseNumber": case_number
                },
            "caseGetOutput":
                {
                    "numberOfSecondaryParties": True,
                    "caseParty":
                        {
                            "identificationType": True,
                            "identification": True,
                            "partyRole": True,
                            "name": True,
                            "participantContactInformation": True,
                            "partyRoleName": True
                        },
                    "caseAttributes":
                        {
                            "title": True,
                            "userFriendlyCaseNumber": True
                        }
                }
        })
        headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {self.get_bearer_token()}"}

        response = requests.put(url, headers=headers, data=payload, timeout=self.TIMEOUT)
        response.raise_for_status()
        cases = response.json()
        return cases
