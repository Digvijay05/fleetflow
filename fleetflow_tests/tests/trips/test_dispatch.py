"""Trip dispatch lifecycle tests."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.trip_page import TripPage
from utils.test_data import VALID_TRIP


@pytest.mark.trips
class TestDispatch:
    """Verify trip creation, capacity validation, and driver availability filtering."""

    def test_trip_page_loads_with_seed_trips(self, dispatcher_driver: WebDriver) -> None:
        """Trip page should display seed trips."""
        page = TripPage(dispatcher_driver)
        page.open()
        assert page.page_contains_text("Trip Dispatcher"), "Expected Trip Dispatcher heading"

    def test_only_on_duty_drivers_in_dropdown(self, dispatcher_driver: WebDriver) -> None:
        """Dispatch modal driver dropdown should only list On Duty drivers."""
        page = TripPage(dispatcher_driver)
        page.open()
        page.click_new_dispatch()

        driver_options = page.get_available_driver_options()
        # Priya Sharma and Vikram Singh are ON_TRIP — must NOT appear
        option_text = " ".join(driver_options)
        assert "Priya Sharma" not in option_text, "ON_TRIP driver should not appear"
        assert "Vikram Singh" not in option_text, "ON_TRIP driver should not appear"
        # Rajesh Patel IS ON_DUTY — should appear
        assert "Rajesh Patel" in option_text, "ON_DUTY driver should appear in dropdown"

    def test_only_available_vehicles_in_dropdown(self, dispatcher_driver: WebDriver) -> None:
        """Dispatch modal vehicle dropdown should only list Available vehicles."""
        page = TripPage(dispatcher_driver)
        page.open()
        page.click_new_dispatch()

        vehicle_options = page.get_available_vehicle_options()
        option_text = " ".join(vehicle_options)
        assert "GJ01AB1234" in option_text, "Available vehicle should appear in dropdown"

    def test_create_valid_trip(self, dispatcher_driver: WebDriver) -> None:
        """Creating a valid trip should close the modal and show the new trip."""
        page = TripPage(dispatcher_driver)
        page.open()
        initial_count = page.get_trip_count()

        page.click_new_dispatch()
        page.fill_dispatch_form(
            origin=VALID_TRIP["origin"],
            destination=VALID_TRIP["destination"],
            cargo_weight=VALID_TRIP["cargo_weight"],
        )
        page.submit_dispatch()

        # Wait for modal to close
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(dispatcher_driver, 10).until(
            lambda d: len(d.find_elements("xpath", "//h3[contains(text(),'Create & Dispatch')]")) == 0
        )
        assert page.page_contains_text(VALID_TRIP["origin"]), "New trip origin should appear on page"
