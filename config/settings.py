import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("UNIFI_BASE_URL")
API_KEY = os.getenv("UNIFI_API_KEY")
SITE_ID = os.getenv("UNIFI_SITE_ID")
DEVICE_ID = os.getenv("UNIFI_DEVICE_ID")
INTEGRATION_DEVICE_ID = os.getenv("UNIFI_INTEGRATION_DEVICE_ID")

POE_PORTS = [1, 2, 3, 4]

HEADERS = {
    "X-API-KEY": API_KEY,
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def validate_config():
    required = {
        "UNIFI_BASE_URL": BASE_URL,
        "UNIFI_API_KEY": API_KEY,
        "UNIFI_SITE_ID": SITE_ID,
        "UNIFI_DEVICE_ID": DEVICE_ID,
        "UNIFI_INTEGRATION_DEVICE_ID": INTEGRATION_DEVICE_ID,
    }

    missing = [
        name
        for name, value in required.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )