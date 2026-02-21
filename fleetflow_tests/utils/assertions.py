"""Custom assertion helpers for FleetFlow Selenium tests."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


def assert_text_present(driver: WebDriver, text: str) -> None:
    """Assert that *text* appears somewhere in the page body."""
    body = driver.find_element(By.TAG_NAME, "body").text
    assert text in body, f"Expected text '{text}' not found on page. Page text excerpt: {body[:300]}"
    logger.info("[PASS] Text present: '%s'", text)


def assert_text_absent(driver: WebDriver, text: str) -> None:
    """Assert that *text* does NOT appear in the page body."""
    body = driver.find_element(By.TAG_NAME, "body").text
    assert text not in body, f"Unexpected text '{text}' found on page."
    logger.info("[PASS] Text absent: '%s'", text)


def assert_current_url_contains(driver: WebDriver, fragment: str) -> None:
    """Assert current URL contains *fragment*."""
    url = driver.current_url
    assert fragment in url, f"Expected URL to contain '{fragment}', got '{url}'"
    logger.info("[PASS] URL contains '%s'", fragment)


def assert_element_count(driver: WebDriver, css: str, expected: int) -> None:
    """Assert that *css* matches exactly *expected* elements."""
    elems = driver.find_elements(By.CSS_SELECTOR, css)
    actual = len(elems)
    assert actual == expected, f"Expected {expected} elements for '{css}', found {actual}"
    logger.info("[PASS] Element count '%s' == %d", css, expected)
