import requests
import urllib3

from config.settings import (
    BASE_URL,
    API_KEY,
    SITE_ID,
    DEVICE_ID,
    INTEGRATION_DEVICE_ID,
    HEADERS,
)

urllib3.disable_warnings()


def get_switch_data():
    response = requests.get(
        f"{BASE_URL}/proxy/network/integration/v1/sites/"
        f"{SITE_ID}/devices/{INTEGRATION_DEVICE_ID}",
        headers={
            "X-API-KEY": API_KEY,
            "Accept": "application/json",
        },
        verify=False,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def get_port_info(port_number):
    data = get_switch_data()

    for port in data["interfaces"]["ports"]:
        if port["idx"] == port_number:
            return port

    return None


def set_poe(port, enabled):
    payload = {
        "port_overrides": [
            {
                "port_idx": port,
                "name": f"Port {port}",
                "setting_preference": "auto",
                "poe_mode": "auto" if enabled else "off",
                "port_poe": enabled,
            }
        ]
    }

    response = requests.put(
        f"{BASE_URL}/proxy/network/api/s/default/rest/device/{DEVICE_ID}",
        headers=HEADERS,
        json=payload,
        verify=False,
        timeout=10,
    )

    response.raise_for_status()

    return response