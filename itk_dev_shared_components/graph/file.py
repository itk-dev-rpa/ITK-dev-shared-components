"""This module is responsible for accessing files using the Microsoft Graph API."""

from dataclasses import dataclass, field

import requests

from itk_dev_shared_components.graph.authentication import GraphAccess


# TODO: Add more properties
@dataclass
class DriveItem:
    """A class representing a DriveItem."""

    id: str = field(repr=False)
    name: str
    web_url: str
    last_modified: str


def get_drive_item(graph_access: GraphAccess, site_id: str, drive_item_path: str) -> str:
    """Given a site id and a drive_item_path, gets the corresponding DriveItem

    You need to authorize against Graph to get the GraphAccess before using this function
    see the graph.authentication module.

    See https://learn.microsoft.com/en-us/graph/api/driveitem-get for further documentation

    Args:
        graph_access: The GraphAccess object used to authenticate.
        site_id: The id of the site in SharePoint.
        drive_item_path: The path to the DriveItem in SharePoint.
    """
    endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{drive_item_path}"
    response = _get_request(endpoint, graph_access)
    raw_response = response.json()

    return _unpack_drive_item_response(raw_response)


def _unpack_drive_item_response(drive_item_raw: dict[str, str]) -> DriveItem:
    """Unpack a json HTTP response and create a DriveItem object.

    Args:
        drive_item_raw: The json dictionary created by response.json().

    Returns:
        DriveItem: A DriveItem object.
    """

    return DriveItem(
        id=drive_item_raw["id"],
        name=drive_item_raw["name"],
        web_url=drive_item_raw["webUrl"],
        last_modified=drive_item_raw["lastModifiedDateTime"],
    )


def _get_request(endpoint: str, graph_access: GraphAccess) -> requests.models.Response:
    """Sends a get request to the given Graph endpoint using the GraphAccess
    and returns the json object of the response.

    Args:
        endpoint: The URL of the Graph endpoint.
        graph_access: The GraphAccess object used to authenticate.

    Returns:
        Response: The response object of the GET request.

    Raises:
        HTTPError: Any errors raised while performing GET request.
    """
    token = graph_access.get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(endpoint, headers=headers, timeout=30)
    response.raise_for_status()

    return response
