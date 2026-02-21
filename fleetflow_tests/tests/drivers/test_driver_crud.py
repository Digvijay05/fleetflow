"""Driver CRUD tests."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.driver_page import DriverPage
from utils.test_data import NEW_DRIVER


@pytest.mark.drivers
class TestDriverCrud:
    """Verify driver creation and table display."""

    def test_driver_page_loads(self, fleet_manager_driver: WebDriver) -> None:
        """Driver page must show the seed drivers."""
        page = DriverPage(fleet_manager_driver)
        page.open()
        assert page.get_table_row_count() > 0, "Expected seed drivers in table"

    def test_add_driver_appears_in_table(self, fleet_manager_driver: WebDriver) -> None:
        """Adding a driver should make them appear in the table."""
        page = DriverPage(fleet_manager_driver)
        page.open()

        page.click_add_driver()
        page.fill_driver_form(
            name=NEW_DRIVER["name"],
            license_number=NEW_DRIVER["license_number"],
            expiry=NEW_DRIVER["license_expiry"],
        )
        page.submit_driver()

        # Wait for table to refresh
        page.wait_visible(*page.TABLE_ROWS)
        names = page.get_all_driver_names()
        assert NEW_DRIVER["name"] in names, f"New driver '{NEW_DRIVER['name']}' not found in table"

    def test_on_trip_drivers_show_correct_status(self, fleet_manager_driver: WebDriver) -> None:
        """Drivers assigned to active trips should show 'On Trip' status."""
        page = DriverPage(fleet_manager_driver)
        page.open()
        status = page.get_driver_status("Priya Sharma")
        assert status == "On Trip", f"Expected 'On Trip' for Priya Sharma, got '{status}'"

    def test_rajesh_patel_is_on_duty(self, fleet_manager_driver: WebDriver) -> None:
        """Rajesh Patel (completed trip) should show 'On Duty'."""
        page = DriverPage(fleet_manager_driver)
        page.open()
        status = page.get_driver_status("Rajesh Patel")
        assert status == "On Duty", f"Expected 'On Duty' for Rajesh Patel, got '{status}'"
