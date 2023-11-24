"""This module is responsible for authenticating a Microsoft Graph
connection."""

import msal


# pylint: disable-next=too-few-public-methods
class GraphAccess:
    """An object that handles access to the Graph api.
    This object should not be created directly but instead
    using one of the authorize methods in the graph.authentication module.
    """
    def __init__(self, app: msal.PublicClientApplication, scopes: list[str]) -> str:
        self.app = app
        self.scopes = scopes

    def get_access_token(self):
        """Get the access token to Graph.
        This function automatically reuses an existing token
        or refreshes an expired one.

        Raises:
            RuntimeError: If the access token couldn't be acquired.

        Returns:
            str: The Graph access token.
        """
        account = self.app.get_accounts()[0]
        token = self.app.acquire_token_silent(self.scopes, account)

        if "access_token" in token:
            return token['access_token']

        if 'error_description' in token:
            raise RuntimeError(f"Token could not be acquired. {token['error_description']}")

        raise RuntimeError("Something went wrong. No error description was returned from Graph.")


def authorize_by_username_password(username: str, password: str, *, client_id: str, tenant_id: str) -> GraphAccess:
    """Get a bearer token for the given user.
    This is used in most other Graph API calls.

    Args:
        username: The username of the user (email address).
        password: The password of the user.
        client_id: The Graph API client id in 8-4-4-12 format.
        tenant_id: The Graph API tenant id in 8-4-4-12 format.

    Returns:
        GraphAccess: The GraphAccess object used to authorize Graph access.
    """
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scopes = ["https://graph.microsoft.com/.default"]

    app = msal.PublicClientApplication(client_id, authority=authority)
    app.acquire_token_by_username_password(username, password, scopes)

    graph_access = GraphAccess(app, scopes)

    # Test connection
    graph_access.get_access_token()

    return graph_access
