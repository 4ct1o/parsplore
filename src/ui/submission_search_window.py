"""Submission search window."""

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

class SubmissionSearchWindow(QWidget):
    """Submision search window."""

    accession_number = Signal(str)

    def __init__(self, dispatcher, cik: str):
        super().__init__()
        # load settings
        settings = load_settings()

        self.setWindowTitle(f"{settings.get('app_name', 'parsplore()')} - Submission Search")
        self.resize(settings.get('window_width', 800), settings.get('window_height', 600))

        # top layout
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

        # submission search dispatcher
        self.submission_search_dispatcher = dispatcher

        # connect > button to dispatcher
        self.submission_search_dispatcher.search_results.connect(
            self.show_results
        )

    def show_results(self, results):

        for submission in results:
            # extract form type and filing date
            form, date = submission['form'], submission['filingDate']

            # results layout
            submission_row = QHBoxLayout()
            submission_row.setContentsMargins(0, 0, 0, 0)
            submission_row.setSpacing(0)

            form_label = QLabel(form)
            form_label.setFixedWidth(100)

            date_label = QLabel(date)
            date_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            button = QPushButton(">")
            button.setFixedWidth(30)

            # connect button to emit accesion number
            button.clicked.connect(
                lambda checked=False, accession_number=submission['accessionNumber']: self.accession_number.emit(accession_number)
            )

            # continue layout
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