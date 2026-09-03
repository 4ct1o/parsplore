"""SEC tasks."""

from PySide6.QtCore import QObject, QThread, Signal, Slot

class SECTickerTask(QObject):
    """Task to validate and update the ticker database with SEC data."""
    finished = Signal()

    def __init__(self):
        super().__init__()

    @Slot()
    def run(self):
        """Run the task."""
        from validators.sec_validator import is_ticker_file_up_to_date
        from data.sec_storage import save_tickers

        try:
            if not is_ticker_file_up_to_date():
                save_tickers()
        
        except Exception as e:
            print(f"Error in SECTickerTask: {e}")
        
        finally:
            self.finished.emit()

class SECSearchTask(QObject):
    """Task to search for a company in the SEC database."""
    finished = Signal(list)

    def __init__(self, search_term: str):
        super().__init__()
        self.search_term = search_term

    @Slot()
    def run(self):
        """Run the task."""
        from services.sec_service import search_company
        results = search_company(self.search_term, limit=10)
        self.finished.emit(results)
