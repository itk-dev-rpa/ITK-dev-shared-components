"""This module contains functionality to authenticate against the KMD Nova api."""

from datetime import datetime, timedelta
import urllib

import requests


# pylint: disable-next=too-few-public-methods
class NovaAccess:
    """An object that handles access to the KMD Nova api."""
    def __init__(self, client_id: str, client_secret: str, domain: str = "https://cap-novaapi.kmd.dk") -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self._bearer_token, self.token_expiry_date = self._get_new_token()
        self.domain = domain

    def _get_new_token(self) -> tuple[str, datetime]:
        """
        This method requests a new token from the API.
        When the token expiry date is passed, requests with the token to the API will return HTTP 401 status code.

        Returns:
            tuple: token and expiry datetime

        Raises:
            requests.exceptions.HTTPError: If the request failed.
        """

        url = "https://novaauth.kmd.dk/realms/NovaIntegration/protocol/openid-connect/token"
        payload = {
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "scope": "client"
        }
        payload = urllib.parse.urlencode(payload)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url, headers=headers, data=payload, timeout=60)
        response.raise_for_status()
        response_json = response.json()
        bearer_token = response_json['access_token']
        token_life_seconds = response_json['expires_in']
        token_expiry_date = datetime.now() + timedelta(seconds=int(token_life_seconds))
        return bearer_token, token_expiry_date

    def get_bearer_token(self) -> str:
        """Return the bearer token. If the token is about to expire,
         a new token is requested form the auth service.

         Returns:
            Bearer token
         """

        if self.token_expiry_date + timedelta(seconds=30) < datetime.now():
            self._bearer_token, self.token_expiry_date = self._get_new_token()

        return self._bearer_token
