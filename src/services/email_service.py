from validators.email_validator import is_valid_email
from data.email_storage import save_email

def process_email(email:str) -> bool:
    """
    Save the provided email to the settings file after validating its format.

    Args:
        email (str): The email address to be saved.
    Returns:
        bool: True if the email was saved successfully, False otherwise.
    """
    if not is_valid_email(email):
        raise ValueError("Invalid email format")

    return save_email(email)