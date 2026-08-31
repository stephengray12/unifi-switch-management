from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def show_title():
    console.print(
        Panel.fit(
            "[bold cyan]UniFi PoE Port Controller[/bold cyan]",
            border_style="blue",
        )
    )


def show_menu():
    console.print()
    console.print("[green]1[/green] - View All Port Status")
    console.print("[green]2[/green] - Enable PoE Port")
    console.print("[green]3[/green] - Disable PoE Port")
    console.print("[green]4[/green] - Power Cycle PoE Port")
    console.print("[green]5[/green] - Power Cycle ALL PoE Ports")
    console.print("[red]Q[/red] - Quit")
    console.print()


def show_port_status(data):
    table = Table(
        title="UniFi Switch Port Status",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Port", justify="center", style="bold")
    table.add_column("Link", justify="center")
    table.add_column("Speed", justify="center")
    table.add_column("PoE", justify="center")

    for port in data["interfaces"]["ports"]:
        idx = port["idx"]
        link_state = port.get("state", "UNKNOWN")
        speed = port.get("speedMbps", 0)

        if link_state == "UP":
            link_display = "[green]UP[/green]"
        else:
            link_display = "[red]DOWN[/red]"

        poe = port.get("poe")

        if poe and poe.get("enabled", False):
            poe_display = "[green]ON[/green]"
        elif poe:
            poe_display = "[red]OFF[/red]"
        else:
            poe_display = "[dim]N/A[/dim]"

        table.add_row(
            str(idx),
            link_display,
            f"{speed} Mbps",
            poe_display,
        )

    console.print()
    console.print(table)


def show_error(message):
    console.print(f"[bold red]{message}[/bold red]")


def show_success(message):
    console.print(f"[bold green]{message}[/bold green]")