"""Driver page object."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class DriverPage(BasePage):
    """Page object for /drivers."""

    # -- Locators --
    ADD_BUTTON = (By.XPATH, "//button[contains(.,'Add Driver')]")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")
    MODAL = (By.XPATH, "//h3[contains(text(),'Register New Driver')]")

    # Modal fields
    NAME_INPUT = (By.XPATH, "//label[contains(text(),'Full Name')]/following-sibling::input")
    LICENSE_INPUT = (By.XPATH, "//label[contains(text(),'License Number')]/following-sibling::input")
    EXPIRY_INPUT = (By.XPATH, "//label[contains(text(),'License Expiry')]/following-sibling::input")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'Save Driver')]")

    # -- Actions --

    def open(self) -> "DriverPage":
        self.navigate("/drivers")
        self.wait_visible(By.XPATH, "//h2[contains(text(),'Driver')]")
        return self

    def click_add_driver(self) -> None:
        self.click(*self.ADD_BUTTON)
        self.wait_visible(*self.MODAL)

    def fill_driver_form(self, name: str, license_number: str, expiry: str) -> None:
        self.type_text(*self.NAME_INPUT, name)
        self.type_text(*self.LICENSE_INPUT, license_number)
        self.type_text(*self.EXPIRY_INPUT, expiry)

    def submit_driver(self) -> None:
        """Click save and wait for the modal to close / table to refresh."""
        self.click(*self.SAVE_BUTTON)
        # The frontend may show a JS alert on validation error
        self.dismiss_alert_if_present()
        # Wait for the modal overlay to disappear
        self.wait_invisible(By.XPATH, "//h3[contains(text(),'Register New Driver')]")

    def wait_for_table_data(self) -> None:
        """Wait until at least one data row is present in the table."""
        self.wait.until(EC.presence_of_element_located(self.TABLE_ROWS))

    def get_all_driver_names(self) -> list[str]:
        self.wait_for_table_data()
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        return [r.find_element(By.CSS_SELECTOR, "td:first-child").text for r in rows]

    def get_driver_status(self, name: str) -> str:
        """Return the status badge text for a driver by name."""
        self.wait_for_table_data()
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            if cells[0].text == name:
                return cells[3].text
        raise ValueError(f"Driver '{name}' not found in table")

    def get_table_row_count(self) -> int:
        self.wait_for_table_data()
        return len(self.driver.find_elements(*self.TABLE_ROWS))
