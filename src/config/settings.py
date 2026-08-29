"""Application settings management module."""

import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent / "settings.json"

def load_settings():
    """
    Load settings from the settings.json file.

    Returns:
        dict: A dictionary containing the settings.
    """

    with SETTINGS_FILE.open('r', encoding='utf-8') as file:
        return json.load(file)

def save_settings(settings: dict) -> None:
    """
    Save settings to the settings.json file.

    Args:
        settings (dict): A dictionary containing the settings to save.
    Returns:
        None
    """
    with SETTINGS_FILE.open('w', encoding='utf-8') as file:
        json.dump(settings, file, indent=4)
