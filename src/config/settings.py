import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent / "settings.json"

def load_settings():
    with SETTINGS_FILE.open('r', encoding='utf-8') as file:
        return json.load(file)

def save_settings(settings: dict) -> None:
    with SETTINGS_FILE.open('w', encoding='utf-8') as file:
        json.dump(settings, file, indent=4)