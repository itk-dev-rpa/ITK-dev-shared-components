"""This module is responsible for accessing sites using the Microsoft Graph API."""

from dataclasses import dataclass, field

import requests

from itk_dev_shared_components.graph.authentication import GraphAccess


@dataclass
class Site:
    """A class representing a Site."""

    id: str = field(repr=False)
    name: str
    display_name: str
    description: str
    web_url: str
    created: str
    last_modified: str


def get_site(graph_access: GraphAccess, site_path: str) -> Site:
    """Retrieve properties and relationships for a site resource.
    A site resource represents a team site in SharePoint.

    You need to authorize against Graph to get the GraphAccess before using this function
    see the graph.authentication module.

    See https://learn.microsoft.com/en-us/graph/api/site-get?view=graph-rest-1.0
    for a list of possible site_paths to pass as argument.

    Args:
        graph_access: The GraphAccess object used to authenticate.
        site_path: The path to the team site in SharePoint.

    returns:
        A Site object
    """
    endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_path}"
    response = _get_request(endpoint, graph_access)

    return _unpack_site_response(response.json())


def download_file_contents(graph_access: GraphAccess, site_id: str, drive_item_id: str) -> bytes:
    """Given a site_id, a drive_item_id, and a download destination, downloads a single file from a site resource

    You need to authorize against Graph to get the GraphAccess before using this function
    see the graph.authentication module.

    See https://learn.microsoft.com/en-us/graph/api/driveitem-get-content
    for a list of possible content_urls to pass as argument.

    Args:
        graph_access: The GraphAccess object used to authenticate.
        site_id: The id of the site in SharePoint.
        drive_item_id: The id of the DriveItem in SharePoint.

    returns:
        bytes containing the contents of the file
    """
    endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{drive_item_id}/content"
    response = _get_request(endpoint, graph_access)
    return response.content


def _unpack_site_response(site_raw: dict[str, str]) -> Site:
    """Unpack a json HTTP response and create a Site object.

    Args:
        site_raw: The json dictionary created by response.json().

    Returns:
        Site: A Site object.
    """

    return Site(
        id=site_raw["id"],
        name=site_raw["name"],
        display_name=site_raw["displayName"],
        description=site_raw["description"],
        web_url=site_raw["webUrl"],
        created=site_raw["createdDateTime"],
        last_modified=site_raw["lastModifiedDateTime"],
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
