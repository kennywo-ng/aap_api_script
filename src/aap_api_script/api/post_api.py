from .client import APIClient
from requests import Response

def post_bulk_imp(base_url: str, token: str, timeout: float, inventory_id: int, host_list: list) -> Response:
    payload = {
        "inventory": inventory_id,
        "hosts": [{"name": host['Hostname']} for host in host_list]
    }

    c = APIClient(base_url=base_url, token=token, timeout=timeout)
    response = c.post(f"/bulk/host_create/", json=payload)
    return response