"""This module is responsible for accessing sites using the Microsoft Graph API."""

from dataclasses import dataclass, field

from itk_dev_shared_components.graph.authentication import GraphAccess
from itk_dev_shared_components.graph.common import get_request, put_request


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
    response = get_request(endpoint, graph_access)

    return _unpack_site_response(response.json())


def download_file_contents(graph_access: GraphAccess, site_id: str, drive_item_id: str) -> bytes:
    """Given a site_id, a drive_item_id, and a download destination, downloads a single file from a site resource

    You need to authorize against Graph to get the GraphAccess before using this function
    see the graph.authentication module.

    See https://learn.microsoft.com/en-us/graph/api/driveitem-get-content for further documentation

    Args:
        graph_access: The GraphAccess object used to authenticate.
        site_id: The id of the site in SharePoint.
        drive_item_id: The id of the DriveItem in SharePoint.

    returns:
        bytes containing the contents of the file
    """
    endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{drive_item_id}/content"
    response = get_request(endpoint, graph_access)
    return response.content


def upload_file_contents(graph_access: GraphAccess, site_id: str, drive_item_path: str, file_contents: bytes):
    """Given a site_id, a drive_item_path, and file_contents as bytes, uploads a single file to a site

    You need to authorize against Graph to get the GraphAccess before using this function
    see the graph.authentication module.

    See https://learn.microsoft.com/en-us/graph/api/driveitem-put-content for further documentation

    Args:
        graph_access: The GraphAccess object used to authenticate.
        site_id: The id of the site in SharePoint.
        drive_item_path: The path to upload the file contents to.
        file_contents: A bytes object containing the file's contents.

    """

    endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{drive_item_path}:/content"
    put_request(endpoint, graph_access, file_contents)


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
