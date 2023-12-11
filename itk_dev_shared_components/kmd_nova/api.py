"""This module provides an API to KMD Nova ESDH"""

import functools
import requests

def refresh_token(func):
    """Decorator for refreshing bearer token.
    The token expires after a certain time limit. When the token expires, a new one will be created."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        retries = 0
        while retries < self.max_retries:
            try:
                return func(self, *args, **kwargs)
            except requests.exceptions.HTTPError as error:
                if error.response.status_code == 401:  # Unauthorized (invalid token) # TODO and respone contains
                    self.bearer_token = self._get_new_token()
                    retries += 1
                    # Retry the original function call with the new token
                else:
                    # Re-raise the exception if it's not a token issue
                    raise
        raise RuntimeError(f"Maximum retry limit ({self.max_retries}) reached.")

    return wrapper

class NovaESDH:
    """
    This class gives access to the KMD Nova ESDH API. Get read/write access to documents and journal notes in the system.
    A bearer token is automatically created and updated when the class is instantiated.
    Using api version 1.0.
    """
    DOMAIN = "https://cap-novaapi.kmd.dk"
    def __init__(self, client_id: str, client_secret: str) -> None:
        """
        Args:
            client_id: string
            client_secret: string
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.bearer_token = self._get_new_token()
        self.max_retries = 3  # Adjust this to your desired maximum retry limit

    def _get_new_token(self):
        url = "https://novaauth.kmd.dk/realms/NovaIntegration/protocol/openid-connect/token"
        payload = f"client_secret={self.client_secret}&grant_type=client_credentials&client_id={self.client_id}&scope=client"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        bearer_token = response.json()['access_token']
        return bearer_token

    @refresh_token
    def get_address_by_cpr(self, cpr: str) -> dict:
        """ Gets the address of a citizen from CPR.
        Args:
            cpr: cpr of the citizen

        Returns: dict with the address information

        Raises: requests.exceptions.HTTPError if the request failed.
        """
        url = (f"{self.DOMAIN}/api/Cpr/GetAddressByCpr"
               f"?TransactionId=08d1bfed-703e-49a2-bf5c-933bc35ff127"
               f"&Cpr={cpr}"
               f"&api-version=1.0-Cpr")
        headers = {'Authorization': f"Bearer {self.bearer_token}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        address = response.json()
        return address
