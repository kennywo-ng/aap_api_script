from requests import Response

def post_bulk_imp(client, inventory_id: int, host_list: list) -> Response:
    payload = {
        "inventory": inventory_id,
        "hosts": [{"name": host['Hostname']} for host in host_list]
    }

    response = client.post("/bulk/host_create/", json=payload)
    return response

def post_grp_host(client, group_id: int, hostname: str) -> Response:
    payload = {
        "name": hostname,
        "enabled": True
    }

    response = client.post(f"/groups/{group_id}/hosts/", json=payload)
    return response