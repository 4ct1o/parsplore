import sys

from PySide6.QtWidgets import QApplication

from ui.email_setup_window import EmailSetupWindow


app = QApplication(sys.argv)

window = EmailSetupWindow()
window.show()

sys.exit(app.exec())