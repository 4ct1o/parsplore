"""SEC workers module."""

from PySide6.QtCore import QObject, Signal, Slot

class TickerUpdateWorker(QObject):
    """Task to validate and update the ticker database with SEC data."""
    finished = Signal()

    def __init__(self):
        super().__init__()

    @Slot()
    def run(self):
        """Run the task."""
        from validators.sec_validator import is_tickers_up_to_date
        from storage.sec_storage import save_tickers

        try:
            if not is_tickers_up_to_date():
                save_tickers()
        
        except Exception as e:
            print(f"Error in TickerUpdateWorker: {e}")
        
        finally:
            self.finished.emit()

class CompanySearchWorker(QObject):
    """Task to search for a company in the SEC database."""
    finished = Signal(list)

    def __init__(self, search_term: str):
        super().__init__()
        self.search_term = search_term

    @Slot()
    def run(self):
        """Run the task."""
        from services.sec_service import search_company
        results = search_company(self.search_term)
        self.finished.emit(results)

class SubmissionSearchWorker(QObject):
    """Task to get the latest submissions for a given CIK."""
    finished = Signal(list)

    def __init__(self, cik: str):
        super().__init__()
        self.cik = cik

    @Slot()
    def run(self):
        """Run the task."""
        from clients.sec_client import get_submissions
        results = get_submissions(self.cik, limit=10)
        self.finished.emit(results)

class FormSearchWorker(QObject):
    """Task to get the form data for a given CIK and accession number."""
    finished = Signal(str)

    def __init__(self, form_info: dict):
        super().__init__()
        self.form_info = form_info

    @Slot()
    def run(self):
        """Run the task."""
        from services.sec_service import create_submission_html
        results = create_submission_html(self.form_info)
        self.finished.emit(results)
