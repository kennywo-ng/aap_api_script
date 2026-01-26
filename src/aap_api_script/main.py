from api.client import APIClient
from api import get_host_w_inventory, get_inv, post_bulk_imp
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

def main():
    print("""
    1. Print inventory hosts with inventory names
    2. Compare hosts from excel with inventory hosts
    3. Bulk import hosts to inventory
    4. 
    """)

    choice = input("Enter your choice: ")
    print("\n")

    if choice == "1":
        host_w_inv = get_host_w_inventory(client)
        for item in host_w_inv:
            print(f"Host: {item['host_name']:<30} Inventory: {item['inventory_name']}")
        
    elif choice == "2":
        exc_host = excel_parse_hostname('excels/host_check.xlsx')
        host_w_inv = get_host_w_inventory(client)
        matches = match_hosts(exc_host, host_w_inv)

        for item in sorted(matches, key=lambda x: x['inventory_name']):
            print(f"Host: {item['host_name']:<30} Inventory: {item['inventory_name']}")

    elif choice == "3":
        excel_bulk_host = excel_parse_hostname('excels/host_bulk_import.xlsx')
        aap_inv = get_inv(client)

        print("Which inventory to add hosts to?")
        print(f"{'ID':<5}{'Inventory Name'}")
        for item in aap_inv:
            print(f"{item['id']:<5}{item['name']}")

        inv_id = input("\nEnter Inventory ID: ")

        try:
            inv_id = int(inv_id)
        except ValueError:
            raise ValueError("Input must be integer.")

        for item in aap_inv:
            if item['id'] == int(inv_id):
                print("\nWould you like to add the following hosts to: " + item['name'])
                break
            
        else:
            sys.exit("Inventory ID not found. Operation cancelled")

        for host in excel_bulk_host:
            print(f"- {host['Hostname']}")

        confirm = input("\nConfirm? (y/n): ")
        if confirm.lower() == 'y':
            import_bulk = post_bulk_imp(client, inv_id, excel_bulk_host)
            if import_bulk.status_code >= 200 and import_bulk.status_code < 300:
                print("Status code: " + str(import_bulk.status_code))
            else:
                print(f"Failed to import hosts. {import_bulk.json()['__all__']}")
        elif confirm.lower() == 'n':
            sys.exit("Operation cancelled.")
        else:
            sys.exit("Invalid input. Operation cancelled.")

    elif choice == "4":
        print("TBC")

    else:
        print("Invalid choice.")
        main()

if __name__ == "__main__":
    main()
