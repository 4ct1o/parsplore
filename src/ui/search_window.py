"""Search windows."""

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)

from config.settings import load_settings
from services.sec_service import search_company
from clients.sec_client import get_latest_submissions
from tasks.sec_tasks import SECSearchTask

class CompanySearchWindow(QWidget):
    """Company search window."""

    def __init__(self, company_search_service, search_term: str):
        super().__init__()

        settings = load_settings()

        self.setWindowTitle(f"{settings.get('app_name', 'parsplore()')} - Company Search")
        self.resize(settings.get('window_width', 800), settings.get('window_height', 600))

        # main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.company_title_label = QLabel('Company (Ticker):')
        self.company_title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.main_layout.addWidget(self.company_title_label)

        self.results_layout = QVBoxLayout()
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(0)

        self.main_layout.addLayout(self.results_layout)

        self.main_layout.addStretch() 

        # search results
        self.company_search_service = company_search_service

        self.company_search_service.company_search_completed.connect(
            self.show_results
        )

    cik_selected = Signal(str)

    def show_results(self, results):

        for company in results:
            title, ticker, cik, score = company

            search_row = QHBoxLayout()

            company_info_label = QLabel(f"{title} ({ticker})")
            company_info_label.setAlignment(Qt.AlignLeft)

            button = QPushButton(">")
            button.setFixedWidth(30)

            button.clicked.connect(
                lambda checked=False, cik_selected=cik: self.select_cik(cik_selected) # CHANGE ME
            )

            search_row.addWidget(company_info_label)
            search_row.addStretch()
            search_row.addWidget(button)

            self.results_layout.addLayout(search_row)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Plain)

            line.setStyleSheet("""
                QFrame {
                    color: #252525;
                    background-color: #252525;
                    border: none;
                    max-height: 1px;
                }
            """)

            self.results_layout.addWidget(line)

    def select_cik(self, cik: str): #                                            DELETE ME
        print(f"Selected CIK: {cik!r}")
        self.cik_selected.emit(str(cik))


class SubmissionSearchWindow(QWidget):
    """Submision search window."""

    def __init__(self, submission_search_service, cik: str):
        super().__init__()

        self.submission_search_service = submission_search_service

        settings = load_settings()

        self.setWindowTitle(f"{settings.get('app_name', 'parsplore()')} - Submission Search")
        self.resize(settings.get('window_width', 800), settings.get('window_height', 600))

        # main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(0)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        form_label = QLabel("Form")
        date_label = QLabel("Date")

        form_label.setFixedWidth(100)
        date_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        header_layout.addWidget(form_label)
        header_layout.addWidget(date_label)
        header_layout.addSpacing(30)

        self.main_layout.addLayout(header_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)

        self.main_layout.addWidget(line)

        self.results_layout = QVBoxLayout()
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(0)
        
        self.main_layout.addLayout(self.results_layout)
        self.main_layout.addStretch()

        self.submission_search_service.submissions_fetched.connect(
            self.show_results
        )

    def show_results(self, results):

        for submission in results:
            form, date = submission['form'], submission['filingDate']

            submission_row = QHBoxLayout()
            submission_row.setContentsMargins(0, 0, 0, 0)
            submission_row.setSpacing(0)

            form_label = QLabel(form)
            form_label.setFixedWidth(100)

            date_label = QLabel(date)
            date_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            button = QPushButton(">")
            button.setFixedWidth(30)

            button.clicked.connect(
                lambda checked=False, accession_number=submission['accessionNumber']: self.accession_number.emit(accession_number)
            )

            submission_row.addWidget(form_label)
            submission_row.addWidget(date_label)
            submission_row.addWidget(button)

            self.results_layout.addLayout(submission_row)

            self.main_layout.addLayout(submission_row)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Plain)
            
            line.setStyleSheet("""
                QFrame {
                    color: #252525;
                    background-color: #252525;
                    border: none;
                    max-height: 1px;
                            }
            """)
