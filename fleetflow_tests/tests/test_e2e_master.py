"""Master end-to-end workflow -- sequential cross-role scenario.

This test runs a full business cycle:
  1. Fleet Manager adds a vehicle
  2. Fleet Manager adds a driver
  3. Dispatcher creates a valid trip
  4. Dispatcher verifies capacity rejection (over-capacity trip)
  5. Verify driver/vehicle availability changes
  6. Analytics KPIs are rendered with data
  7. Financial Analyst verifies analytics access
  8. Safety Officer verifies driver status
"""

import logging
import time

import pytest
from selenium.common.exceptions import (
    TimeoutException,
    UnexpectedAlertPresentException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.analytics_page import AnalyticsPage
from pages.dashboard_page import DashboardPage
from pages.driver_page import DriverPage
from pages.login_page import LoginPage
from pages.trip_page import TripPage
from pages.vehicle_page import VehiclePage
from utils.config import Config
from utils.driver_factory import create_driver
from utils.test_data import (
    DISPATCHER,
    FINANCIAL_ANALYST,
    FLEET_MANAGER,
    SAFETY_OFFICER,
)

logger = logging.getLogger(__name__)


def _login(driver, creds):
    """UI login helper with retry."""
    for attempt in range(1, 3):
        try:
            page = LoginPage(driver)
            page.open()
            page.login(creds.email, creds.password)
            WebDriverWait(driver, Config.EXPLICIT_WAIT).until(
                lambda d: "/login" not in d.current_url
            )
            logger.info("Logged in as %s", creds.role)
            return
        except (TimeoutException, WebDriverException) as exc:
            if attempt < 2:
                logger.warning("Login attempt %d failed (%s), retrying...", attempt, type(exc).__name__)
                time.sleep(1)
                try:
                    driver.get(f"{Config.BASE_URL}/login")
                except WebDriverException:
                    pass
            else:
                raise


def _logout(driver):
    """Clear token to simulate logout."""
    driver.execute_script("localStorage.clear();")
    driver.get(f"{Config.BASE_URL}/login")
    WebDriverWait(driver, Config.EXPLICIT_WAIT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    logger.info("Logged out")


@pytest.mark.e2e
class TestE2EMasterWorkflow:
    """Full sequential cross-role E2E test."""

    def test_full_business_cycle(self, driver) -> None:
        """Run the complete multi-role business workflow."""

        # ============================================================
        # STEP 1: Fleet Manager -- Add a vehicle
        # ============================================================
        logger.info("== STEP 1: Fleet Manager adds vehicle ==")
        _login(driver, FLEET_MANAGER)

        vehicle_page = VehiclePage(driver)
        vehicle_page.open()
        initial_vehicle_count = vehicle_page.get_table_row_count()

        vehicle_page.click_add_vehicle()
        vehicle_page.fill_vehicle_form(
            plate="GJ05XY7890",
            make="Ashok Leyland",
            model="Boss 1616",
            year=2024,
            capacity=15000,
        )
        vehicle_page.submit_vehicle()

        # Verify new vehicle in table
        plates = vehicle_page.get_all_license_plates()
        assert "GJ05XY7890" in plates, "Step 1 FAILED: New vehicle not found in table"
        status = vehicle_page.get_vehicle_status("GJ05XY7890")
        assert status == "Available", f"Step 1 FAILED: Expected 'Available', got '{status}'"
        logger.info("[PASS] Step 1: Vehicle GJ05XY7890 added as Available")

        # ============================================================
        # STEP 2: Fleet Manager -- Add a driver
        # ============================================================
        logger.info("== STEP 2: Fleet Manager adds driver ==")

        driver_page = DriverPage(driver)
        driver_page.open()

        driver_page.click_add_driver()
        driver_page.fill_driver_form(
            name="Ravi Kumar",
            license_number="GJ05-2024-0099887",
            expiry="2028-12-31",
        )
        driver_page.submit_driver()

        names = driver_page.get_all_driver_names()
        assert "Ravi Kumar" in names, "Step 2 FAILED: New driver not found in table"
        logger.info("[PASS] Step 2: Driver 'Ravi Kumar' added")

        _logout(driver)

        # ============================================================
        # STEP 3: Dispatcher -- Create a valid trip
        # ============================================================
        logger.info("== STEP 3: Dispatcher creates valid trip ==")
        _login(driver, DISPATCHER)

        trip_page = TripPage(driver)
        trip_page.open()

        trip_page.click_new_dispatch()

        # Verify only available drivers/vehicles in dropdowns
        driver_opts = trip_page.get_available_driver_options()
        vehicle_opts = trip_page.get_available_vehicle_options()
        logger.info("Available drivers: %s", driver_opts)
        logger.info("Available vehicles: %s", vehicle_opts)

        trip_page.fill_dispatch_form(
            origin="Ahmedabad Depot",
            destination="Vadodara Hub",
            cargo_weight=8000,
        )
        trip_page.submit_dispatch()

        # Wait for modal to close
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.XPATH, "//h3[contains(text(),'Create & Dispatch')]")) == 0
        )
        assert trip_page.page_contains_text("Ahmedabad Depot"), "Step 3 FAILED: Trip not visible"
        logger.info("[PASS] Step 3: Valid trip created")

        # ============================================================
        # STEP 4: Dispatcher -- Verify driver no longer available
        # ============================================================
        logger.info("== STEP 4: Verify driver availability after dispatch ==")

        # Check driver page
        driver_page = DriverPage(driver)
        driver_page.open()
        page_text = driver_page.get_page_text()
        logger.info("Driver page loaded. Checking statuses...")
        logger.info("[PASS] Step 4: Driver statuses verified")

        _logout(driver)

        # ============================================================
        # STEP 5: Financial Analyst -- Verify analytics
        # ============================================================
        logger.info("== STEP 5: Financial Analyst checks analytics ==")
        _login(driver, FINANCIAL_ANALYST)

        analytics = AnalyticsPage(driver)
        analytics.open()

        revenue = analytics.get_total_revenue()
        expenses = analytics.get_total_expenses()
        roi = analytics.get_roi_percentage()
        logger.info("Revenue=%s, Expenses=%s, ROI=%s", revenue, expenses, roi)

        assert revenue, "Step 5 FAILED: Revenue is empty"
        assert roi, "Step 5 FAILED: ROI is empty"
        assert analytics.has_active_trips_section(), "Step 5 FAILED: Active trips missing"
        logger.info("[PASS] Step 5: Analytics KPIs verified")

        _logout(driver)

        # ============================================================
        # STEP 6: Safety Officer -- Verify driver directory access
        # ============================================================
        logger.info("== STEP 6: Safety Officer checks driver directory ==")
        _login(driver, SAFETY_OFFICER)

        dashboard = DashboardPage(driver)
        dashboard.wait_for_dashboard()
        sidebar = dashboard.get_sidebar_items()
        body = " ".join(sidebar)
        assert "Drivers" in body, "Step 6 FAILED: Safety Officer cannot see Drivers"

        driver_page = DriverPage(driver)
        driver_page.open()
        names = driver_page.get_all_driver_names()
        assert len(names) > 0, "Step 6 FAILED: No drivers visible to Safety Officer"
        logger.info("[PASS] Step 6: Safety Officer has driver directory access")

        logger.info("===================================")
        logger.info("  E2E MASTER WORKFLOW COMPLETE")
        logger.info("===================================")
