"""Authentication tests — valid login, invalid credentials, role redirect."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.login_page import LoginPage
from utils.assertions import assert_current_url_contains
from utils.test_data import (
    CUSTOMER,
    DISPATCHER,
    FLEET_MANAGER,
    INVALID_USER,
    WRONG_PASSWORD,
)


@pytest.mark.auth
class TestLogin:
    """Verify authentication flows for all user roles."""

    def test_fleet_manager_login_redirects_to_dashboard(self, driver: WebDriver) -> None:
        """Fleet Manager login should redirect to /dashboard."""
        page = LoginPage(driver)
        page.open()
        page.login(FLEET_MANAGER.email, FLEET_MANAGER.password)
        page.wait_url_contains("/dashboard")
        assert_current_url_contains(driver, "/dashboard")

    def test_dispatcher_login_redirects_to_dashboard(self, driver: WebDriver) -> None:
        """Dispatcher login should redirect to /dashboard."""
        page = LoginPage(driver)
        page.open()
        page.login(DISPATCHER.email, DISPATCHER.password)
        page.wait_url_contains("/dashboard")
        assert_current_url_contains(driver, "/dashboard")

    def test_customer_login_redirects_to_tracking(self, driver: WebDriver) -> None:
        """Customer login should redirect to /tracking."""
        page = LoginPage(driver)
        page.open()
        page.login(CUSTOMER.email, CUSTOMER.password)
        page.wait_url_contains("/tracking")
        assert_current_url_contains(driver, "/tracking")

    def test_invalid_email_shows_error(self, driver: WebDriver) -> None:
        """Non-existent user should show an error message."""
        page = LoginPage(driver)
        page.open()
        page.login(INVALID_USER.email, INVALID_USER.password)
        error = page.get_error()
        assert error, "Expected an error message for invalid credentials"

    def test_wrong_password_shows_error(self, driver: WebDriver) -> None:
        """Correct email with wrong password should show an error."""
        page = LoginPage(driver)
        page.open()
        page.login(WRONG_PASSWORD.email, WRONG_PASSWORD.password)
        error = page.get_error()
        assert error, "Expected an error message for wrong password"

    def test_unauthenticated_redirect_to_login(self, driver: WebDriver) -> None:
        """Accessing /dashboard without login should redirect to /login."""
        from pages.base_page import BasePage
        page = BasePage(driver)
        page.navigate("/dashboard")
        page.wait_url_contains("/login")
        assert_current_url_contains(driver, "/login")
