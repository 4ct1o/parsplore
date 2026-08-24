from PySide6.QtWidgets import (
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)
from PySide6.QtCore import Qt

from config.settings import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT

class EmailSetupWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Email Setup")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

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