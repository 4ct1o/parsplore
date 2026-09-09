"""SEC dispatchers module."""

from PySide6.QtCore import QObject, Signal, QThread

class TickerUpdateDispatcher(QObject):
    """Ticker update dispatcher."""

    ticker_updated = Signal()

    def start(self):
        """Start the SEC ticker task."""
        from workers.sec_workers import TickerUpdateWorker
    
        self.sec_ticker_task = TickerUpdateWorker()
        self.sec_ticker_thread = QThread()
    
        self.sec_ticker_task.moveToThread(self.sec_ticker_thread)
    
        self.sec_ticker_thread.started.connect(self.sec_ticker_task.run)
        self.sec_ticker_task.finished.connect(self.sec_ticker_thread.quit)
        self.sec_ticker_task.finished.connect(self.sec_ticker_task.deleteLater)
        self.sec_ticker_thread.finished.connect(self.sec_ticker_thread.deleteLater)
    
        self.sec_ticker_thread.start()

class CompanySearchDispatcher(QObject):
    """Company search dispatcher."""

    search_results = Signal(list)

    def start(self, search_term: str):
        """Start the company search task."""
        from workers.sec_workers import CompanySearchWorker

        self.search_task = CompanySearchWorker(search_term)
        self.search_thread = QThread()

        self.search_task.moveToThread(self.search_thread)

        self.search_thread.started.connect(self.search_task.run)
        self.search_task.finished.connect(self.handle_results)
        self.search_task.finished.connect(self.search_thread.quit)
        self.search_task.finished.connect(self.search_task.deleteLater)
        self.search_thread.finished.connect(self.search_thread.deleteLater)

        self.search_thread.start()

    def handle_results(self, results: list[tuple[str, str, str, float]]):
        """Handle the search results."""
        self.search_results.emit(results)

class SubmissionSearchDispatcher(QObject):
    """Submission search dispatcher."""

    search_results = Signal(list)

    def start(self, cik_selected: str):
        """Start the submission search task."""
        from workers.sec_workers import SubmissionSearchWorker

        self.submission_task = SubmissionSearchWorker(cik_selected)
        self.submission_thread = QThread()

        self.submission_task.moveToThread(self.submission_thread)

        self.submission_thread.started.connect(self.submission_task.run)
        self.submission_task.finished.connect(self.handle_results)
        self.submission_task.finished.connect(self.submission_thread.quit)
        self.submission_task.finished.connect(self.submission_task.deleteLater)
        self.submission_thread.finished.connect(self.submission_thread.deleteLater)

        self.submission_thread.start()

    def handle_results(self, results: list[dict]):
        """Handle the submission results."""
        self.search_results.emit(results)
