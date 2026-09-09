"""Reusable back/forward navigation controls."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class NavigationBar(QWidget):
    """Navigation bar widget."""

    back_requested = Signal()
    forward_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # back and forward buttons
        self.back_button = QPushButton("<")
        self.back_button.setFixedWidth(30)

        self.forward_button = QPushButton(">")
        self.forward_button.setFixedWidth(30)

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.back_button)
        layout.addWidget(self.forward_button)

        self.back_button.clicked.connect(self.back_requested)
        self.forward_button.clicked.connect(self.forward_requested)

    
