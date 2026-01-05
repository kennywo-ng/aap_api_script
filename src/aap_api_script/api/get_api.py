from .client import APIClient
from config.settings import (
    API_BASE_URL,
    API_TOKEN,
    API_TIMEOUT,
)

def get_int(base_url: str, token: str, timeout: float) -> dict:
    with APIClient(base_url=base_url, token=token, timeout=timeout) as c:
        inventory = list(c.get_pagination(f"/inventories/"))
    return inventory

def get_host(base_url: str, token: str, timeout: float) -> dict:
    with APIClient(base_url=base_url, token=token, timeout=timeout) as c:
        hosts = list(c.get_pagination(f"/hosts/"))
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

def get_host_w_inventory(base_url: str, token: str, timeout: float) -> dict:
    inventory_host = get_host(base_url, token, timeout)
    inventory = get_int(base_url, token, timeout)
    host_with_inv = match_host_to_inv(inventory_host, inventory)
    return host_with_inv

if __name__ == "__main__":
    host_w_inv = get_host_w_inventory(API_BASE_URL, API_TOKEN, API_TIMEOUT)
    for item in host_w_inv:
            print(f"Host: {item['host_name']:<30} Inventory: {item['inventory_name']}")