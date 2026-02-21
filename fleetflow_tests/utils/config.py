"""Test framework configuration — all tunables in one place."""

import os


class Config:
    """Centralised test configuration, overridable via environment variables."""

    BASE_URL: str = os.getenv("FLEETFLOW_BASE_URL", "http://localhost")
    API_URL: str = os.getenv("FLEETFLOW_API_URL", "http://localhost:8001/api/v1")

    BROWSER: str = os.getenv("BROWSER", "chrome")
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    RECORD_VIDEO: bool = os.getenv("RECORD_VIDEO", "false").lower() == "true"

    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "5"))
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    SCREENSHOT_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
    VIDEO_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "videos")
    LOG_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "logs")

    WINDOW_WIDTH: int = 1920
    WINDOW_HEIGHT: int = 1080

    VIDEO_FPS: int = 10
