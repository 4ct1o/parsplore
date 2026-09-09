"""Company Submissions Page."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class CompanySubmissionsPage(QWidget):
    """Company submissions page."""

    accession_number = Signal(str)

    def __init__(self, dispatcher, cik: str):
        super().__init__()

        # Submission search dispatcher
        self.submission_search_dispatcher = dispatcher

        # Store CIK
        self.cik = cik

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        form_label = QLabel("Form")
        date_label = QLabel("Date")

        form_label.setFixedWidth(100)
        date_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        header_layout.addWidget(form_label)
        header_layout.addWidget(date_label)
        header_layout.addSpacing(30)

        main_layout.addLayout(header_layout)

        # Header line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)

        main_layout.addWidget(line)

        # Results
        self.results_layout = QVBoxLayout()
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(0)

        main_layout.addLayout(self.results_layout)
        main_layout.addStretch()

        # Connect dispatcher
        self.submission_search_dispatcher.search_results.connect(
            self.show_results
        )

    def show_results(self, results):
        """Display submission search results."""

        for submission in results:
            form = submission["form"]
            date = submission["filingDate"]
            accession_number = submission["accessionNumber"]

            submission_row = QHBoxLayout()
            submission_row.setContentsMargins(0, 0, 0, 0)
            submission_row.setSpacing(0)

            form_label = QLabel(form)
            form_label.setFixedWidth(100)

            date_label = QLabel(date)
            date_label.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Preferred
            )

            button = QPushButton(">")
            button.setFixedWidth(30)

            button.clicked.connect(
                lambda checked=False,
                accession_number=accession_number:
                self.accession_number.emit(accession_number)
            )

            submission_row.addWidget(form_label)
            submission_row.addWidget(date_label)
            submission_row.addWidget(button)

            self.results_layout.addLayout(submission_row)

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