"""Search windows."""

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel
)

from PySide6.QtCore import (
    Qt,
    Signal
)

from config.settings import load_settings
from services.sec_service import search_company

class CompanySearchWindow(QWidget):
    """Company search window."""
    def __init__(self, search_term: str):
        super().__init__()

        settings = load_settings()

        self.setWindowTitle(f"{settings.get('app_name', 'parsplore()')} - Company Search")
        self.resize(settings.get('window_width', 800), settings.get('window_height', 600))

        self.company_title_label = QLabel('Company (Ticker):')

        results = search_company(search_term, limit=10)

        for company in results:
            title, ticker, cik, score = company
            company_info_label = QLabel(f"{title} ({ticker})")
            company_info_label.setAlignment(Qt.AlignLeft)
            self.layout().addWidget(company_info_label)
        





