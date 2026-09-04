"""SEC service module."""

from rapidfuzz import fuzz, process
import re

from PySide6.QtCore import (
    Qt,
    Signal,
    QThread,
    QObject,
)

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

    query = search_term.strip().lower()

    if not query:
        return []

    results = []

    for _, data in tickers.items():
        title = data["title"]
        ticker = data["ticker"]
        cik = data["cik_str"]

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

class TickerUpdateService(QObject):
    ticker_updated = Signal()

    def start_sec_ticker_task(self):
        """Start the SEC ticker task."""
        from tasks.sec_tasks import SECTickerTask
    
        self.sec_ticker_task = SECTickerTask()
        self.sec_ticker_thread = QThread()
    
        self.sec_ticker_task.moveToThread(self.sec_ticker_thread)
    
        self.sec_ticker_thread.started.connect(self.sec_ticker_task.run)
        self.sec_ticker_task.finished.connect(self.sec_ticker_thread.quit)
        self.sec_ticker_task.finished.connect(self.sec_ticker_task.deleteLater)
        self.sec_ticker_thread.finished.connect(self.sec_ticker_thread.deleteLater)
    
        self.sec_ticker_thread.start()


class CompanySearchService(QObject):
    company_search_completed = Signal(list)

    def start_company_search_task(self, search_term: str):
        """Start the company search task."""
        from tasks.sec_tasks import SECSearchTask

        self.search_task = SECSearchTask(search_term)
        self.search_thread = QThread()

        self.search_task.moveToThread(self.search_thread)

        self.search_thread.started.connect(self.search_task.run)
        self.search_task.finished.connect(self.handle_search_results)
        self.search_task.finished.connect(self.search_thread.quit)
        self.search_task.finished.connect(self.search_task.deleteLater)
        self.search_thread.finished.connect(self.search_thread.deleteLater)

        self.search_thread.start()

    def handle_search_results(self, results: list[tuple[str, str, str, str]]):
        """Handle the search results."""
        self.company_search_completed.emit(results)

class SubmissionSearchService(QObject):
    submissions_fetched = Signal(list) #                                               dict?

    def start_submission_search_task(self, cik_selected: str):
        """Start the submission search task."""
        from tasks.sec_tasks import SECSubmissionsTask

        print(f"Submission search CIK: {cik_selected!r}") #                           DELETE ME

        self.submission_task = SECSubmissionsTask(cik_selected)
        self.submission_thread = QThread()

        self.submission_task.moveToThread(self.submission_thread)

        self.submission_thread.started.connect(self.submission_task.run)
        self.submission_task.finished.connect(self.handle_submission_results)
        self.submission_task.finished.connect(self.submission_thread.quit)
        self.submission_task.finished.connect(self.submission_task.deleteLater)
        self.submission_thread.finished.connect(self.submission_thread.deleteLater)

        self.submission_thread.start()

    def handle_submission_results(self, results: dict):
        """Handle the submission results."""
        self.submissions_fetched.emit(results)
