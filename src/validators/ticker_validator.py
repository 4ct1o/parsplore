"""Ticker validation module."""

import json
import requests

from src.clients.sec_client import get_sec_ticker_last_modified

def is_ticker_file_up_to_date(file: str = "data/tickers.json") -> bool:
    """
    Check if the ticker file is up to date.

    Args:
        file (str): The path to the ticker file.
    Returns:
        bool: True if the ticker file is up to date, False otherwise.
    """

    last_modified = get_sec_ticker_last_modified()

    with open(file, "r") as f:
        data = json.load(f)
        current_last_modified = data.get("last_modified")

    if last_modified == current_last_modified:
        return True

    return False
