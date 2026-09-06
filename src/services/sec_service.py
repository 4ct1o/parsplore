"""SEC service module."""

from rapidfuzz import fuzz
import re

from storage.sec_storage import read_tickers

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
