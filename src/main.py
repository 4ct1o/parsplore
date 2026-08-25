import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ui.email_setup_window import EmailSetupWindow
from ui.main_window import MainWindow
from config.settings import load_settings
from validators.email_validator import is_valid_email

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.window = None

    def start(self):
        settings = load_settings()
        email = settings.get("email")

        if is_valid_email(email):
            self.show_main_window()
        else:
            self.show_email_setup_window()

    def show_email_setup_window(self):
        self.window = EmailSetupWindow()
        self.window.email_saved.connect(self.show_main_window)
        self.window.show()

    def show_main_window(self):
        if self.window:
            self.window.close()

        self.window = MainWindow()
        self.window.show()

def main():

    app = Application(sys.argv)

    app.start()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()