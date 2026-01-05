from api import get_host_w_inventory
from config.settings import (
    API_BASE_URL,
    API_TOKEN,
    API_TIMEOUT,
)

def main():
    print("""
    1. Print inventory hosts with inventory names
    2
    3
    4
    """)

    choice = input("Enter your choice: ")

    if choice == "1":
        host_w_inv = get_host_w_inventory(API_BASE_URL, API_TOKEN, API_TIMEOUT)
        for item in host_w_inv:
            print(f"Host: {item['host_name']:<30} Inventory: {item['inventory_name']}")
        
if __name__ == "__main__":
    main()
