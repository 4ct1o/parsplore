from config.settings import load_settings, save_settings
from validators.email_validator import is_valid_email

def save_email(email: str) -> bool:
    """
    Save the provided email to the settings file.

    Args:
        email (str): The email address to be saved.
    Returns:
        bool: True if the email was saved successfully, False otherwise.
    """

    settings = load_settings()
    settings["email"] = email
    save_settings(settings)

    return True
    