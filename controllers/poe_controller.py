import time

from config.settings import POE_PORTS
from services.unifi_service import set_poe


def enable_port(port):
    return set_poe(port, True)


def disable_port(port):
    return set_poe(port, False)


def power_cycle_port(port, delay=10):
    set_poe(port, False)

    time.sleep(delay)

    set_poe(port, True)


def power_cycle_all_ports(delay=10):
    for port in POE_PORTS:
        set_poe(port, False)

    time.sleep(delay)

    for port in POE_PORTS:
        set_poe(port, True)