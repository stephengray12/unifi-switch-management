import sys
from datetime import datetime

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from config.settings import POE_PORTS

from controllers.poe_controller import (
    enable_port,
    disable_port,
    power_cycle_port,
    power_cycle_all_ports,
)

from services.unifi_service import get_switch_data

from services.port_label_service import (
    load_labels,
    save_label,
)


# =========================================================
# POWER CYCLE WORKER
# =========================================================

class PowerCycleWorker(QThread):
    finished_successfully = Signal()
    failed = Signal(str)

    def __init__(self, port=None, delay=10, cycle_all=False):
        super().__init__()

        self.port = port
        self.delay = delay
        self.cycle_all = cycle_all

    def run(self):
        try:
            if self.cycle_all:
                power_cycle_all_ports(self.delay)
            else:
                power_cycle_port(self.port, self.delay)

            self.finished_successfully.emit()

        except Exception as error:
            self.failed.emit(str(error))


# =========================================================
# MAIN WINDOW
# =========================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None

        self.setWindowTitle("UniFi Switch Manager")
        self.resize(1200, 650)

        # -------------------------------------------------
        # Main Widget
        # -------------------------------------------------

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        main_layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        main_layout.setSpacing(20)

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = QLabel("UniFi Switch Manager")
        title.setObjectName("titleLabel")

        main_layout.addWidget(title)

        # -------------------------------------------------
        # Connection Status
        # -------------------------------------------------

        connection_layout = QHBoxLayout()

        connection_text = QLabel(
            "Connection Status:"
        )

        self.connection_indicator = QFrame()

        self.connection_indicator.setObjectName(
            "connectionIndicator"
        )

        self.connection_indicator.setFixedSize(
            14,
            14,
        )

        self.connection_label = QLabel(
            "Disconnected"
        )

        self.connection_label.setObjectName(
            "connectionLabel"
        )

        connection_layout.addWidget(
            connection_text
        )

        connection_layout.addWidget(
            self.connection_indicator
        )

        connection_layout.addWidget(
            self.connection_label
        )

        connection_layout.addStretch()

        self.last_refresh_label = QLabel(
            "Last Refresh: --"
        )

        connection_layout.addWidget(
            self.last_refresh_label
        )

        main_layout.addLayout(
            connection_layout
        )

        # -------------------------------------------------
        # Port Table
        # -------------------------------------------------

        self.port_table = QTableWidget()

        headers = [
            "Port",
            "Device",
            "Link",
            "Speed",
            "PoE Status",
            "PoE Control",
            "Connector",
            "Actions",
        ]

        self.port_table.setColumnCount(
            len(headers)
        )

        self.port_table.setHorizontalHeaderLabels(
            headers
        )

        self.port_table.setRowCount(0)

        self.port_table.setAlternatingRowColors(
            True
        )

        # Allow device names to be edited by double-clicking
        self.port_table.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked
        )

        # Save a device name when the table item changes
        self.port_table.itemChanged.connect(
            self.save_device_label
        )

        self.port_table.verticalHeader().setVisible(
            False
        )

        header = self.port_table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        main_layout.addWidget(
            self.port_table
        )

        # -------------------------------------------------
        # Bottom Buttons
        # -------------------------------------------------

        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton(
            "Refresh Ports"
        )

        self.refresh_button.clicked.connect(
            self.refresh_ports
        )

        self.cycle_all_button = QPushButton(
            "Power Cycle All"
        )

        self.cycle_all_button.clicked.connect(
            self.cycle_all_ports
        )

        button_layout.addWidget(
            self.refresh_button
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.cycle_all_button
        )

        main_layout.addLayout(
            button_layout
        )

        # -------------------------------------------------
        # Bottom Status
        # -------------------------------------------------

        self.status_label = QLabel(
            "Ready"
        )

        self.status_label.setObjectName(
            "statusLabel"
        )

        main_layout.addWidget(
            self.status_label
        )

        # -------------------------------------------------
        # Styles
        # -------------------------------------------------

        self.apply_styles()

        # -------------------------------------------------
        # Initial Refresh
        # -------------------------------------------------

        self.refresh_ports()

    # =====================================================
    # REFRESH PORTS
    # =====================================================

    def refresh_ports(self):

        self.status_label.setText(
            "Refreshing switch data..."
        )

        QApplication.processEvents()

        try:
            data = get_switch_data()

            self.set_connected(True)

            ports = data.get(
                "interfaces",
                {}
            ).get(
                "ports",
                []
            )

            self.populate_port_table(
                ports
            )

            current_time = datetime.now().strftime(
                "%I:%M:%S %p"
            )

            self.last_refresh_label.setText(
                f"Last Refresh: {current_time}"
            )

            self.status_label.setText(
                f"Loaded {len(ports)} ports"
            )

        except Exception as error:

            self.set_connected(False)

            self.status_label.setText(
                f"Connection error: {error}"
            )

            self.port_table.setRowCount(0)

    # =====================================================
    # POPULATE PORT TABLE
    # =====================================================

    def populate_port_table(self, ports):

        # Stop itemChanged from firing while we load
        # existing labels into the table.
        self.port_table.blockSignals(True)

        self.port_table.setRowCount(
            len(ports)
        )

        # Load all saved labels once
        labels = load_labels()

        for row, port in enumerate(ports):

            # ---------------------------------------------
            # Port Number
            # ---------------------------------------------

            port_number = port.get(
                "idx",
                "--"
            )

            # ---------------------------------------------
            # Custom Device Label
            # ---------------------------------------------

            device_name = labels.get(
                str(port_number),
                ""
            )

            # ---------------------------------------------
            # Link Status
            # ---------------------------------------------

            link_state = port.get(
                "state",
                "DOWN"
            )

            link_status = link_state.title()

            # ---------------------------------------------
            # Speed
            # ---------------------------------------------

            speed = port.get(
                "speedMbps"
            )

            if speed:

                if speed >= 1000:

                    speed_text = (
                        f"{speed / 1000:g} Gbps"
                    )

                else:

                    speed_text = (
                        f"{speed} Mbps"
                    )

            else:

                speed_text = "--"

            # ---------------------------------------------
            # Connector
            # ---------------------------------------------

            connector = port.get(
                "connector",
                "--"
            )

            # ---------------------------------------------
            # Is this a PoE capable port?
            # ---------------------------------------------

            is_poe_port = (
                port_number in POE_PORTS
            )

            # ---------------------------------------------
            # PoE Information
            # ---------------------------------------------

            poe = port.get(
                "poe",
                {}
            )

            poe_enabled = poe.get(
                "enabled",
                False
            )

            poe_state = poe.get(
                "state",
                "DOWN"
            )

            poe_active = (
                poe_state == "UP"
            )

            # =============================================
            # PORT COLUMN
            # =============================================

            port_item = QTableWidgetItem(
                str(port_number)
            )

            # Make Port read-only
            port_item.setFlags(
                port_item.flags()
                & ~Qt.ItemFlag.ItemIsEditable
            )

            self.port_table.setItem(
                row,
                0,
                port_item
            )

            # =============================================
            # DEVICE COLUMN
            # =============================================

            device_item = QTableWidgetItem(
                device_name
            )

            # Store the port number inside the item
            device_item.setData(
                Qt.ItemDataRole.UserRole,
                port_number
            )

            self.port_table.setItem(
                row,
                1,
                device_item
            )

            # =============================================
            # LINK COLUMN
            # =============================================

            link_item = QTableWidgetItem(
                link_status
            )

            link_item.setFlags(
                link_item.flags()
                & ~Qt.ItemFlag.ItemIsEditable
            )

            self.port_table.setItem(
                row,
                2,
                link_item
            )

            # =============================================
            # SPEED COLUMN
            # =============================================

            speed_item = QTableWidgetItem(
                speed_text
            )

            speed_item.setFlags(
                speed_item.flags()
                & ~Qt.ItemFlag.ItemIsEditable
            )

            self.port_table.setItem(
                row,
                3,
                speed_item
            )

            # =============================================
            # POE STATUS
            # =============================================

            if not is_poe_port:

                poe_status = QLabel(
                    "Non-PoE"
                )

                poe_status.setStyleSheet("""
                    color: #9ca3af;
                    font-weight: bold;
                """)

            elif poe_active:

                poe_status = QLabel(
                    "● Active"
                )

                poe_status.setStyleSheet("""
                    color: #22c55e;
                    font-weight: bold;
                """)

            else:

                poe_status = QLabel(
                    "● Inactive"
                )

                poe_status.setStyleSheet("""
                    color: #ef4444;
                    font-weight: bold;
                """)

            poe_status.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.port_table.setCellWidget(
                row,
                4,
                poe_status
            )

            # =============================================
            # POE CONTROL
            # =============================================

            if not is_poe_port:

                control_label = QLabel(
                    "--"
                )

                control_label.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.port_table.setCellWidget(
                    row,
                    5,
                    control_label
                )

            else:

                if poe_enabled:

                    poe_button = QPushButton(
                        "Disable"
                    )

                    poe_button.setObjectName(
                        "disablePoeButton"
                    )

                else:

                    poe_button = QPushButton(
                        "Enable"
                    )

                    poe_button.setObjectName(
                        "enablePoeButton"
                    )

                poe_button.clicked.connect(
                    lambda checked=False,
                    p=port_number,
                    enabled=poe_enabled:
                    self.toggle_poe(
                        p,
                        enabled
                    )
                )

                self.port_table.setCellWidget(
                    row,
                    5,
                    poe_button
                )

            # =============================================
            # CONNECTOR
            # =============================================

            connector_item = QTableWidgetItem(
                connector
            )

            connector_item.setFlags(
                connector_item.flags()
                & ~Qt.ItemFlag.ItemIsEditable
            )

            self.port_table.setItem(
                row,
                6,
                connector_item
            )

            # =============================================
            # ACTIONS
            # =============================================

            actions_widget = QWidget()

            actions_layout = QHBoxLayout(
                actions_widget
            )

            actions_layout.setContentsMargins(
                3,
                3,
                3,
                3,
            )

            if is_poe_port:

                cycle_button = QPushButton(
                    "Cycle"
                )

                cycle_button.clicked.connect(
                    lambda checked=False,
                    p=port_number:
                    self.cycle_port(p)
                )

                actions_layout.addWidget(
                    cycle_button
                )

            else:

                no_action_label = QLabel(
                    "--"
                )

                no_action_label.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                actions_layout.addWidget(
                    no_action_label
                )

            self.port_table.setCellWidget(
                row,
                7,
                actions_widget
            )

        # Turn signals back on after table is loaded
        self.port_table.blockSignals(False)

    # =====================================================
    # SAVE DEVICE LABEL
    # =====================================================

    def save_device_label(self, item):

        # We only want to save edits made to
        # column 1, which is the Device column.
        if item.column() != 1:
            return

        # Retrieve the port number that we stored
        # in UserRole when the table was populated.
        port_number = item.data(
            Qt.ItemDataRole.UserRole
        )

        if port_number is None:
            return

        # Remove spaces from beginning/end
        device_name = item.text().strip()

        try:

            save_label(
                port_number,
                device_name
            )

            self.status_label.setText(
                f'Saved Port {port_number} as "{device_name}"'
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Save Error",
                f"Could not save device label:\n{error}"
            )

            self.status_label.setText(
                "Could not save device label"
            )

    # =====================================================
    # ENABLE / DISABLE POE
    # =====================================================

    def toggle_poe(
        self,
        port,
        currently_enabled,
    ):

        try:

            if currently_enabled:

                self.status_label.setText(
                    f"Disabling PoE on port {port}..."
                )

                QApplication.processEvents()

                disable_port(
                    port
                )

            else:

                self.status_label.setText(
                    f"Enabling PoE on port {port}..."
                )

                QApplication.processEvents()

                enable_port(
                    port
                )

            self.refresh_ports()

        except Exception as error:

            QMessageBox.critical(
                self,
                "PoE Error",
                str(error),
            )

            self.status_label.setText(
                "PoE command failed"
            )

    # =====================================================
    # POWER CYCLE ONE PORT
    # =====================================================

    def cycle_port(
        self,
        port,
    ):

        self.status_label.setText(
            f"Power cycling port {port}..."
        )

        self.set_controls_enabled(
            False
        )

        self.worker = PowerCycleWorker(
            port=port,
            delay=10,
        )

        self.worker.finished_successfully.connect(
            self.worker_finished
        )

        self.worker.failed.connect(
            self.worker_failed
        )

        self.worker.start()

    # =====================================================
    # POWER CYCLE ALL POE PORTS
    # =====================================================

    def cycle_all_ports(self):

        answer = QMessageBox.question(
            self,
            "Power Cycle All Ports",
            "Are you sure you want to power cycle all configured PoE ports?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if (
            answer
            != QMessageBox.StandardButton.Yes
        ):
            return

        self.status_label.setText(
            "Power cycling all PoE ports..."
        )

        self.set_controls_enabled(
            False
        )

        self.worker = PowerCycleWorker(
            delay=10,
            cycle_all=True,
        )

        self.worker.finished_successfully.connect(
            self.worker_finished
        )

        self.worker.failed.connect(
            self.worker_failed
        )

        self.worker.start()

    # =====================================================
    # WORKER FINISHED
    # =====================================================

    def worker_finished(self):

        self.status_label.setText(
            "Power cycle complete"
        )

        self.set_controls_enabled(
            True
        )

        self.refresh_ports()

    def worker_failed(
        self,
        error,
    ):

        self.set_controls_enabled(
            True
        )

        self.status_label.setText(
            "Power cycle failed"
        )

        QMessageBox.critical(
            self,
            "Power Cycle Error",
            error,
        )

    # =====================================================
    # ENABLE / DISABLE CONTROLS
    # =====================================================

    def set_controls_enabled(
        self,
        enabled,
    ):

        self.refresh_button.setEnabled(
            enabled
        )

        self.cycle_all_button.setEnabled(
            enabled
        )

        self.port_table.setEnabled(
            enabled
        )

    # =====================================================
    # CONNECTION INDICATOR
    # =====================================================

    def set_connected(
        self,
        connected,
    ):

        if connected:

            self.connection_indicator.setStyleSheet("""
                background-color: #22c55e;
                border-radius: 7px;
            """)

            self.connection_label.setText(
                "Connected"
            )

            self.connection_label.setStyleSheet("""
                color: #22c55e;
                font-weight: bold;
            """)

        else:

            self.connection_indicator.setStyleSheet("""
                background-color: #dc2626;
                border-radius: 7px;
            """)

            self.connection_label.setText(
                "Disconnected"
            )

            self.connection_label.setStyleSheet("""
                color: #dc2626;
                font-weight: bold;
            """)

    # =====================================================
    # STYLES
    # =====================================================

    def apply_styles(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f1115;
            }

            QWidget {
                color: #ffffff;
                font-size: 14px;
            }

            QLabel#titleLabel {
                font-size: 28px;
                font-weight: bold;
            }

            QFrame#connectionIndicator {
                background-color: #dc2626;
                border-radius: 7px;
            }

            QLabel#connectionLabel {
                color: #dc2626;
                font-weight: bold;
            }

            QTableWidget {
                background-color: #12151b;
                alternate-background-color: #181c23;
                color: white;

                gridline-color: #343a46;

                border: 1px solid #343a46;
                border-radius: 6px;

                selection-background-color: #2563eb;
            }

            QTableWidget::item {
                padding: 8px;
            }

            QHeaderView::section {
                background-color: #1d222b;
                color: white;

                padding: 10px;

                border: none;
                border-right: 1px solid #343a46;
                border-bottom: 1px solid #343a46;

                font-weight: bold;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;

                border: none;
                border-radius: 5px;

                padding: 8px 14px;

                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton:pressed {
                background-color: #1e40af;
            }

            QPushButton:disabled {
                background-color: #374151;
                color: #9ca3af;
            }

            QPushButton#disablePoeButton {
                background-color: #dc2626;
            }

            QPushButton#disablePoeButton:hover {
                background-color: #b91c1c;
            }

            QPushButton#enablePoeButton {
                background-color: #16a34a;
            }

            QPushButton#enablePoeButton:hover {
                background-color: #15803d;
            }

            QLabel#statusLabel {
                color: #9ca3af;
            }
        """)


# =========================================================
# RUN GUI
# =========================================================

def run_gui():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    run_gui()