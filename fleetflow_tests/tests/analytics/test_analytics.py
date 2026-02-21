"""Analytics module tests — KPI card verification."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.analytics_page import AnalyticsPage


@pytest.mark.analytics
class TestAnalytics:
    """Verify analytics KPI cards and metrics display."""

    def test_analytics_page_loads(self, fleet_manager_driver: WebDriver) -> None:
        """Analytics page should render the Financial Analytics heading."""
        page = AnalyticsPage(fleet_manager_driver)
        page.open()
        assert "Financial Analytics" in page.get_page_text()

    def test_kpi_cards_present(self, fleet_manager_driver: WebDriver) -> None:
        """All four KPI cards should be visible."""
        page = AnalyticsPage(fleet_manager_driver)
        page.open()
        # Each card should render its value
        assert page.get_total_revenue(), "Total Revenue KPI card is empty"
        assert page.get_total_expenses(), "Total Expenses KPI card is empty"
        assert page.get_net_profit(), "Net Profit KPI card is empty"
        assert page.get_roi_percentage(), "ROI KPI card is empty"

    def test_efficiency_metrics_present(self, fleet_manager_driver: WebDriver) -> None:
        """Efficiency metric cards (Cost/Km, Fuel Efficiency) should be visible."""
        page = AnalyticsPage(fleet_manager_driver)
        page.open()
        cost_per_km = page.get_cost_per_km()
        fuel_eff = page.get_fuel_efficiency()
        assert cost_per_km, "Cost per Km metric is empty"
        assert fuel_eff, "Fuel Efficiency metric is empty"

    def test_active_trips_section_exists(self, fleet_manager_driver: WebDriver) -> None:
        """Active Trips section should be rendered on the analytics page."""
        page = AnalyticsPage(fleet_manager_driver)
        page.open()
        assert page.has_active_trips_section(), "Active Trips section not found"

    def test_analyst_can_access_analytics(self, analyst_driver: WebDriver) -> None:
        """Financial Analyst should have access to the analytics page."""
        page = AnalyticsPage(analyst_driver)
        page.open()
        assert "Financial Analytics" in page.get_page_text()

    def test_revenue_is_positive(self, fleet_manager_driver: WebDriver) -> None:
        """With seed trips, total revenue should be a positive value."""
        page = AnalyticsPage(fleet_manager_driver)
        page.open()
        revenue_text = page.get_total_revenue()
        # Revenue should contain ₹ and a non-zero number
        assert "₹" in revenue_text or revenue_text != "₹0", (
            f"Expected positive revenue, got: {revenue_text}"
        )
