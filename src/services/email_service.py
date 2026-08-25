from validators.email_validator import is_valid_email
from data.email_storage import save_email

def process_email(email:str) -> bool:
    if not is_valid_email(email):
        raise ValueError("Invalid email format")

    return save_email(email)