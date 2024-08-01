"""This module contains common functions like HTTP request wrappers which are used across other modules."""

from typing import Any

import requests

from itk_dev_shared_components.graph.authentication import GraphAccess


def get_request(endpoint: str, graph_access: GraphAccess) -> requests.models.Response:
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


def put_request(endpoint: str, graph_access: GraphAccess, data: Any) -> requests.models.Response:
    """Sends a put request to the given Graph endpoint using the GraphAccess
    and returns the json object of the response.

    Args:
        endpoint: The URL of the Graph endpoint.
        data: The data to send in the request.
        graph_access: The GraphAccess object used to authenticate.

    Returns:
        Response: The response object of the PUT request.

    Raises:
        HTTPError: Any errors raised while performing PUT request.
    """
    token = graph_access.get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.put(endpoint, headers=headers, data=data, timeout=30)
    response.raise_for_status()

    return response
