"""Expense page object."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ExpensePage(BasePage):
    """Page object for /expenses."""

    # -- Locators --
    LOG_EXPENSE_BUTTON = (By.XPATH, "//button[contains(.,'Log Expense')]")
    MODAL_HEADING = (By.XPATH, "//h3[contains(text(),'Log Expense')]")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")
    TOTAL_EXPENSES_CARD = (By.XPATH, "//h3[contains(text(),'Total Expenses')]/following-sibling::p")

    # Modal fields
    DATE_INPUT = (By.XPATH, "//label[contains(text(),'Date')]/following-sibling::input")
    VEHICLE_SELECT = (By.XPATH, "//label[contains(text(),'Select Vehicle')]/following-sibling::select")
    TRIP_SELECT = (By.XPATH, "//label[contains(text(),'Associated Trip')]/following-sibling::select")
    FUEL_LITERS_INPUT = (By.XPATH, "//label[contains(text(),'Fuel Log Amount')]/following-sibling::input")
    FUEL_COST_INPUT = (By.XPATH, "//label[contains(text(),'Fuel Cost')]/following-sibling::input")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Submit Expense')]")

    # -- Actions --

    def open(self) -> "ExpensePage":
        self.navigate("/expenses")
        self.wait_visible(By.XPATH, "//h2[contains(text(),'Expenses')]")
        return self

    def click_log_expense(self) -> None:
        self.click(*self.LOG_EXPENSE_BUTTON)
        self.wait_visible(*self.MODAL_HEADING)

    def fill_expense_form(
        self,
        fuel_liters: float,
        fuel_cost: float,
        vehicle_index: int = 1,
        trip_index: int = 1,
    ) -> None:
        self.select_by_index(*self.VEHICLE_SELECT, vehicle_index)
        # After selecting vehicle, trips are filtered -- wait briefly for option rendering
        self.select_by_index(*self.TRIP_SELECT, trip_index)
        self.type_text(*self.FUEL_LITERS_INPUT, str(fuel_liters))
        self.type_text(*self.FUEL_COST_INPUT, str(fuel_cost))

    def submit_expense(self) -> None:
        """Click submit and wait for modal to close."""
        self.click(*self.SUBMIT_BUTTON)
        self.dismiss_alert_if_present()
        self.wait_invisible(*self.MODAL_HEADING)

    def get_total_expenses_text(self) -> str:
        return self.get_text(*self.TOTAL_EXPENSES_CARD)

    def wait_for_table_data(self) -> None:
        """Wait until at least one data row is present."""
        self.wait.until(EC.presence_of_element_located(self.TABLE_ROWS))

    def get_table_row_count(self) -> int:
        self.wait_for_table_data()
        return len(self.driver.find_elements(*self.TABLE_ROWS))
