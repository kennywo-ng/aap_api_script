import pandas
import json
from config.settings import (
    DOMAIN_NAME
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

    id_num = None
    while id_num is None:
        try:
            id_num = int(input(f"\nEnter {type} ID: "))
        except ValueError:
            print("Invalid input. Please enter a valid ID.")

    id_match = next((i for i in inv if i['id'] == id_num), None)

    return id_match

def prompt_till_valid(list: list, label: str) -> list:
    selected = None
    while selected is None:
        selected = sel_id(list, label)
        if selected is None:
            print(f"\n{label} ID not found. Please try again.")
    return selected