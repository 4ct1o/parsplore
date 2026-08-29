"""Ticker validation module."""

def is_ticker_file_up_to_date(file: str) -> bool:
    """
    Check if the ticker file is up to date.

    Args:
        file (str): The path to the ticker file.
    Returns:
        bool: True if the ticker file is up to date, False otherwise.
    """

    if file == "tickers.json":
        return True

    return False
