"""Ticker storage module."""

import json

from src.clients.sec_client import get_sec_tickers, get_sec_ticker_last_modified

def save_tickers(file: str = "data/tickers.json") -> None:
    """
    Save the tickers.

    Args:
        file (str): The path to the file to save the tickers to.
    """

    sec_tickers, last_modified = get_sec_tickers()

    data = {
        "last_modified": last_modified,
        "tickers": sec_tickers,
    }

    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def read_tickers_last_modified(file: str = "data/tickers.json") -> str | None:
    """
    Get the last modified date of the tickers.

    Args:
        file (str): The path to the file to get the last modified date from.
    Returns:
        str | None: The last modified date of the tickers.
    """

    with open(file, "r") as f:
        data = json.load(f)

    return data.get("last_modified")        

def read_tickers(file: str = "data/tickers.json") -> dict:
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
