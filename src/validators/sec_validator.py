"""SEC validation module."""

from clients.sec_client import get_tickers_last_modified
from storage.sec_storage import read_tickers_last_modified

def is_tickers_up_to_date(file: str = "data/sec_tickers_database.json") -> bool:
    """
    Check if the ticker file is up to date.

    Args:
        file (str): The path to the ticker file.
    Returns:
        bool: True if the ticker file is up to date, False otherwise.
    """

    last_modified = get_tickers_last_modified()

    current_last_modified = read_tickers_last_modified()

    return last_modified == current_last_modified
