from api.client import APIClient
from config.settings import (
    API_BASE_URL,
    API_TOKEN,
    API_TIMEOUT,
)

def print_inv_host(inv: int) -> dict:
    client = APIClient(base_url=API_BASE_URL, token=API_TOKEN, timeout=API_TIMEOUT,
        #verify=True, # Set to True to verify SSL certificates
    )
    response = client.get(f"/inventories/{inv}/hosts")
    return response.json()

def main():
    inventory = print_inv_host(6)
    print(inventory)

if __name__ == "__main__":
    main()