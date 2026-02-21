"""Maintenance module tests."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.maintenance_page import MaintenancePage
from pages.vehicle_page import VehiclePage
from utils.test_data import NEW_MAINTENANCE


@pytest.mark.maintenance
class TestMaintenance:
    """Verify maintenance logging and vehicle status transitions."""

    def test_maintenance_page_loads(self, fleet_manager_driver: WebDriver) -> None:
        """Maintenance page should render the heading."""
        page = MaintenancePage(fleet_manager_driver)
        page.open()
        assert "Maintenance Central" in page.get_page_text()

    def test_log_maintenance_creates_record(self, fleet_manager_driver: WebDriver) -> None:
        """Logging a maintenance record should add a row to the table."""
        page = MaintenancePage(fleet_manager_driver)
        page.open()

        page.click_log_service()
        page.fill_maintenance_form(
            maint_type=NEW_MAINTENANCE["type"],
            description=NEW_MAINTENANCE["description"],
            cost=NEW_MAINTENANCE["cost"],
        )
        page.submit_log()

        # Verify table has at least one row
        page.wait_visible(*page.TABLE_ROWS)
        assert page.get_table_row_count() >= 1, "Expected at least one maintenance record"

    def test_maintenance_sets_vehicle_in_shop(self, fleet_manager_driver: WebDriver) -> None:
        """After logging maintenance, the vehicle status should change to 'In Shop'."""
        # First log maintenance for GJ01AB1234 (Available vehicle)
        maint_page = MaintenancePage(fleet_manager_driver)
        maint_page.open()
        maint_page.click_log_service()
        maint_page.fill_maintenance_form(
            maint_type="Inspection",
            description="Pre-trip safety inspection",
            cost=2000.00,
        )
        maint_page.submit_log()

        # Now verify vehicle status changed to In Shop
        vehicle_page = VehiclePage(fleet_manager_driver)
        vehicle_page.open()
        status = vehicle_page.get_vehicle_status("GJ01AB1234")
        assert status == "In Shop", f"Expected 'In Shop' after maintenance, got '{status}'"
