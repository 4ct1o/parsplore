"""SEC service module."""

from rapidfuzz import fuzz
import re
from bs4 import BeautifulSoup

from storage.sec_storage import read_tickers
from clients.sec_client import get_form

def search_company(search_term: str, limit: int = 10) -> list[tuple[str, str, str, float]]:
    """
    Search for a company.

    Args:
        search_term (str): The search term.
        limit (int): The maximum number of results to return.
    Returns:
        list[tuple[str, str, str, float]]: A list containing (title, ticker, cik number, match score) for each result.
    """
    tickers = read_tickers()

    query = search_term.strip().lower()

    if not query:
        return []

    results = []

    for _, data in tickers.items():
        title = data["title"]
        ticker = data["ticker"]
        cik = str(data["cik_str"])

        words = re.findall(r"[a-z0-9]+", title.lower())

        if query == ticker.lower():
            score = 100.0

        elif query in words:
            score = 100.0

        else:
            word_scores = [
                fuzz.ratio(query, word)
                for word in words
            ]

            score = max(word_scores, default=0)

        if score >= 60:
            results.append((
                title,
                ticker,
                cik,
                score
            ))

    results.sort(key=lambda result: result[3], reverse=True)

    return results[:limit] 

# Ignore warnings about XML being parsed as HTML
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def create_submission_html(form_info: dict) -> str:
    """
    Create the HTML for a submission.

    Args:
        form_info (dict): The form information.
    Returns:
        str: The HTML for the submission.
    """

    html_text = get_form(form_info)

    soup = BeautifulSoup(html_text, "lxml")

    # Remove XBRL metadata
    for tag in soup.find_all(
        lambda tag: tag.name and (
            tag.name.lower() in {
                "ix:header",
                "ix:hidden",
                "ix:resources",
            }
            # or tag.name.lower().startswith("ix:") # this delete numbers in financial statement part, ix:nonfraction
        )
    ):
        tag.decompose()

    # Remove script and noscript tags
    for tag in soup.find_all(["script", "noscript"]):
        tag.decompose()

    return str(soup)
