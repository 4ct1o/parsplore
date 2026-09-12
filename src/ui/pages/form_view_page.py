"""Form view page."""

from PySide6.QtWidgets import (
    QWidget,
    QTextBrowser,
    QVBoxLayout,
)

class FormViewPage(QWidget):
    """Form view page."""

    def __init__(self, dispatcher, form_info: dict):
        super().__init__()

        # Form search dispatcher
        self.form_search_dispatcher = dispatcher

        # Text browser
        self.text_browser = QTextBrowser(self)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_browser)

        # Connect dispatcher
        self.form_search_dispatcher.form_results.connect(
            self.text_browser.setHtml
        )
