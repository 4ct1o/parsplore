"""SEC storage module."""

import json

from clients.sec_client import get_tickers

def save_tickers(file: str = "data/sec_tickers_database.json") -> None:
    """
    Save the tickers.

    Args:
        file (str): The path to the file to save the tickers to.
    """

    sec_tickers, last_modified = get_tickers()

    data = {
        "last_modified": last_modified,
        "tickers": sec_tickers,
    }

    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def read_tickers(file: str = "data/sec_tickers_database.json") -> dict:
    """
    Read the tickers.

    Args:
        file (str): The path to the file to read the tickers from.
    Returns:
        dict: The tickers.
    """

    with open(file, "r") as f:
        data = json.load(f)

    return data.get("tickers", {})

def read_tickers_last_modified(file: str = "data/sec_tickers_database.json") -> str | None:
    """
    Get the last modified date of the tickers.

    Args:
        file (str): The path to the file to get the last modified date from.
    Returns:
        str | None: The last modified date of the tickers.
    """
    try:
        with open(file, "r") as f:
                data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    return data.get("last_modified")        
