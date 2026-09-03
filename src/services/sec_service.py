"""SEC service module."""

from rapidfuzz import fuzz, process

from data.sec_storage import read_tickers

def search_company(search_term: str, limit: int = 10) -> list[tuple[str, str, str, str]]:
    """
    Search for a company.

    Args:
        search_term (str): The search term.
        limit (int): The maximum number of results to return.
    Returns:
        list[tuple[str, str, str, str]]: A list containing (title, ticker, cik number, match score) for each result.
    """

    tickers = read_tickers()

    choices = {cik: f"{data['title']} ({data['ticker']})" 
               for cik, data in tickers.items() for cik in [data['cik']]}

    results = process.extract(
        search_term,
        choices,
        scorer=fuzz.WRatio,
        limit=limit,
        score_cutoff=80
    )

    return [(
            tickers[cik]["title"],
            tickers[cik]["ticker"],
            cik,
            score
            ) for score, cik, _ in results] 
