"""Maintenance page object."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class MaintenancePage(BasePage):
    """Page object for /maintenance."""

    # -- Locators --
    LOG_SERVICE_BUTTON = (By.XPATH, "//button[contains(.,'Log Service')]")
    MODAL_HEADING = (By.XPATH, "//h3[contains(text(),'Log Maintenance')]")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")

    # Modal fields
    VEHICLE_SELECT = (By.XPATH, "//label[contains(text(),'Select Vehicle')]/following-sibling::select")
    TYPE_SELECT = (By.XPATH, "//label[contains(text(),'Maintenance Type')]/following-sibling::select")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea")
    COST_INPUT = (By.XPATH, "//label[contains(text(),'Estimated Cost')]/following-sibling::input")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Submit Log')]")

    COMPLETE_BUTTONS = (By.XPATH, "//button[contains(.,'Complete')]")

    # -- Actions --

    def open(self) -> "MaintenancePage":
        self.navigate("/maintenance")
        self.wait_visible(By.XPATH, "//h2[contains(text(),'Maintenance')]")
        return self

    def click_log_service(self) -> None:
        self.click(*self.LOG_SERVICE_BUTTON)
        self.wait_visible(*self.MODAL_HEADING)

    def fill_maintenance_form(self, maint_type: str, description: str, cost: float, vehicle_index: int = 1) -> None:
        self.select_by_index(*self.VEHICLE_SELECT, vehicle_index)
        self.select_by_visible_text(*self.TYPE_SELECT, maint_type)
        self.type_text(*self.DESCRIPTION_INPUT, description)
        self.type_text(*self.COST_INPUT, str(cost))

    def submit_log(self) -> None:
        """Click submit and wait for modal to close."""
        self.click(*self.SUBMIT_BUTTON)
        self.dismiss_alert_if_present()
        self.wait_invisible(*self.MODAL_HEADING)

    def complete_first_log(self) -> None:
        """Click the first 'Complete' button in the table."""
        self.click(*self.COMPLETE_BUTTONS)

    def wait_for_table_data(self) -> None:
        """Wait until at least one data row is present."""
        self.wait.until(EC.presence_of_element_located(self.TABLE_ROWS))

    def get_table_row_count(self) -> int:
        self.wait_for_table_data()
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def get_first_row_status(self) -> str:
        self.wait_for_table_data()
        row = self.wait_visible(*self.TABLE_ROWS)
        cells = row.find_elements(By.CSS_SELECTOR, "td")
        return cells[4].text
