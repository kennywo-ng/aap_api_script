import os
import getpass
from dotenv import load_dotenv

load_dotenv(f'../../.env.prod')

API_BASE_URL = os.getenv("AAP_API_BASE_URL")
API_TIMEOUT = int(os.getenv("AAP_API_TIMEOUT", "5"))
DOMAIN_NAME = os.getenv("AAP_DOMAIN_NAME")
ENV = os.getenv("AAP_ENV")

if ENV == "stage":
    API_TOKEN = os.getenv("AAP_API_TOKEN")
    AUTH_USERNAME = None
    AUTH_PASSWORD = None
    if not API_TOKEN:
        raise RuntimeError("AAP_API_TOKEN is not set")
    if not API_BASE_URL:
        raise RuntimeError("AAP_API_BASE_URL is not set")

if ENV == "prod":
    AUTH_USERNAME = os.getenv("AAP_AUTH_USERNAME")
    AUTH_PASSWORD = getpass.getpass("Enter password: ")
    API_TOKEN = None
    
    if not AUTH_USERNAME:
        raise RuntimeError("AAP_AUTH_USERNAME is not set for production")
