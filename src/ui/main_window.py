"""Main application window."""

from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QStackedWidget,
)

# local imports
from config.settings import load_settings
from ui.widgets.navigation_bar import NavigationBar

from ui.pages.company_search_page import CompanySearchPage
from ui.pages.company_results_page import CompanyResultsPage
from ui.pages.company_submissions_page import CompanySubmissionsPage
from ui.pages.email_setup_page import EmailSetupPage
from validators.email_validator import is_valid_email


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(
        self,
        ticker_update_dispatcher,
        company_search_dispatcher,
        submission_search_dispatcher,
    ):
        super().__init__()

        # load settings

        self.settings = load_settings()

        self.setWindowTitle(
            self.settings.get("app_name", "parsplore()")
        )

        self.resize(
            self.settings.get("window_width", 800),
            self.settings.get("window_height", 600),
        )

        # history
        self.navigation_history = []
        self.history_index = -1

        # dispatchers
        self.company_search_dispatcher = company_search_dispatcher
        self.submission_search_dispatcher = submission_search_dispatcher

        # toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.navigation_bar = NavigationBar()
        toolbar.addWidget(self.navigation_bar)

        self.navigation_bar.back_requested.connect(self.go_back)
        self.navigation_bar.forward_requested.connect(self.go_forward)

        # pages
        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

        self.email_setup_page = EmailSetupPage()
        self.company_search_page = CompanySearchPage(
            ticker_update_dispatcher
        )
        self.pages.addWidget(self.email_setup_page)
        self.pages.addWidget(self.company_search_page)

        # email setup -> company search flow
        self.email_setup_page.email_saved.connect(
            self.show_company_search
        )

        # search flow
        self.company_search_page.search_term.connect(
            self.show_company_results
        )

        # initial page
        email = self.settings.get("email")

        if is_valid_email(self.settings.get("email")):
            self.show_company_search()
        else:
            self.show_email_setup()

    def navigate_to(self, page: QWidget):
        """Navigate to a specific page."""

        if self.pages.indexOf(page) == -1:
            self.pages.addWidget(page)

        self.pages.setCurrentWidget(page)
        # remove forward history
        del self.navigation_history[self.history_index + 1 :]
        # add to history
        self.navigation_history.append(page)
        self.history_index += 1

    def go_back(self):
        """Go back to the previous page."""
        if self.history_index > 0:
            self.history_index -= 1
            previous_page = self.navigation_history[self.history_index]
            self.pages.setCurrentWidget(previous_page)

    def go_forward(self):
        """Go forward to the next page."""
        if self.history_index < len(self.navigation_history) - 1:
            self.history_index += 1
            next_page = self.navigation_history[self.history_index]
            self.pages.setCurrentWidget(next_page)

    def show_email_setup(self):
        """Show the email setup page."""

        self.navigate_to(self.email_setup_page)

    def show_company_search(self):
        """Show the company search page."""

        self.navigate_to(self.company_search_page)

    def show_company_results(self, search_term: str):
        """Show company search results."""

        page = CompanyResultsPage(
            self.company_search_dispatcher,
            search_term,
        )

        page.cik_selected.connect(
            self.show_company_submissions
        )

        self.navigate_to(page)

        self.company_search_dispatcher.start(search_term)

    def show_company_submissions(self, cik: str):
        """Show company submissions."""

        page = CompanySubmissionsPage(
            self.submission_search_dispatcher,
            cik,
        )

        self.navigate_to(page)

        self.submission_search_dispatcher.start(cik)
