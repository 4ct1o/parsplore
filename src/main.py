"""Main application."""

import sys

from PySide6.QtWidgets import QApplication

from dispatchers.sec_dispatchers import (
    TickerUpdateDispatcher,
    CompanySearchDispatcher,
    SubmissionSearchDispatcher,
)

from ui.main_window import MainWindow


class Application(QApplication):
    """Main application."""

    def __init__(self, argv):
        super().__init__(argv)

        # Application services
        self.ticker_update_dispatcher = TickerUpdateDispatcher()
        self.company_search_dispatcher = CompanySearchDispatcher()
        self.submission_search_dispatcher = SubmissionSearchDispatcher()

        # Main window
        self.window = MainWindow(
            self.ticker_update_dispatcher,
            self.company_search_dispatcher,
            self.submission_search_dispatcher,
        )

    def start(self):
        """Start the application."""

        self.window.show()


def main():
    app = Application(sys.argv)
    app.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()