"""Main application."""

import sys

from PySide6.QtWidgets import QApplication

from ui.email_setup_window import EmailSetupWindow
from ui.main_window import MainWindow
from config.settings import load_settings
from validators.email_validator import is_valid_email

class Application(QApplication):
    """Main application class."""
    def __init__(self, argv):
        super().__init__(argv)

        self.window = None

    def start(self):
        """Start the application by checking for a valid email"""
        settings = load_settings()
        email = settings.get("email")

        if is_valid_email(email):
            self.show_main_window()
        else:
            self.show_email_setup_window()

    def show_email_setup_window(self):
        """Show the email setup window."""
        self.window = EmailSetupWindow()
        self.window.email_saved.connect(self.show_main_window)
        self.window.show()

    def show_main_window(self):
        """Show the main application window."""
        if self.window:
            self.window.close()

        self.window = MainWindow()
        self.window.show()

def main():
    """Start the application."""

    app = Application(sys.argv)

    app.start()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
