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
