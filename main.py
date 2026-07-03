import os
import time
import requests
import urllib3

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

urllib3.disable_warnings()

load_dotenv()

# ======================================================
# CONFIGURATION
# ======================================================

BASE_URL = os.getenv("UNIFI_BASE_URL")
API_KEY = os.getenv("UNIFI_API_KEY")
SITE_ID = os.getenv("UNIFI_SITE_ID")
DEVICE_ID = os.getenv("UNIFI_DEVICE_ID")
INTEGRATION_DEVICE_ID = os.getenv("UNIFI_INTEGRATION_DEVICE_ID")

POE_PORTS = [1, 2, 3, 4]

console = Console()

required = {
    "UNIFI_BASE_URL": BASE_URL,
    "UNIFI_API_KEY": API_KEY,
    "UNIFI_SITE_ID": SITE_ID,
    "UNIFI_DEVICE_ID": DEVICE_ID,
    "UNIFI_INTEGRATION_DEVICE_ID": INTEGRATION_DEVICE_ID,
}

missing = [name for name, value in required.items() if not value]

if missing:
    console.print("[bold red]Missing required environment variables:[/bold red]")
    for var in missing:
        console.print(f" • {var}")
    raise SystemExit(1)

HEADERS = {
    "X-API-KEY": API_KEY,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# ======================================================
# UTILITIES
# ======================================================

def clear_screen():
    os.system("clear")


def pause():
    input("\nPress Enter to continue...")


# ======================================================
# API FUNCTIONS
# ======================================================

def get_switch_data():
    try:
        response = requests.get(
            f"{BASE_URL}/proxy/network/integration/v1/sites/{SITE_ID}/devices/{INTEGRATION_DEVICE_ID}",
            headers={
                "X-API-KEY": API_KEY,
                "Accept": "application/json"
            },
            verify=False,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        console.print("[bold red]Failed to retrieve switch data[/bold red]")
        console.print(str(e))
        return None


def get_port_info(port_number):
    data = get_switch_data()

    if not data:
        return None

    for port in data["interfaces"]["ports"]:
        if port["idx"] == port_number:
            return port

    return None


# ======================================================
# STATUS DISPLAY
# ======================================================

def show_port_status():
    data = get_switch_data()

    if not data:
        return

    table = Table(
        title="UniFi Switch Port Status",
        show_header=True,
        header_style="bold cyan"
    )

    table.add_column("Port", justify="center", style="bold")
    table.add_column("Link", justify="center")
    table.add_column("Speed", justify="center")
    table.add_column("PoE", justify="center")

    for port in data["interfaces"]["ports"]:
        idx = port["idx"]

        link_state = port.get("state", "UNKNOWN")
        speed = str(port.get("speedMbps", 0))

        if link_state == "UP":
            link_display = "[green]UP[/green]"
        else:
            link_display = "[red]DOWN[/red]"

        poe = port.get("poe")

        if poe:
            if poe.get("enabled", False):
                poe_display = "[green]ON[/green]"
            else:
                poe_display = "[red]OFF[/red]"
        else:
            poe_display = "[dim]N/A[/dim]"

        table.add_row(
            str(idx),
            link_display,
            f"{speed} Mbps",
            poe_display
        )

    console.print()
    console.print(table)


# ======================================================
# POE CONTROL
# ======================================================

def set_poe(port, enabled):
    payload = {
        "port_overrides": [
            {
                "port_idx": port,
                "name": f"Port {port}",
                "setting_preference": "auto",
                "poe_mode": "auto" if enabled else "off",
                "port_poe": enabled
            }
        ]
    }

    response = requests.put(
        f"{BASE_URL}/proxy/network/api/s/default/rest/device/{DEVICE_ID}",
        headers=HEADERS,
        json=payload,
        verify=False,
        timeout=10
    )

    console.print()

    if response.status_code == 200:
        state = "ON" if enabled else "OFF"

        console.print(
            f"[bold green]Successfully turned PoE {state} on Port {port}[/bold green]"
        )
    else:
        console.print(
            f"[bold red]HTTP Status: {response.status_code}[/bold red]"
        )
        console.print(response.text)

    return response.status_code == 200


def power_cycle_port(port, delay):
    console.print(
        f"\n[yellow]Turning OFF PoE on Port {port}[/yellow]"
    )

    set_poe(port, False)

    console.print(
        f"[cyan]Waiting {delay} seconds...[/cyan]"
    )

    time.sleep(delay)

    console.print(
        f"[yellow]Turning ON PoE on Port {port}[/yellow]"
    )

    set_poe(port, True)

    console.print(
        f"\n[bold green]Port {port} power cycle complete[/bold green]"
    )


def power_cycle_all_ports(delay):
    console.print(
        "\n[bold yellow]Turning OFF all PoE ports...[/bold yellow]"
    )

    for port in POE_PORTS:
        set_poe(port, False)

    console.print(
        f"\n[cyan]Waiting {delay} seconds...[/cyan]"
    )

    time.sleep(delay)

    console.print(
        "\n[bold yellow]Turning ON all PoE ports...[/bold yellow]"
    )

    for port in POE_PORTS:
        set_poe(port, True)

    console.print(
        "\n[bold green]All PoE ports restored[/bold green]"
    )


# ======================================================
# MENU HELPERS
# ======================================================

def select_poe_port():
    console.print(
        "\n[bold cyan]Available PoE Ports:[/bold cyan] 1, 2, 3, 4"
    )

    value = input("\nSelect port: ").strip()

    if not value.isdigit():
        return None

    port = int(value)

    if port not in POE_PORTS:
        return None

    return port


# ======================================================
# MAIN LOOP
# ======================================================

while True:
    clear_screen()

    console.print(
        Panel.fit(
            "[bold cyan]UniFi PoE Port Controller[/bold cyan]",
            border_style="blue"
        )
    )

    console.print()
    console.print("[green]1[/green] - View All Port Status")
    console.print("[green]2[/green] - Enable PoE Port")
    console.print("[green]3[/green] - Disable PoE Port")
    console.print("[green]4[/green] - Power Cycle PoE Port")
    console.print("[green]5[/green] - Power Cycle ALL PoE Ports")
    console.print("[red]Q[/red] - Quit")
    console.print()

    choice = input("Select option: ").strip().lower()

    # Quit
    if choice == "q":
        console.print("\n[bold green]Goodbye![/bold green]")
        break

    # View Status
    elif choice == "1":
        show_port_status()
        pause()

    # Single Port Actions
    elif choice in ["2", "3", "4"]:

        port = select_poe_port()

        if port is None:
            console.print(
                "\n[bold red]Invalid port selection[/bold red]"
            )
            pause()
            continue

        port_info = get_port_info(port)

        if port_info and "poe" in port_info:
            current_state = port_info["poe"].get("enabled", False)

            if current_state:
                state_text = "[green]ON[/green]"
            else:
                state_text = "[red]OFF[/red]"

            console.print(
                f"\nCurrent PoE State: {state_text}"
            )

        confirm = input(
            f"\nModify Port {port}? (y/n): "
        ).lower()

        if confirm != "y":
            continue

        if choice == "2":
            set_poe(port, True)

        elif choice == "3":
            set_poe(port, False)

        elif choice == "4":

            delay_input = input(
                "\nDelay in seconds [10]: "
            ).strip()

            delay = int(delay_input) if delay_input else 10

            power_cycle_port(port, delay)

        console.print("\n[bold cyan]Updated Status:[/bold cyan]")
        show_port_status()

        pause()

    # All Ports Power Cycle
    elif choice == "5":

        confirm = input(
            "\nPower cycle ALL PoE ports? (y/n): "
        ).lower()

        if confirm != "y":
            continue

        delay_input = input(
            "\nDelay in seconds [10]: "
        ).strip()

        delay = int(delay_input) if delay_input else 10

        power_cycle_all_ports(delay)

        console.print("\n[bold cyan]Updated Status:[/bold cyan]")
        show_port_status()

        pause()

    else:
        console.print(
            "\n[bold red]Invalid selection[/bold red]"
        )
        pause()