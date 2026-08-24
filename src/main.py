import os
import sys

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow

from ui.email_setup_window import EmailSetupWindow
from ui.main_window import MainWindow

def main():
    load_dotenv()

    app = QApplication(sys.argv)

    email = os.getenv("USER_EMAIL")

    if email:
        window = MainWindow()
    else:
        window = EmailSetupWindow()

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()