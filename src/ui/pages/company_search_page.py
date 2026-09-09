"""Company Search Page"""

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
    Signal,
)

from config.settings import load_settings
from ui.widgets.navigation_bar import NavigationBar

class CompanySearchPage(QWidget):
    """Company search page."""

    search_term = Signal(str)

    def __init__(self, dispatcher):
        super().__init__()

        # Ticker update dispatcher
        self.ticker_update = dispatcher

        # Main layout
        self.layout = QVBoxLayout(self)

        # Search form
        self.search_label = QLabel("Company:")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "AAPL, Apple, Apple Inc. ..."
        )

        self.search_button = QPushButton(
            "Search for recent filings"
        )

        # Search row
        self.search_row = QHBoxLayout()
        self.search_row.addWidget(self.search_label)
        self.search_row.addWidget(self.search_input)

        # Form widget
        self.form_widget = QWidget()
        self.form_widget.setFixedWidth(230)

        self.form = QVBoxLayout(self.form_widget)
        self.form.addLayout(self.search_row)
        self.form.addWidget(self.search_button)

        # Add form to page
        self.layout.addWidget(
            self.form_widget,
            alignment=Qt.AlignCenter
        )

        # Connect search button
        self.search_button.clicked.connect(self.handle_search)

    def handle_search(self):
        """Emit the search term signal."""
        term = self.search_input.text()

        if term:
            self.search_term.emit(term)
