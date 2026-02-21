"""Dashboard / Layout page object — sidebar navigation and header."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page object for the authenticated layout (sidebar + header)."""

    # ── Locators ──
    SIDEBAR_LINKS = (By.CSS_SELECTOR, "nav a, aside a")
    ROLE_BADGE = (By.XPATH, "//*[contains(@class,'text-xs') and contains(@class,'uppercase')]")
    PAGE_HEADING = (By.CSS_SELECTOR, "h2")

    # ── Actions ──

    def wait_for_dashboard(self) -> None:
        """Wait until the sidebar is rendered (authenticated layout)."""
        self.wait_visible(By.CSS_SELECTOR, "nav, aside")

    def get_sidebar_items(self) -> list[str]:
        """Return list of sidebar link text values."""
        self.wait_visible(*self.SIDEBAR_LINKS)
        return self.get_texts(*self.SIDEBAR_LINKS)

    def navigate_via_sidebar(self, link_text: str) -> None:
        """Click a sidebar link by its visible text."""
        self.click(By.LINK_TEXT, link_text)

    def get_heading(self) -> str:
        return self.get_text(*self.PAGE_HEADING)

    def get_role_text(self) -> str:
        """Return the role badge text from the header."""
        return self.get_text(*self.ROLE_BADGE)
