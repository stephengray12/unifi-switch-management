import json
from pathlib import Path


# Find the root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

LABEL_FILE = PROJECT_ROOT / "data" / "port_labels.json"


def load_labels():
    """
    Load all saved port labels from the JSON file.
    """

    if not LABEL_FILE.exists():
        return {}

    try:
        with open(LABEL_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def get_label(port):
    """
    Get the saved label for one port.
    """

    labels = load_labels()

    return labels.get(
        str(port),
        ""
    )


def save_label(port, name):
    """
    Save or update the label for one port.
    """

    labels = load_labels()

    labels[str(port)] = name.strip()

    LABEL_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(LABEL_FILE, "w", encoding="utf-8") as file:
        json.dump(
            labels,
            file,
            indent=4
        )