import re

def is_valid_email(email: str) -> bool:
    """
    Validate the format of the provided email address.

    Args:
        email (str): The email address to be validated.
    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None