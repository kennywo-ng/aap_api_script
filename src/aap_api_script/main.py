from api.client import APIClient
from config.settings import (
    API_BASE_URL,
    API_TOKEN,
    API_TIMEOUT,
)

# def test(inv: int):
#     with APIClient(base_url=API_BASE_URL, token=API_TOKEN, timeout=API_TIMEOUT) as c:
#         hosts = list(c.get_pagination(f"/inventories/{inv}/hosts/"))
#     print(hosts)



def get_int() -> dict:
    with APIClient(base_url=API_BASE_URL, token=API_TOKEN, timeout=API_TIMEOUT) as c:
        inventory = list(c.get_pagination(f"/inventories/"))
    return inventory

def get_inv_host(inv: int) -> dict:
    with APIClient(base_url=API_BASE_URL, token=API_TOKEN, timeout=API_TIMEOUT) as c:
        hosts = list(c.get_pagination(f"/inventories/{inv}/hosts/"))
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


def main():
    print("""
    1. Print inventory hosts
    2
    3
    4
    """)

    choice = input("Enter your choice: ")

    if choice == "1":
        inventory_host = get_inv_host(6)
        inventory = get_int()
        host_with_inv = match_host_to_inv(inventory_host, inventory)
        print(host_with_inv)

        # for item in inventory['results']:
        #     print(item['name'])
        

if __name__ == "__main__":
    main()

# excel functions module
# display instruction
# 1. 