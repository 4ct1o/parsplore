"""SEC validation module."""

import json
import requests

from clients.sec_client import get_sec_ticker_last_modified
from data.sec_storage import read_tickers_last_modified

def is_ticker_file_up_to_date(file: str = "data/sec_tickers_database.json") -> bool:
    """
    Check if the ticker file is up to date.

    Args:
        file (str): The path to the ticker file.
    Returns:
        bool: True if the ticker file is up to date, False otherwise.
    """

    last_modified = get_sec_ticker_last_modified()

    current_last_modified = read_tickers_last_modified()

    return last_modified == current_last_modified
