"""Main application window."""

from PySide6.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)

from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
)

from config.settings import load_settings
from tasks.sec_tasks import SECTickerTask

class MainWindow(QMainWindow):
    """Main application window."""
    def __init__(self):
        super().__init__()

        settings = load_settings()

        self.setWindowTitle(settings.get('app_name', 'parsplore()'))
        self.resize(settings.get('window_width', 800), settings.get('window_height', 600))

        self.search_label = QLabel("Company:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("AAPL, Apple, Apple Inc. ...")

        self.search_button = QPushButton("Search for recent filings")

        search_row = QHBoxLayout()
        search_row.addWidget(self.search_label)
        search_row.addWidget(self.search_input)

        form_widget = QWidget()
        form_widget.setFixedWidth(230)

        form = QVBoxLayout(form_widget)
        form.addLayout(search_row)
        form.addWidget(self.search_button)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        layout.addWidget(form_widget, alignment=Qt.AlignCenter)

        self.setCentralWidget(central_widget)

        self.search_button.clicked.connect(self.handle_search)

        self.start_sec_ticker_task()

    search_term = Signal(str)

    def handle_search(self):
        """Emit the search term signal."""
        term = self.search_input.text()
        if term:
            self.search_term.emit(term)

    def start_sec_ticker_task(self):
        """Start the SEC ticker task."""

        self.sec_ticker_task = SECTickerTask()
        self.sec_ticker_thread = QThread()

        self.sec_ticker_task.moveToThread(self.sec_ticker_thread)

        self.sec_ticker_thread.started.connect(self.sec_ticker_task.run)
        self.sec_ticker_task.finished.connect(self.sec_ticker_thread.quit)
        self.sec_ticker_task.finished.connect(self.sec_ticker_task.deleteLater)
        self.sec_ticker_thread.finished.connect(self.sec_ticker_thread.deleteLater)

        self.sec_ticker_thread.start()

