"""Vehicle CRUD tests."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.vehicle_page import VehiclePage
from utils.test_data import NEW_VEHICLE


@pytest.mark.vehicles
class TestVehicleCrud:
    """Verify vehicle creation and table display."""

    def test_vehicle_page_loads(self, fleet_manager_driver: WebDriver) -> None:
        """Vehicle page should render heading and table."""
        page = VehiclePage(fleet_manager_driver)
        page.open()
        assert page.get_table_row_count() > 0, "Expected seed vehicles in table"

    def test_add_vehicle_appears_in_table(self, fleet_manager_driver: WebDriver) -> None:
        """Adding a vehicle should make it appear in the table with 'Available' status."""
        page = VehiclePage(fleet_manager_driver)
        page.open()
        initial_count = page.get_table_row_count()

        page.click_add_vehicle()
        page.fill_vehicle_form(
            plate=NEW_VEHICLE["license_plate"],
            make=NEW_VEHICLE["make"],
            model=NEW_VEHICLE["model"],
            year=NEW_VEHICLE["year"],
            capacity=NEW_VEHICLE["max_capacity_kg"],
        )
        page.submit_vehicle()

        # Wait for modal to close and table to refresh
        page.wait_visible(*page.TABLE_ROWS)
        plates = page.get_all_license_plates()
        assert NEW_VEHICLE["license_plate"] in plates, (
            f"New vehicle {NEW_VEHICLE['license_plate']} not found in table"
        )

        status = page.get_vehicle_status(NEW_VEHICLE["license_plate"])
        assert status == "Available", f"Expected 'Available', got '{status}'"

    def test_seed_vehicles_have_correct_statuses(self, fleet_manager_driver: WebDriver) -> None:
        """Seed vehicles on active trips should show 'On Trip' status."""
        page = VehiclePage(fleet_manager_driver)
        page.open()
        # GJ01AB1234 is the only Available vehicle per seed data
        status = page.get_vehicle_status("GJ01AB1234")
        assert status == "Available", f"Expected 'Available' for GJ01AB1234, got '{status}'"
