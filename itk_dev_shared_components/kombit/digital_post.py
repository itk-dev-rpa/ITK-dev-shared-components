import uuid
from datetime import datetime
from typing import Literal

import requests

from itk_dev_shared_components.kombit.authentication import KombitAccess


def is_registered(cpr: str, service: Literal['digitalpost', 'nemsms'], kombit_access: KombitAccess) -> bool:
    """Check if the person with the given cpr number is registered for
    either Digital Post or NemSMS.

    Args:
        cpr: The cpr number of the person to look up.
        service: The service to look up for.
        kombit_access: The KombitAccess object used to authenticate.

    Returns:
        True if the person is registered for Digital Post.
    """
    url = f"https://prod.serviceplatformen.dk/service/PostForespoerg_1/{service}"

    parameters = {
        "cprNumber": cpr
    }

    headers = {
        "X-TransaktionsId": str(uuid.uuid4()),
        "X-TransaktionsTid": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "authorization": kombit_access.get_access_token("http://entityid.kombit.dk/service/postforespoerg/1")
    }

    response = requests.get(url, params=parameters, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()['result']
