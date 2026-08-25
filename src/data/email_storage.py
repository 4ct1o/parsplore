from config.settings import load_settings, save_settings
from validators.email_validator import is_valid_email

def save_email(email: str) -> bool:
    if not is_valid_email(email):
        raise ValueError("Invalid email format")

    settings = load_settings()
    settings["email"] = email
    save_settings(settings)

    return True
    