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
    def __init__(self, ticker_service):
        super().__init__()

        self.ticker_service = ticker_service

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

    search_term = Signal(str)

    def handle_search(self):
        """Emit the search term signal."""
        term = self.search_input.text()
        if term:
            self.search_term.emit(term)

