from .client import APIClient

def get_inv(client) -> list:
    inventory = list(client.get_pagination("/inventories/"))
    return inventory

def get_host(client) -> list:
    hosts = list(client.get_pagination("/hosts/"))
    return hosts

def get_inv_group(client, inv_id: int) -> list:
    groups = list(client.get_pagination(f"/inventories/{inv_id}/groups/"))
    return groups

def match_host_to_inv(host_name: list, inventory_list: list) -> list:
    inv_list = {a['id']: a['name'] for a in inventory_list}
    results = []
    for host in host_name:
        host_to_inv = inv_list.get(host.get('inventory'), 'Unknown Inventory')
        results.append({
            'host_name': host.get('name'),
            'inventory_name': host_to_inv
        })
    return results

def get_host_w_inventory(client) -> list:
    inventory_host = get_host(client)
    inventory = get_inv(client)
    host_with_inv = match_host_to_inv(inventory_host, inventory)
    return host_with_inv