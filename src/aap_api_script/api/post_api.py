from requests import Response

def post_bulk_imp(client, inventory_id: int, host_list: list) -> Response:
    payload = {
        "inventory": inventory_id,
        "hosts": [{"name": host['Hostname']} for host in host_list]
    }

    response = client.post(f"/bulk/host_create/", json=payload)
    return response