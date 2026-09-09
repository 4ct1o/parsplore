"""Company Results Page."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CompanyResultsPage(QWidget):
    """Company search results page."""

    cik_selected = Signal(str)

    def __init__(self, dispatcher, search_term: str):
        super().__init__()

        # Company search dispatcher
        self.company_search_dispatcher = dispatcher

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # Title
        company_title_label = QLabel("Company (Ticker):")
        company_title_label.setAlignment(
            Qt.AlignLeft | Qt.AlignTop
        )

        main_layout.addWidget(company_title_label)

        # Results
        self.results_layout = QVBoxLayout()
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(0)

        main_layout.addLayout(self.results_layout)
        main_layout.addStretch()

        # Connect dispatcher
        self.company_search_dispatcher.search_results.connect(
            self.show_results
        )

    def show_results(self, results):
        """Display company search results."""

        for company in results:
            title, ticker, cik, score = company

            search_row = QHBoxLayout()

            company_info_label = QLabel(
                f"{title} ({ticker})"
            )
            company_info_label.setAlignment(Qt.AlignLeft)

            button = QPushButton(">")
            button.setFixedWidth(30)

            button.clicked.connect(
                lambda checked=False,
                company_cik=cik:
                self.cik_selected.emit(company_cik)
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