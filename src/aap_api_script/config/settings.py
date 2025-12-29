import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("AAP_API_TOKEN")
API_BASE_URL = os.getenv("AAP_API_BASE_URL")
API_TIMEOUT = int(os.getenv("AAP_API_TIMEOUT", "5"))

if not API_TOKEN:
    raise RuntimeError("AAP_API_TOKEN is not set")
if not API_BASE_URL:
    raise RuntimeError("AAP_API_BASE_URL is not set")
