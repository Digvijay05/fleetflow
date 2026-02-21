"""Login page object."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for /login."""

    # ── Locators ──
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".text-danger-700, .text-red-600")
    HEADING = (By.XPATH, "//h1[contains(text(),'FleetFlow')]")

    # ── Actions ──

    def open(self) -> "LoginPage":
        self.navigate("/login")
        self.wait_visible(*self.EMAIL_INPUT)
        return self

    def login(self, email: str, password: str) -> None:
        """Fill credentials and submit the login form."""
        self.type_text(*self.EMAIL_INPUT, email)
        self.type_text(*self.PASSWORD_INPUT, password)
        self.click(*self.SUBMIT_BUTTON)

    def get_error(self) -> str:
        """Return the error message text shown on invalid login."""
        return self.get_text(*self.ERROR_MESSAGE)

    def is_submit_disabled(self) -> bool:
        elem = self.wait_present(*self.SUBMIT_BUTTON)
        return not elem.is_enabled()
