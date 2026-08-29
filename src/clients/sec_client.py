"""SEC client module."""

import requests

from src.config.settings import load_settings

def get_headers() -> dict:
    """
    Get the headers for the SEC client.

    Returns:
        dict: The headers for the SEC client.
    """
    settings = load_settings()

    headers = {
               'User-Agent': f'parsplore() {settings["email"]}',
              }
    return headers

def get_sec_tickers() -> tuple[dict, str]:
    """
    Get the tickers from the SEC.

    Returns:
        dict: The tickers from the SEC.
    """

    sec_tickers_url = 'https://www.sec.gov/files/company_tickers.json'
    headers = get_headers()

    response = requests.get(sec_tickers_url, headers=headers)
    response.raise_for_status()

    last_modified = response.headers.get("Last-Modified")

    sec_tickers = response.json()

    return sec_tickers, last_modified

def get_sec_ticker_last_modified() -> str | None:
    """
    Get the last modified date of the tickers from the SEC.

    Returns:
        str | None: The last modified date of the tickers.
    """

    sec_tickers_url = 'https://www.sec.gov/files/company_tickers.json'
    headers = get_headers()

    response = requests.head(sec_tickers_url, headers=headers)
    response.raise_for_status()

    last_modified = response.headers.get("Last-Modified")

    return last_modified