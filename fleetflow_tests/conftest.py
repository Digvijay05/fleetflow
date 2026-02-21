"""Pytest configuration -- fixtures, hooks, and video recording lifecycle."""

from __future__ import annotations

import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Generator

import pytest
from selenium.common.exceptions import (
    InvalidSessionIdException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver

# Ensure project root is on sys.path so `from pages.*` / `from utils.*` resolve
sys.path.insert(0, os.path.dirname(__file__))

from pages.login_page import LoginPage
from utils.config import Config
from utils.driver_factory import create_driver
from utils.test_data import (
    CUSTOMER,
    DISPATCHER,
    FINANCIAL_ANALYST,
    FLEET_MANAGER,
    SAFETY_OFFICER,
    Credentials,
)
from utils.video_recorder import VideoRecorder

# -- Logging --
LOG_DIR = Path(Config.LOG_DIR)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            LOG_DIR / f"test_{datetime.now():%Y%m%d_%H%M%S}.log",
            encoding="utf-8",
        ),
    ],
)
logger = logging.getLogger("conftest")

# -- Ensure report directories --
Path(Config.SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)
Path(Config.VIDEO_DIR).mkdir(parents=True, exist_ok=True)


# -- CLI options --
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", default="chrome", help="Browser: chrome or firefox")
    parser.addoption("--headless", default="false", help="Run headless: true/false")
    parser.addoption("--record-video", action="store_true", default=False, help="Record screen video")
    parser.addoption("--base-url", default=None, help="Override BASE_URL")


def pytest_configure(config: pytest.Config) -> None:
    """Apply CLI overrides to Config singleton."""
    if config.getoption("--browser"):
        Config.BROWSER = config.getoption("--browser")
    if config.getoption("--headless").lower() == "true":
        Config.HEADLESS = True
    if config.getoption("--record-video"):
        Config.RECORD_VIDEO = True
    if config.getoption("--base-url"):
        Config.BASE_URL = config.getoption("--base-url")


# -- Session-scoped video recorder --
_recorder: VideoRecorder | None = None


def pytest_sessionstart(session: pytest.Session) -> None:
    global _recorder
    if Config.RECORD_VIDEO:
        _recorder = VideoRecorder()
        path = _recorder.start()
        logger.info("Session video recording -> %s", path)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    global _recorder
    if _recorder is not None:
        path = _recorder.stop()
        logger.info("Session video saved -> %s", path)
        _recorder = None


# -- WebDriver fixture --
@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    """Provide a fresh WebDriver instance per test function."""
    drv = create_driver()
    yield drv
    try:
        drv.quit()
    except (InvalidSessionIdException, WebDriverException):
        pass  # browser already closed


# -- Login helpers --
_MAX_LOGIN_RETRIES = 2


def _login(driver: WebDriver, creds: Credentials) -> None:
    """Login via the UI and wait for redirect away from /login.

    Retries once if the redirect does not happen within the wait timeout
    (guards against intermittent slow logins or stale sessions).
    """
    from selenium.webdriver.support.ui import WebDriverWait

    for attempt in range(1, _MAX_LOGIN_RETRIES + 1):
        try:
            page = LoginPage(driver)
            page.open()
            page.login(creds.email, creds.password)
            # Wait for redirect away from /login
            WebDriverWait(driver, Config.EXPLICIT_WAIT).until(
                lambda d: "/login" not in d.current_url
            )
            logger.info("Logged in as %s (%s)", creds.email, creds.role)
            return
        except (TimeoutException, InvalidSessionIdException, WebDriverException) as exc:
            if attempt < _MAX_LOGIN_RETRIES:
                logger.warning(
                    "Login attempt %d failed (%s), retrying...", attempt, type(exc).__name__
                )
                time.sleep(1)
                # Refresh the page and try again
                try:
                    driver.get(f"{Config.BASE_URL}/login")
                except WebDriverException:
                    pass
            else:
                raise


@pytest.fixture
def fleet_manager_driver(driver: WebDriver) -> WebDriver:
    """Driver logged in as Fleet Manager."""
    _login(driver, FLEET_MANAGER)
    return driver


@pytest.fixture
def dispatcher_driver(driver: WebDriver) -> WebDriver:
    """Driver logged in as Dispatcher."""
    _login(driver, DISPATCHER)
    return driver


@pytest.fixture
def safety_officer_driver(driver: WebDriver) -> WebDriver:
    """Driver logged in as Safety Officer."""
    _login(driver, SAFETY_OFFICER)
    return driver


@pytest.fixture
def analyst_driver(driver: WebDriver) -> WebDriver:
    """Driver logged in as Financial Analyst."""
    _login(driver, FINANCIAL_ANALYST)
    return driver


@pytest.fixture
def customer_driver(driver: WebDriver) -> WebDriver:
    """Driver logged in as Customer."""
    _login(driver, CUSTOMER)
    return driver


# -- Screenshot on failure --
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:
    """Capture a screenshot when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when in ("call", "setup") and report.failed:
        drv: WebDriver | None = (
            item.funcargs.get("driver")
            or item.funcargs.get("fleet_manager_driver")
            or item.funcargs.get("dispatcher_driver")
            or item.funcargs.get("analyst_driver")
            or item.funcargs.get("customer_driver")
            or item.funcargs.get("safety_officer_driver")
        )
        if drv is not None:
            try:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(Config.SCREENSHOT_DIR, f"{item.name}_{ts}.png")
                drv.save_screenshot(path)
                logger.info("Failure screenshot -> %s", path)
                # Attach to pytest-html report
                if hasattr(report, "extra"):
                    from pytest_html import extras
                    report.extra = getattr(report, "extra", [])
                    report.extra.append(extras.image(path))
            except (InvalidSessionIdException, WebDriverException):
                logger.warning("Could not capture screenshot (session dead)")
