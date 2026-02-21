# FleetFlow Selenium E2E Test Suite

Comprehensive Selenium-based end-to-end test automation for the FleetFlow fleet management application.

## Architecture

```
fleetflow_tests/
├── conftest.py           # WebDriver lifecycle, login fixtures, video hooks
├── pytest.ini            # Markers and reporting config
├── requirements.txt      # Pinned dependencies
├── pages/                # Page Object Model (POM)
│   ├── base_page.py      # Shared WebDriverWait helpers
│   ├── login_page.py     # Authentication
│   ├── dashboard_page.py # Sidebar, header
│   ├── vehicle_page.py   # Vehicle CRUD
│   ├── driver_page.py    # Driver CRUD
│   ├── trip_page.py      # Trip dispatch lifecycle
│   ├── maintenance_page.py
│   ├── expense_page.py
│   └── analytics_page.py
├── utils/
│   ├── config.py         # Centralised configuration
│   ├── test_data.py      # Deterministic Indian-context data
│   ├── driver_factory.py # Chrome/Firefox WebDriver factory
│   ├── video_recorder.py # mss + OpenCV screen recorder
│   └── assertions.py     # Custom assertion helpers
├── tests/
│   ├── auth/             # Login & RBAC tests
│   ├── vehicles/         # Vehicle CRUD tests
│   ├── drivers/          # Driver CRUD tests
│   ├── trips/            # Trip dispatch lifecycle tests
│   ├── maintenance/      # Maintenance module tests
│   ├── expenses/         # Expense module tests
│   ├── analytics/        # Analytics KPI tests
│   └── test_e2e_master.py # Full cross-role E2E workflow
└── reports/              # Generated at runtime
    ├── report.html       # pytest-html report
    ├── screenshots/      # Failure screenshots
    ├── videos/           # Screen recordings
    └── logs/             # Structured test logs
```

## Prerequisites

- **Python 3.11+**
- **Chrome** or **Firefox** browser installed
- **ChromeDriver** / **GeckoDriver** matching your browser version
- **FleetFlow running** at `http://localhost` (frontend) and `http://localhost:8001` (API)

## Setup

```bash
cd fleetflow_tests

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with video recording
```bash
pytest --record-video
```

### Run specific module
```bash
pytest tests/auth/ -m auth
pytest tests/trips/ -m trips
pytest tests/analytics/ -m analytics
```

### Run E2E master workflow only
```bash
pytest tests/test_e2e_master.py -m e2e
```

### Run headless
```bash
pytest --headless=true
```

### Run with Firefox
```bash
pytest --browser=firefox
```

### Override base URL
```bash
pytest --base-url=http://staging.fleetflow.com
```

## Test Coverage

| Module | Tests | Roles Tested |
|--------|-------|-------------|
| Auth | 6 | FM, Dispatcher, Customer |
| RBAC | 4 | FM, Dispatcher, Customer |
| Vehicles | 3 | Fleet Manager |
| Drivers | 4 | Fleet Manager |
| Trips | 4 | Dispatcher |
| Maintenance | 3 | Fleet Manager |
| Expenses | 4 | FM, Financial Analyst |
| Analytics | 6 | FM, Financial Analyst |
| E2E Master | 1 (6 steps) | All 4 management roles |
| **Total** | **35** | |

## Reports

After running, reports are generated in `reports/`:

- **`report.html`** — Interactive pass/fail summary with failure screenshots
- **`screenshots/`** — Automatic screenshots on test failure
- **`videos/test_run_<timestamp>.mp4`** — Full screen recording (when `--record-video` is used)
- **`logs/test_<timestamp>.log`** — Structured log file

## Design Principles

- **Zero `time.sleep()`** — All waits use `WebDriverWait` with explicit conditions
- **Page Object Model** — Clean separation of locators and test logic
- **Deterministic data** — Indian-context test data with pinned values
- **Structured logging** — Every major step logged with timestamps
- **Failure resilience** — Screenshot capture on any test failure
