from api.client import APIClient
from api import get_host_w_inventory, get_inv, get_inv_group, post_bulk_imp, post_grp_host
from config.settings import (
    API_BASE_URL,
    API_TOKEN,
    API_TIMEOUT,
    AUTH_PASSWORD,
    AUTH_USERNAME,
    DOMAIN_NAME,
    ENV,
)

import pandas
import json
import sys

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

def match_hosts(excel_list, aap_inv_list):
    lookup = {item["host_name"]: item["inventory_name"] for item in aap_inv_list}
    
    result = []
    for item in excel_list:
        host = item['Hostname']
        if host in lookup:
            result.append({
                "host_name": host,
                "inventory_name": lookup[host]
                })
        else:
            result.append({
                "host_name": host,
                "inventory_name": "Not Found"
                })
    
    return result

def excel_parse_hostname(file_path: str) -> dict:
    excel = pandas.read_excel(file_path, engine='openpyxl').to_json(orient='records')
    excel = json.loads(excel)
    for item in excel:
        if DOMAIN_NAME not in item['Hostname']:
            item['Hostname'] = f"{item['Hostname']}.{DOMAIN_NAME}"
    return excel

def sel_id(inv: list, type: str) -> list | None:
    print(
        f"\nWhich {type} to add hosts to?\n"
        f"{'ID':<5}{type} Name"
    )

    for item in inv:
        print(f"{item['id']:<5}{item['name']}")

    inv_id = None
    while inv_id is None:
        try:
            inv_id = int(input(f"\nEnter {type} ID: "))
        except ValueError:
            print("Invalid input. Please enter a valid ID.")

    inv_id_match = next((i for i in inv if i['id'] == inv_id), None)

    return inv_id_match

def main():
    print("""
    1. Print inventory hosts with inventory names
    2. Compare hosts from excel with inventory hosts
    3. Bulk import hosts to inventory
    4. Group hosts
    """)

    choice = input("Enter your choice: ")
    print("\n")

    if choice == "1":
        host_w_inv = get_host_w_inventory(client)
        for item in host_w_inv:
            print(f"Host: {item['host_name']:<40} Inventory: {item['inventory_name']}")
        
    elif choice == "2":
        exc_host = excel_parse_hostname('excels/host_check.xlsx')
        host_w_inv = get_host_w_inventory(client)
        matches = match_hosts(exc_host, host_w_inv)

        for item in sorted(matches, key=lambda x: x['inventory_name']):
            print(f"Host: {item['host_name']:<40} Inventory: {item['inventory_name']}")

    elif choice == "3":
        excel_bulk_host = excel_parse_hostname('excels/host_bulk_import.xlsx')
        aap_inv = get_inv(client)
        selected_inv = None

        while selected_inv is None:
            selected_inv = sel_id(aap_inv, "inventory")

            if selected_inv:
                print("\nWould you like to add the following hosts to: " + selected_inv['name'])
            else:
                print("\nInventory ID not found. Please try again.")

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

    elif choice == "4":
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
        host_w_inv = get_host_w_inventory(client)

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

        while True:
            confirm = input("\nConfirm? (y/n): ").strip().lower()

            if confirm == 'y':
                break
            elif confirm == 'n':
                sys.exit("Operation cancelled.")
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        
        for host in exc_group_host:
            resp = post_grp_host(client, selected_grp['id'], host['Hostname'])
            if resp.status_code in range(200, 300):
                print(f"Added host {host['Hostname']} to group {selected_grp['name']}.")
            else:
                print(f"Failed to add host {host['Hostname']}. {resp.json()}")

    else:
        print("Invalid choice.")
        main()

if __name__ == "__main__":
    main()
