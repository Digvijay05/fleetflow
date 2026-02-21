"""Trip page object."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class TripPage(BasePage):
    """Page object for /trips -- dispatch modal and trip cards."""

    # -- Locators --
    NEW_DISPATCH_BUTTON = (By.XPATH, "//button[contains(.,'New Dispatch')]")
    MODAL_HEADING = (By.XPATH, "//h3[contains(text(),'Create & Dispatch')]")

    # Dispatch modal fields
    VEHICLE_SELECT = (By.XPATH, "//label[contains(text(),'Select Vehicle')]/following-sibling::select")
    DRIVER_SELECT = (By.XPATH, "//label[contains(text(),'Select Driver')]/following-sibling::select")
    ORIGIN_INPUT = (By.XPATH, "//label[contains(text(),'Start Location')]/following-sibling::input")
    DESTINATION_INPUT = (By.XPATH, "//label[contains(text(),'Destination')]/following-sibling::input")
    CARGO_INPUT = (By.XPATH, "//label[contains(text(),'Cargo Weight')]/following-sibling::input")
    DISPATCH_BUTTON = (By.XPATH, "//button[contains(.,'Dispatch Trip')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(),'Cancel')]")

    # Trip cards
    TRIP_CARDS = (By.CSS_SELECTOR, ".bg-white.rounded-xl.shadow-sm, .bg-white.rounded-xl.border")
    COMPLETE_BUTTON = (By.XPATH, "//button[contains(.,'Complete')]")

    # -- Actions --

    def open(self) -> "TripPage":
        self.navigate("/trips")
        self.wait_visible(By.XPATH, "//h2[contains(text(),'Trip')]")
        return self

    def click_new_dispatch(self) -> None:
        self.click(*self.NEW_DISPATCH_BUTTON)
        self.wait_visible(*self.MODAL_HEADING)

    def fill_dispatch_form(
        self,
        origin: str,
        destination: str,
        cargo_weight: int,
        vehicle_index: int = 1,
        driver_index: int = 1,
    ) -> None:
        """Fill the dispatch modal. vehicle/driver indices are 1-based (skip placeholder)."""
        self.select_by_index(*self.VEHICLE_SELECT, vehicle_index)
        self.select_by_index(*self.DRIVER_SELECT, driver_index)
        self.type_text(*self.ORIGIN_INPUT, origin)
        self.type_text(*self.DESTINATION_INPUT, destination)
        self.type_text(*self.CARGO_INPUT, str(cargo_weight))

    def submit_dispatch(self) -> None:
        """Click dispatch and handle any alert."""
        self.click(*self.DISPATCH_BUTTON)
        self.dismiss_alert_if_present()

    def cancel_dispatch(self) -> None:
        self.click(*self.CANCEL_BUTTON)

    def get_trip_count(self) -> int:
        """Return the number of trip cards on the page."""
        return len(self.driver.find_elements(*self.TRIP_CARDS))

    def get_available_driver_options(self) -> list[str]:
        """Return text of all options in the driver <select> (skip placeholder)."""
        elem = self.wait_visible(*self.DRIVER_SELECT)
        options = elem.find_elements(By.TAG_NAME, "option")
        return [o.text for o in options if o.get_attribute("value")]

    def get_available_vehicle_options(self) -> list[str]:
        """Return text of all options in the vehicle <select> (skip placeholder)."""
        elem = self.wait_visible(*self.VEHICLE_SELECT)
        options = elem.find_elements(By.TAG_NAME, "option")
        return [o.text for o in options if o.get_attribute("value")]

    def page_contains_text(self, text: str) -> bool:
        return text in self.get_page_text()
