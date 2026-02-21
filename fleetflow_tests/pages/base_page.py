"""Base page object -- shared WebDriverWait helpers for all page objects."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from utils.config import Config

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


class BasePage:
    """Shared browser interactions -- explicit waits everywhere, no sleep."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    # -- Navigation --

    def navigate(self, path: str) -> None:
        """Navigate to *path* relative to BASE_URL."""
        url = f"{Config.BASE_URL}{path}"
        logger.info("Navigating to %s", url)
        self.driver.get(url)

    def current_url(self) -> str:
        return self.driver.current_url

    # -- Alert handling --

    def dismiss_alert_if_present(self) -> str | None:
        """Accept any pending JS alert and return its text, or None."""
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            logger.info("Dismissed alert: %s", text)
            return text
        except NoAlertPresentException:
            return None

    # -- Waits & Finds --

    def wait_visible(self, by: str, value: str) -> WebElement:
        """Wait until an element is visible and return it."""
        try:
            return self.wait.until(EC.visibility_of_element_located((by, value)))
        except UnexpectedAlertPresentException:
            self.dismiss_alert_if_present()
            return self.wait.until(EC.visibility_of_element_located((by, value)))

    def wait_clickable(self, by: str, value: str) -> WebElement:
        """Wait until an element is clickable and return it."""
        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def wait_present(self, by: str, value: str) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def wait_text_present(self, by: str, value: str, text: str) -> bool:
        return self.wait.until(EC.text_to_be_present_in_element((by, value), text))

    def wait_url_contains(self, fragment: str) -> bool:
        return self.wait.until(EC.url_contains(fragment))

    def wait_invisible(self, by: str, value: str) -> bool:
        """Wait until an element is no longer visible."""
        return self.wait.until(EC.invisibility_of_element_located((by, value)))

    # -- Interactions --

    def click(self, by: str, value: str) -> None:
        """Wait for element to be clickable, then click."""
        elem = self.wait_clickable(by, value)
        logger.info("Clicking (%s=%s)", by, value)
        elem.click()

    def type_text(self, by: str, value: str, text: str) -> None:
        """Clear and type into an input."""
        elem = self.wait_visible(by, value)
        elem.clear()
        elem.send_keys(text)
        logger.info("Typed '%s' into (%s=%s)", text, by, value)

    def select_by_visible_text(self, by: str, value: str, text: str) -> None:
        """Select a <select> option by visible text."""
        elem = self.wait_visible(by, value)
        Select(elem).select_by_visible_text(text)
        logger.info("Selected '%s' from (%s=%s)", text, by, value)

    def select_by_index(self, by: str, value: str, index: int) -> None:
        """Select a <select> option by index."""
        elem = self.wait_visible(by, value)
        Select(elem).select_by_index(index)
        logger.info("Selected index %d from (%s=%s)", index, by, value)

    def get_text(self, by: str, value: str) -> str:
        """Return the text content of an element."""
        return self.wait_visible(by, value).text

    def get_texts(self, by: str, value: str) -> list[str]:
        """Return text content of all matching elements."""
        self.wait_visible(by, value)
        elems = self.driver.find_elements(by, value)
        return [e.text for e in elems]

    def is_element_present(self, by: str, value: str) -> bool:
        """Check if at least one matching element exists (no wait)."""
        return len(self.driver.find_elements(by, value)) > 0

    def get_page_text(self) -> str:
        """Return the full body text of the page."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_alert_text(self) -> str:
        """Wait for and return browser alert text, then accept it."""
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        logger.info("Alert captured: %s", text)
        return text
