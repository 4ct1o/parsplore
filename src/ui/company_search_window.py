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

class CompanySearchWindow(QWidget):
    """Company search window."""

    cik_selected = Signal(str)

    def __init__(self, dispatcher, search_term: str):
        super().__init__()
        # load settings
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

        # company search dispatcher
        self.company_search_dispatcher = dispatcher

        # connect > button to dispatcher
        self.company_search_dispatcher.search_results.connect(
            self.show_results
        )

    def show_results(self, results):

        for company in results:
            # extract company information
            title, ticker, cik, score = company

            # results layout
            search_row = QHBoxLayout()

            company_info_label = QLabel(f"{title} ({ticker})")
            company_info_label.setAlignment(Qt.AlignLeft)

            button = QPushButton(">")
            button.setFixedWidth(30)

            # connect button to emit cik
            button.clicked.connect(
                lambda checked=False, company_cik=cik: self.cik_selected.emit(company_cik)
            )

            # continue layout
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
