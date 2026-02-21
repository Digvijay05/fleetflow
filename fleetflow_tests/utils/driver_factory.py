"""WebDriver factory — browser instantiation with configurable options."""

import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from utils.config import Config

logger = logging.getLogger(__name__)


def create_driver() -> webdriver.Remote:
    """Create and return a configured WebDriver instance."""
    browser = Config.BROWSER.lower()
    logger.info("Creating %s driver (headless=%s)", browser, Config.HEADLESS)

    if browser == "chrome":
        opts = ChromeOptions()
        if Config.HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")
        opts.add_argument("--disable-extensions")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=opts)

    elif browser == "firefox":
        opts = FirefoxOptions()
        if Config.HEADLESS:
            opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)
        driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

    else:
        raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'.")

    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    logger.info("WebDriver ready: %s", driver.capabilities.get("browserName", browser))
    return driver
