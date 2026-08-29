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

from PySide6.QtCore import Qt

from config.settings import load_settings

class MainWindow(QMainWindow):
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
