"""Main application."""

import sys

from PySide6.QtWidgets import QApplication

from ui.email_setup_window import EmailSetupWindow
from ui.main_window import MainWindow
from ui.company_search_window import CompanySearchWindow
from ui.submission_search_window import SubmissionSearchWindow
from config.settings import load_settings
from validators.email_validator import is_valid_email
from dispatchers.sec_dispatchers import TickerUpdateDispatcher, CompanySearchDispatcher, SubmissionSearchDispatcher

class Application(QApplication):
    """Main application class."""
    def __init__(self, argv):
        super().__init__(argv)

        self.window = None

        # dispatchers
        self.ticker_update_dispatcher = TickerUpdateDispatcher()
        self.company_search_dispatcher = CompanySearchDispatcher()
        self.submission_search_dispatcher = SubmissionSearchDispatcher()

    def start(self):
        """Start the application"""
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

        self.window = MainWindow(self.ticker_update_dispatcher)
        self.window.search_term.connect(self.show_company_search_window)
        self.window.show()

    def show_company_search_window(self, search_term: str):
        """Show the company search window."""
        if self.window:
            self.window.close()

        self.window = CompanySearchWindow(
            self.company_search_dispatcher,
            search_term
        )

        self.window.cik_selected.connect(self.show_submission_search_window)

        self.company_search_dispatcher.start(search_term)

        self.window.show()

    def show_submission_search_window(self, cik: str):
        """Show the submission search window."""

        if self.window:
            self.window.close()

        self.submission_search_dispatcher.start(cik)

        self.window = SubmissionSearchWindow(
            self.submission_search_dispatcher,
            cik
        )
        self.window.show()

def main():
    """Start the application."""

    app = Application(sys.argv)

    app.start()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
