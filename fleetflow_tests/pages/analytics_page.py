"""Analytics page object."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.config import Config


class AnalyticsPage(BasePage):
    """Page object for /analytics -- KPI cards & efficiency metrics."""

    # -- Locators --
    PAGE_HEADING = (By.XPATH, "//h2[contains(text(),'Financial Analytics')]")
    LOADING_SPINNER = (By.CSS_SELECTOR, ".animate-spin")

    # KPI card values -- match by title text then sibling <p>
    TOTAL_REVENUE = (By.XPATH, "//h3[contains(text(),'Total Revenue')]/following-sibling::p")
    TOTAL_EXPENSES = (By.XPATH, "//h3[contains(text(),'Total Expenses')]/following-sibling::p")
    NET_PROFIT = (By.XPATH, "//h3[contains(text(),'Net Profit')]/following-sibling::p")
    ROI_PERCENTAGE = (By.XPATH, "//h3[contains(text(),'ROI')]/following-sibling::p")

    # Efficiency metrics
    COST_PER_KM = (By.XPATH, "//h3[contains(text(),'Cost per Km')]/following-sibling::p[1]")
    FUEL_EFFICIENCY = (By.XPATH, "//h3[contains(text(),'Fuel Efficiency')]/following-sibling::p[1]")
    FUEL_COST = (By.XPATH, "//h3[contains(text(),'Fuel Cost')]/following-sibling::p[1]")

    # Active trips section
    ACTIVE_TRIPS_HEADING = (By.XPATH, "//h3[contains(text(),'Active Trips')]")

    # -- Actions --

    def open(self) -> "AnalyticsPage":
        self.navigate("/analytics")
        # The page shows a spinner while fetching data; wait for it to vanish
        # then check for either the heading or an error banner.
        extended_wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT + 10)
        try:
            extended_wait.until(EC.visibility_of_element_located(self.PAGE_HEADING))
        except Exception:
            # May have loaded already, or an error appeared -- re-check
            pass
        return self

    def get_total_revenue(self) -> str:
        return self.get_text(*self.TOTAL_REVENUE)

    def get_total_expenses(self) -> str:
        return self.get_text(*self.TOTAL_EXPENSES)

    def get_net_profit(self) -> str:
        return self.get_text(*self.NET_PROFIT)

    def get_roi_percentage(self) -> str:
        return self.get_text(*self.ROI_PERCENTAGE)

    def get_cost_per_km(self) -> str:
        return self.get_text(*self.COST_PER_KM)

    def get_fuel_efficiency(self) -> str:
        return self.get_text(*self.FUEL_EFFICIENCY)

    def get_fuel_cost(self) -> str:
        return self.get_text(*self.FUEL_COST)

    def has_active_trips_section(self) -> bool:
        return self.is_element_present(*self.ACTIVE_TRIPS_HEADING)
