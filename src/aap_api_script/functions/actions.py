from api.client import APIClient
from config.settings import (
    API_BASE_URL,
    API_TOKEN,
    API_TIMEOUT,
    AUTH_PASSWORD,
    AUTH_USERNAME,
    ENV,
)

from .helpers import (
    excel_parse_hostname,
    match_hosts,
    sel_id
)
from api import (
    get_host_w_inventory,
    get_inv,
    get_inv_group,
    post_bulk_imp,
    post_grp_host
)

if ENV == "prod":
    client = APIClient(
        base_url=API_BASE_URL,
        username=AUTH_USERNAME,
        password=AUTH_PASSWORD,
        timeout=API_TIMEOUT
    )
elif ENV == "stage":
    client = APIClient(
        base_url=API_BASE_URL,
        token=API_TOKEN,
        timeout=API_TIMEOUT
    )

import sys

def func_1():
    host_w_inv = get_host_w_inventory(client)
    for item in host_w_inv:
        print(f"Host: {item['host_name']:<40} Inventory: {item['inventory_name']}")

def func_2():
    exc_host = excel_parse_hostname('excels/host_check.xlsx')
    host_w_inv = get_host_w_inventory(client)
    matches = match_hosts(exc_host, host_w_inv)

    for item in sorted(matches, key=lambda x: x['inventory_name']):
        print(f"Host: {item['host_name']:<40} Inventory: {item['inventory_name']}")

def func_3():
    excel_bulk_host = excel_parse_hostname('excels/host_bulk_import.xlsx')
    aap_inv = get_inv(client)
    selected_inv = None

    while selected_inv is None:
        selected_inv = sel_id(aap_inv, "inventory")

        if not selected_inv:
            print("\nInventory ID not found. Please try again.")
        
        print("\nWould you like to add the following hosts to: " + selected_inv['name'])

    for host in excel_bulk_host:
        print(f"- {host['Hostname']}")

    while True:
        confirm = input("\nConfirm? (y/n): ").strip().lower()

        if confirm == 'y':
            break
        elif confirm == 'n':
            sys.exit("Operation cancelled.")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    import_bulk = post_bulk_imp(client, selected_inv['id'], excel_bulk_host)

    if import_bulk.status_code in range(200, 300):
        print("Status code: " + str(import_bulk.status_code))
    else:
        print(f"Failed to import hosts. {import_bulk.json()['__all__']}")

def func_4():
    exc_group_host = excel_parse_hostname('excels/host_grouping.xlsx')
    aap_inv = get_inv(client)
    selected_inv = None
    selected_grp = None

    while selected_inv is None:
        selected_inv = sel_id(aap_inv, "inventory")
        if selected_inv:
            break
        else:
            print("\nInventory ID not found. Please try again.")

    aap_inv_groups = get_inv_group(client, selected_inv['id'])

    while selected_grp is None:
        selected_grp = sel_id(aap_inv_groups, "group")
        if selected_grp:
            break
        else:
            print("\nGroup ID not found. Please try again.")

    print(f"\nInventory: {selected_inv['name']} \nGroup: {selected_grp['name']} ")
    print("Hosts to be added to group:")
    for host in exc_group_host:
        print(f"- {host['Hostname']}")

    confirm = input("\nConfirm? (y/n): ").strip().lower()

    if confirm not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'.")
        return

    if confirm == 'n':
        print("Cancelled.")
        return
    
    for host in exc_group_host:
        resp = post_grp_host(client, selected_grp['id'], host['Hostname'])
        if resp.status_code in range(200, 300):
            print(f"Added host {host['Hostname']} to group {selected_grp['name']}.")
        else:
            print(f"Failed to add host {host['Hostname']}. {resp.json()}")