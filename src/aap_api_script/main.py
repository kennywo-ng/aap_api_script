from api import get_host_w_inventory, get_inv
from config.settings import (
    API_BASE_URL,
    API_TOKEN,
    API_TIMEOUT,
    DOMAIN_NAME,
)

import pandas
import json

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
    4
    """)

    choice = input("Enter your choice: ")
    print("\n")

    if choice == "1":
        host_w_inv = get_host_w_inventory(API_BASE_URL, API_TOKEN, API_TIMEOUT)
        for item in host_w_inv:
            print(f"Host: {item['host_name']:<30} Inventory: {item['inventory_name']}")
        
    elif choice == "2":
        exc_host = excel_parse_hostname('excels/host_check.xlsx')
        host_w_inv = get_host_w_inventory(API_BASE_URL, API_TOKEN, API_TIMEOUT)
        matches = match_hosts(exc_host, host_w_inv)

        for item in sorted(matches, key=lambda x: x['inventory_name']):
            print(f"Host: {item['host_name']:<30} Inventory: {item['inventory_name']}")

    elif choice == "3":
        exc_bulk_host = excel_parse_hostname('excels/host_bulk_import.xlsx')
        for item in exc_bulk_host:
            print(item['Hostname'])
        aap_inv = get_inv(API_BASE_URL, API_TOKEN, API_TIMEOUT)

        for item in aap_inv:
            print(item['name'])


if __name__ == "__main__":
    main()
