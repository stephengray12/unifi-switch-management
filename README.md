<div align="center">

# ⚡ UniFi Switch Management

### Cross-Platform UniFi Switch Management with Python

A Python application for monitoring and controlling UniFi switch ports through the UniFi API, featuring both a **PySide6 desktop GUI** and a **command-line interface**.

<br>

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge\&logo=qt\&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-11-0078D4?style=for-the-badge\&logo=windows11\&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-Linux-E95420?style=for-the-badge\&logo=ubuntu\&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge\&logo=github\&logoColor=white)

<br>

**GUI • CLI • PoE Control • Port Monitoring • Cross-Platform**

</div>

---

## 📖 About

**UniFi Switch Management** is a cross-platform Python application designed to provide a simple interface for interacting with UniFi network switches.

The application communicates with a UniFi Controller through the **UniFi API**, allowing switch information to be retrieved and supported PoE ports to be controlled remotely.

Two interfaces are available:

| Interface   | Description                                                    |
| ----------- | -------------------------------------------------------------- |
| 🖥️ **GUI** | Desktop interface built with PySide6 and Qt                    |
| ⌨️ **CLI**  | Terminal-based interface for users who prefer the command line |

The same Python codebase can run on **Windows and Linux**.

---

## ✨ Features

### 🖥️ Graphical Interface

* Modern PySide6 / Qt desktop interface
* View switch ports in a table
* View port link status
* View negotiated connection speed
* View connector type
* View PoE activity
* Enable or disable PoE
* Power-cycle individual PoE ports
* Assign custom device names to ports
* Save port labels between application sessions

### ⚡ Switch Management

* Connects directly to a UniFi Controller
* Retrieves switch information using the UniFi API
* Controls supported PoE ports
* Displays active and inactive PoE states
* Distinguishes PoE and non-PoE ports

### 🔐 Configuration

* Credentials are stored outside the source code
* `.env` configuration support
* API keys are not hard-coded
* Virtual environment support

### 🌎 Cross-Platform

Currently tested on:

| Platform          |  Status  |
| ----------------- | :------: |
| 🪟 Windows 11 Pro | ✅ Tested |
| 🐧 Ubuntu Linux   | ✅ Tested |

---

# 🚀 Getting Started

## 📋 Prerequisites

Before installing UniFi Switch Management, you will need:

* 🐍 **Python 3.12+**
* 🌿 **Git**
* 🌐 Network access to your UniFi Controller
* 🔑 UniFi API credentials
* 🖥️ Desktop environment if using the GUI

Check your Python installation:

### Windows

```powershell
python --version
```

### Linux

```bash
python3 --version
```

Check Git:

```bash
git --version
```

---

# 📥 1. Clone the Repository

Open **PowerShell**, **Terminal**, or your preferred shell.

```bash
git clone https://github.com/stephengray12/unifi-switch-management.git
```

Enter the project directory:

```bash
cd unifi-switch-management
```

---

# 🐍 2. Create a Virtual Environment

Using a virtual environment keeps the project's dependencies separate from your system Python installation.

## 🪟 Windows

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

After activation, your prompt should look similar to:

```text
(.venv) PS C:\...\unifi-switch-management>
```

### PowerShell Script Execution

If PowerShell prevents the activation script from running, check your execution policy or use Command Prompt with:

```cmd
.venv\Scripts\activate.bat
```

---

## 🐧 Ubuntu / Linux

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Your terminal should now show:

```text
(.venv)
```

> [!TIP]
> Activate the virtual environment each time you open a new terminal and want to run or develop the application.

---

# 📦 3. Install Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

### Major Dependencies

| Package              | Purpose                          |
| -------------------- | -------------------------------- |
| 🟢 **PySide6**       | Qt desktop graphical interface   |
| 🌐 **requests**      | Communication with the UniFi API |
| 🔐 **python-dotenv** | Loads environment variables      |
| 🎨 **rich**          | Enhanced CLI formatting          |

---

# 🔐 4. Configure the Application

Create a file named:

```text
.env
```

in the root of the project.

Your project should look similar to:

```text
unifi-switch-management/
│
├── 📁 config/
├── 📁 controllers/
├── 📁 data/
├── 📁 models/
├── 📁 resources/
├── 📁 services/
├── 📁 tests/
├── 📁 utils/
├── 📁 views/
│
├── 🔐 .env
├── 🐍 app.py
├── 📦 requirements.txt
├── 📖 README.md
└── 📄 LICENSE
```

Add the configuration values required by `config/settings.py`.

Example:

```env
UNIFI_BASE_URL=https://your-unifi-controller
UNIFI_API_KEY=your_api_key
UNIFI_SITE_ID=your_site_id
UNIFI_DEVICE_ID=your_device_id
UNIFI_INTEGRATION_DEVICE_ID=your_integration_device_id
```

> [!IMPORTANT]
> The exact environment variable names must match the variables expected by `config/settings.py`.

---

## 🛡️ Protect Your Credentials

**Never commit your `.env` file to GitHub.**

Your `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

Before pushing code, check:

```bash
git status
```

Make sure `.env` is **not** listed as a file being committed.

> [!CAUTION]
> If an API key is accidentally committed to a public Git repository, treat that credential as compromised and replace/revoke it.

---

# 🖥️ Launch the GUI

The PySide6 GUI is the recommended way to interact with the application.

## 🪟 Windows

Activate your environment:

```powershell
.venv\Scripts\Activate.ps1
```

Launch:

```powershell
python -m views.gui_view
```

---

## 🐧 Ubuntu / Linux

Activate your environment:

```bash
source .venv/bin/activate
```

Launch:

```bash
python -m views.gui_view
```

If your Linux installation uses `python3` instead:

```bash
python3 -m views.gui_view
```

### 🎉 That's It!

If your configuration is correct, the **UniFi Switch Management GUI** should open.

---

# ⌨️ Launch the CLI

The original command-line interface remains available.

### Windows

```powershell
python app.py
```

### Linux

```bash
python3 app.py
```

The CLI can be useful for:

* SSH sessions
* Remote administration
* Testing
* Users who prefer terminal-based workflows

---

# 🏷️ Custom Device Labels

The GUI allows custom names to be assigned to physical switch ports.

For example:

| Port | Device            |
| :--: | ----------------- |
|   1  | 🥧 Raspberry Pi 5 |
|   2  | 🖥️ Test Server   |
|   3  | 📡 Access Point   |
|   4  | 📷 Camera         |

Labels are stored locally in:

```text
data/port_labels.json
```

This allows the GUI to remember your device names between application sessions.

---

# 🔄 Updating the Application

If you've already cloned the repository, enter the project directory:

```bash
cd unifi-switch-management
```

Activate your virtual environment.

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Linux

```bash
source .venv/bin/activate
```

Pull the newest code:

```bash
git pull
```

Then update dependencies:

```bash
pip install -r requirements.txt
```

> [!TIP]
> Running `pip install -r requirements.txt` after pulling is a good idea whenever dependencies may have changed.

---

# 🏗️ Project Architecture

```text
unifi-switch-management/
│
├── config/
│   └── settings.py
│
├── controllers/
│   └── poe_controller.py
│
├── data/
│   └── port_labels.json
│
├── models/
│
├── resources/
│   ├── icons/
│   └── images/
│
├── services/
│   ├── unifi_service.py
│   └── port_label_service.py
│
├── tests/
│
├── utils/
│
├── views/
│   ├── cli_view.py
│   ├── gui_view.py
│   └── widgets/
│
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

### ⚙️ `config/`

Application configuration and environment-variable handling.

### 🎮 `controllers/`

Application logic for operations such as:

* Enabling PoE
* Disabling PoE
* Power cycling ports

### 🌐 `services/`

Communication and data services.

`unifi_service.py`

Handles communication with the UniFi Controller.

`port_label_service.py`

Handles saving and loading custom device labels.

### 📦 `models/`

Application data models.

### 👁️ `views/`

User interfaces.

`gui_view.py`

PySide6 graphical interface.

`cli_view.py`

Terminal interface.

### 💾 `data/`

Locally stored application data such as custom port labels.

### 🎨 `resources/`

Icons, images, and other graphical resources.

### 🧪 `tests/`

Automated application tests.

---

# 🌎 Cross-Platform Architecture

The application is designed so the operating system running the management application does not have to be the same system running the UniFi Controller.

```text
         🪟 Windows PC
               │
         Python + PySide6
               │
               │
               ├──────────────┐
               │              │
               ▼              │
      UniFi Switch Manager    │
                              │
                         HTTPS / API
                              │
                              ▼
                       UniFi Controller
                              ▲
                         HTTPS / API
                              │
               ▲              │
               │              │
      UniFi Switch Manager    │
               │
         Python + PySide6
               │
         🐧 Linux PC
```

As long as the computer running the application can reach the UniFi Controller over the network, it can communicate with the controller using the API.

This makes the application useful across:

* 🪟 Windows workstations
* 🐧 Linux workstations
* 🖥️ Lab computers
* 🌐 Network-management stations

---

# 🛠️ Troubleshooting

<details>
<summary><strong>❌ ModuleNotFoundError</strong></summary>

<br>

Make sure your virtual environment is activated.

Then run:

```bash
pip install -r requirements.txt
```

You can check whether PySide6 is installed with:

```bash
pip show PySide6
```

</details>

<details>
<summary><strong>🐧 GUI Does Not Open on Linux</strong></summary>

<br>

Verify that PySide6 is installed:

```bash
pip show PySide6
```

Check whether a graphical display is available:

```bash
echo $DISPLAY
```

A headless Linux server or SSH session without graphical forwarding cannot directly display the PySide6 window.

The CLI can still be used without a graphical desktop.

</details>

<details>
<summary><strong>🌐 Cannot Connect to UniFi</strong></summary>

<br>

Verify:

* UniFi Controller is running
* Controller is reachable over the network
* Controller URL is correct
* API key is valid
* Site ID is correct
* Device ID is correct
* Firewall rules allow communication

</details>

<details>
<summary><strong>🌿 Git Pull Says Local Changes Would Be Overwritten</strong></summary>

<br>

First check:

```bash
git status
```

If the local computer should **exactly match GitHub `main`** and you intentionally want to discard tracked local changes:

```bash
git fetch origin
git reset --hard origin/main
```

> [!WARNING]
> `git reset --hard` permanently discards uncommitted changes to tracked files.

Do not run it if you have local work you want to keep.

</details>

---

# 👨‍💻 Development

A typical development session is:

## 🪟 Windows

```powershell
cd unifi-switch-management
.venv\Scripts\Activate.ps1
python -m views.gui_view
```

## 🐧 Ubuntu

```bash
cd unifi-switch-management
source .venv/bin/activate
python -m views.gui_view
```

The project works well with Python IDEs such as PyCharm and Visual Studio Code.

---

# 🗺️ Roadmap

Planned improvements include:

* [ ] 🔄 Background API requests
* [ ] 📊 Additional switch statistics
* [ ] 🔎 Improved device discovery
* [ ] 🌐 Additional UniFi device support
* [ ] ⚡ Expanded PoE controls
* [ ] 🖥️ Additional GUI improvements
* [ ] 🎨 Custom application icon
* [ ] 🪟 Packaged Windows executable
* [ ] 🐧 Packaged Linux application
* [ ] ⚙️ Additional configuration options
* [ ] 🧪 Expanded automated testing

---

# 🔒 Security

This application communicates with network infrastructure and should be treated accordingly.

### Recommended Practices

* 🔑 Never hard-code API keys
* 🔐 Store credentials in `.env`
* 🚫 Never commit `.env`
* 🔄 Rotate exposed API credentials
* 🌐 Restrict access to the UniFi Controller
* 📦 Keep dependencies updated
* 🌿 Review changes before pushing to GitHub

---

# 🤝 Contributing

Contributions, improvements, and bug reports are welcome.

A typical development workflow:

```bash
git switch -c feature/my-feature
```

Make your changes, then:

```bash
git add .
git commit -m "Add my feature"
git push -u origin feature/my-feature
```

Changes can then be reviewed before being merged into `main`.

---

# 📄 License

This project is distributed under the license included in the repository.

See:

```text
LICENSE
```

for details.

---

<div align="center">

### ⚡ UniFi Switch Management

**Built with Python 🐍 • PySide6 🟢 • Qt 💻**

Designed for **Windows 🪟 + Linux 🐧**

</div>
