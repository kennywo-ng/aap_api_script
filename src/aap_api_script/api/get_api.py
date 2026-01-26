from .client import APIClient

def get_inv(client) -> dict:
    inventory = list(client.get_pagination(f"/inventories/"))
    return inventory

def get_host(client) -> dict:
    hosts = list(client.get_pagination(f"/hosts/"))
    return hosts

def match_host_to_inv(host_name: list, inventory_list: list) -> dict:
    inv_list = {a['id']: a['name'] for a in inventory_list}
    results = []
    for host in host_name:
        host_to_inv = inv_list.get(host.get('inventory'), 'Unknown Inventory')
        results.append({
            'host_name': host.get('name'),
            'inventory_name': host_to_inv
        })
    return results

def get_host_w_inventory(client) -> dict:
    inventory_host = get_host(client)
    inventory = get_inv(client)
    host_with_inv = match_host_to_inv(inventory_host, inventory)
    return host_with_inv