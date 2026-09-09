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

        # dispatchers
        self.company_search_dispatcher = company_search_dispatcher
        self.submission_search_dispatcher = submission_search_dispatcher

        # toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.navigation_bar = NavigationBar()
        toolbar.addWidget(self.navigation_bar)

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

    def show_email_setup(self):
        """Show the email setup page."""

        self.pages.setCurrentWidget(self.email_setup_page)

    def show_company_search(self):
        """Show the company search page."""

        self.pages.setCurrentWidget(self.company_search_page)

    def show_company_results(self, search_term: str):
        """Show company search results."""

        page = CompanyResultsPage(
            self.company_search_dispatcher,
            search_term,
        )

        page.cik_selected.connect(
            self.show_company_submissions
        )

        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

        self.company_search_dispatcher.start(search_term)

    def show_company_submissions(self, cik: str):
        """Show company submissions."""

        page = CompanySubmissionsPage(
            self.submission_search_dispatcher,
            cik,
        )

        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

        self.submission_search_dispatcher.start(cik)