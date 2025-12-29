from api.client import APIClient
from config.settings import (
    API_BASE_URL,
    API_TOKEN,
    API_TIMEOUT,
)

def establish_session():
    client = APIClient(
        base_url=API_BASE_URL,
        token=API_TOKEN,
        timeout=API_TIMEOUT,
        #verify=True, # Set to True to verify SSL certificates
    )

    response = client.get("/inventories/6/hosts")
    print(response.json())

def main():
    establish_session()

if __name__ == "__main__":
    main()