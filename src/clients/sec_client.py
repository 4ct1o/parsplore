"""SEC client module."""

import requests

from config.settings import load_settings

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

def get_tickers() -> tuple[dict, str]:
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

def create_submissions_link(company_info: dict) -> str:
    """
    Create a link to the SEC submissions page for a given ticker.

    Args:
        cik (str): The CIK number.
    Returns:
        str: The URL to the SEC submissions page for the given ticker.
    """

    cik = str(company_info.get("cik", "")).strip()

    if not cik or not cik.isdigit():
        raise ValueError(f"Invalid CIK received: {cik!r}")
    
    formatted_cik = f"CIK{cik.zfill(10)}"

    url = f"https://data.sec.gov/submissions/{formatted_cik}.json"

    return url


def get_submissions(cik: str, limit: int = 20) -> dict:
    """
    Get the latest submissions for a given link.

    Args:
        link (str): The link to the SEC submissions page.
    Returns:
        dict: The latest submissions for the given link.
    """

    url = create_submissions_link(cik)

    headers = get_headers()

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()

    recent_filings = []

    for key in range(min(limit, len(data['filings']['recent']))):
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

def get_tickers_last_modified() -> str | None:
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

def create_form_link(form_info: dict) -> str:
    """
    Create a link to the SEC form page for a given CIK and accession number.

    Args:
        form_info (dict): A dictionary containing the form information.

    Returns:
        str: The URL to the SEC form page for the given CIK and accession number.
    """
    cik = str(form_info.get("cik", "")).strip()
    accession_number = str(form_info.get("accession_number", "")).replace('-', '').strip()
    ticker = str(form_info.get("ticker", "")).strip().lower()
    report_date = str(form_info.get("report_date", "")).replace('-', '').strip()

    if "-" in ticker:
        ticker = ticker.split("-")[0] + "a"

    if not cik or not cik.isdigit():
        raise ValueError(f"Invalid CIK received: {cik!r}")

    if not accession_number:
        raise ValueError(f"Invalid accession number received: {accession_number!r}")

    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{ticker}-{report_date}.htm"

def get_form(form_info: dict) -> str:
    """
    Get the form from the SEC.

    Args:
        form_info (dict): A dictionary containing the form information.

    Returns:
        str: The form from the SEC.
    """
    sec_form_url = create_form_link(form_info)

    headers = get_headers()

    response = requests.get(sec_form_url, headers=headers)
    response.raise_for_status()

    return response.text
