"""SEC client module."""

import requests

from src.config.settings import load_settings
from src.services.sec_service import create_company_submission_link

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

def get_latest_submissions(cik: str, limit: int = 10) -> dict:
    """
    Get the latest submissions for a given link.

    Args:
        link (str): The link to the SEC submissions page.
    Returns:
        dict: The latest submissions for the given link.
    """

    url = create_company_submission_link(cik)

    headers = get_headers()

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()

    recent_filings = []

    for key in range(min(limit, len(data['recent']))):
        filing = {
            'accessionNumber':       data['filings']['recent']['accessionNumber'][key],
            'filingDate':            data['filings']['recent']['filingDate'][key],
            'reportDate':            data['filings']['recent']['reportDate'][key],
            'acceptanceDateTime':    data['filings']['recent']['acceptanceDateTime'][key],
            'form':                  data['filings']['recent']['form'][key],
            'fileNumber':            data['filings']['recent']['fileNumber'][key],
            'primaryDocument':       data['filings']['recent']['primaryDocument'][key],
            'primaryDocDescription': data['filings']['recent']['primaryDocDescription'][key],
            'items':                 data['filings']['recent']['items'][key],
            'isXBRL':                data['filings']['recent']['isXBRL'][key],
            'isInlineXBRL':          data['filings']['recent']['isInlineXBRL'][key],
        }
        recent_filings.append(filing)

    return recent_filings