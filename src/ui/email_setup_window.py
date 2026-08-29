"""Email setup window."""

from PySide6.QtWidgets import (
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
from services.email_service import process_email


class EmailSetupWindow(QWidget):
    """Email setup window."""
    def __init__(self):
        super().__init__()

        settings = load_settings()

        self.setWindowTitle(f"{settings.get('app_name', 'parsplore()')} - Email Setup")
        self.resize(settings.get('window_width', 800), settings.get('window_height', 600))

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("username@domain.xxx")

        self.continue_button = QPushButton("Continue")

        email_row = QHBoxLayout()
        email_row.addWidget(self.email_label)
        email_row.addWidget(self.email_input)

        form_widget = QWidget()
        form_widget.setFixedWidth(250)

        form = QVBoxLayout(form_widget)
        form.addLayout(email_row)
        form.addWidget(self.continue_button)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(form_widget, alignment=Qt.AlignCenter)

        self.continue_button.clicked.connect(self.handle_continue)

    email_saved = Signal()

    def handle_continue(self):
        """Process the email input and emit a signal if saved successfully."""
        email = self.email_input.text()

        if process_email(email):
            self.email_saved.emit()
