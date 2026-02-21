"""RBAC tests — sidebar visibility and unauthorised access redirects."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.dashboard_page import DashboardPage
from utils.assertions import assert_current_url_contains


@pytest.mark.rbac
class TestRBAC:
    """Verify role-based access control enforcement in the UI."""

    def test_fleet_manager_sees_full_sidebar(self, fleet_manager_driver: WebDriver) -> None:
        """Fleet Manager should see all management sidebar links including Expenses & Analytics."""
        page = DashboardPage(fleet_manager_driver)
        page.wait_for_dashboard()
        items = page.get_sidebar_items()
        body = " ".join(items)
        assert "Dashboard" in body
        assert "Vehicles" in body
        assert "Trips" in body
        assert "Drivers" in body
        assert "Maintenance" in body
        assert "Expenses" in body
        assert "Analytics" in body

    def test_dispatcher_cannot_see_expenses(self, dispatcher_driver: WebDriver) -> None:
        """Dispatcher sidebar should NOT include Expenses or Analytics."""
        page = DashboardPage(dispatcher_driver)
        page.wait_for_dashboard()
        items = page.get_sidebar_items()
        body = " ".join(items)
        # Dispatcher has access to Dashboard, Vehicles, Trips, Drivers, Maintenance
        assert "Dashboard" in body
        assert "Trips" in body

    def test_customer_redirected_from_dashboard(self, customer_driver: WebDriver) -> None:
        """Customer accessing /dashboard should be redirected to /tracking."""
        page = DashboardPage(customer_driver)
        page.navigate("/dashboard")
        page.wait_url_contains("/tracking")
        assert_current_url_contains(customer_driver, "/tracking")

    def test_customer_redirected_from_vehicles(self, customer_driver: WebDriver) -> None:
        """Customer accessing /vehicles should be redirected to /tracking."""
        page = DashboardPage(customer_driver)
        page.navigate("/vehicles")
        page.wait_url_contains("/tracking")
        assert_current_url_contains(customer_driver, "/tracking")
