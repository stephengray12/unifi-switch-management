from config.settings import validate_config
from controllers.poe_controller import (
    enable_port,
    disable_port,
    power_cycle_port,
    power_cycle_all_ports,
)
from services.unifi_service import get_switch_data
from utils.terminal import clear_screen, pause
from views.cli_view import (
    console,
    show_title,
    show_menu,
    show_port_status,
    show_error,
)


def main():
    validate_config()

    while True:
        clear_screen()

        show_title()
        show_menu()

        choice = input("Select option: ").strip().lower()

        if choice == "q":
            console.print("\n[bold green]Goodbye![/bold green]")
            break

        elif choice == "1":
            try:
                data = get_switch_data()
                show_port_status(data)
            except Exception as error:
                show_error(str(error))

            pause()

        elif choice == "2":
            port = int(input("Port: "))
            enable_port(port)
            pause()

        elif choice == "3":
            port = int(input("Port: "))
            disable_port(port)
            pause()

        elif choice == "4":
            port = int(input("Port: "))
            delay = int(input("Delay [10]: ") or 10)

            power_cycle_port(port, delay)
            pause()

        elif choice == "5":
            delay = int(input("Delay [10]: ") or 10)

            power_cycle_all_ports(delay)
            pause()

        else:
            show_error("Invalid selection")
            pause()


if __name__ == "__main__":
    main()