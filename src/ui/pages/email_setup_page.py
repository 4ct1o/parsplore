"""Email Setup Page."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.email_service import process_email


class EmailSetupPage(QWidget):
    """Email setup page."""

    email_saved = Signal()

    def __init__(self):
        super().__init__()

        # Email
        email_label = QLabel("Email:")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(
            "username@domain.xxx"
        )

        self.continue_button = QPushButton("Continue")

        # Email row
        email_row = QHBoxLayout()
        email_row.addWidget(email_label)
        email_row.addWidget(self.email_input)

        # Form widget
        form_widget = QWidget()
        form_widget.setFixedWidth(250)

        form_layout = QVBoxLayout(form_widget)
        form_layout.addLayout(email_row)
        form_layout.addWidget(self.continue_button)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(
            form_widget,
            alignment=Qt.AlignCenter
        )

        # Connect
        self.continue_button.clicked.connect(
            self.handle_continue
        )

    def handle_continue(self):
        """Process the email and emit a signal if saved."""

        email = self.email_input.text()

        if process_email(email):
            self.email_saved.emit()