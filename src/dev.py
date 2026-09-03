"""Development script to test windows and functionalities."""

import sys

from PySide6.QtWidgets import QApplication

from ui.email_setup_window import EmailSetupWindow
from ui.main_window import MainWindow
from ui.search_window import CompanySearchWindow


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
