"""Vehicle page object."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class VehiclePage(BasePage):
    """Page object for /vehicles."""

    # -- Locators --
    ADD_BUTTON = (By.XPATH, "//button[contains(.,'Add Vehicle')]")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")
    MODAL = (By.XPATH, "//h3[contains(text(),'Add New Vehicle')]")

    # Modal fields
    LICENSE_PLATE_INPUT = (By.XPATH, "//label[contains(text(),'License Plate')]/following-sibling::input")
    MAKE_INPUT = (By.XPATH, "//label[contains(text(),'Make')]/following-sibling::input")
    MODEL_INPUT = (By.XPATH, "//label[contains(text(),'Model')]/following-sibling::input")
    YEAR_INPUT = (By.XPATH, "//label[contains(text(),'Year')]/following-sibling::input")
    CAPACITY_INPUT = (By.XPATH, "//label[contains(text(),'Capacity')]/following-sibling::input")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'Save Vehicle')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(),'Cancel')]")

    # -- Actions --

    def open(self) -> "VehiclePage":
        self.navigate("/vehicles")
        self.wait_visible(By.XPATH, "//h2[contains(text(),'Vehicle')]")
        return self

    def click_add_vehicle(self) -> None:
        self.click(*self.ADD_BUTTON)
        self.wait_visible(*self.MODAL)

    def fill_vehicle_form(self, plate: str, make: str, model: str, year: int, capacity: int) -> None:
        self.type_text(*self.LICENSE_PLATE_INPUT, plate)
        self.type_text(*self.MAKE_INPUT, make)
        self.type_text(*self.MODEL_INPUT, model)
        self.type_text(*self.YEAR_INPUT, str(year))
        self.type_text(*self.CAPACITY_INPUT, str(capacity))

    def submit_vehicle(self) -> None:
        """Click save and wait for modal to dismount / table to refresh."""
        self.click(*self.SAVE_BUTTON)
        # The frontend alert()s on API error (e.g., duplicate plate).
        self.dismiss_alert_if_present()
        # Wait for modal overlay to close
        self.wait_invisible(By.XPATH, "//h3[contains(text(),'Add New Vehicle')]")

    def wait_for_table_data(self) -> None:
        """Wait until at least one data row is present in the table."""
        self.wait.until(EC.presence_of_element_located(self.TABLE_ROWS))

    def get_table_row_count(self) -> int:
        self.wait_for_table_data()
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def get_all_license_plates(self) -> list[str]:
        """Return the first column text of every table row."""
        self.wait_for_table_data()
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        return [r.find_element(By.CSS_SELECTOR, "td:first-child").text for r in rows]

    def get_vehicle_status(self, plate: str) -> str:
        """Find a row by license plate and return its status badge text."""
        self.wait_for_table_data()
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            if cells[0].text == plate:
                return cells[4].text
        raise ValueError(f"Vehicle {plate} not found in table")
