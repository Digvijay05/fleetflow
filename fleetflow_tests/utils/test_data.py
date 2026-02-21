"""Deterministic Indian-context test data for FleetFlow E2E tests."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Credentials:
    email: str
    password: str
    role: str


# Seed accounts — must match scripts/seed.py
FLEET_MANAGER = Credentials("admin@fleetflow.com", "admin123", "Fleet Manager")
DISPATCHER = Credentials("dispatcher@fleetflow.com", "dispatch123", "Dispatcher")
SAFETY_OFFICER = Credentials("safety@fleetflow.com", "safety123", "Safety Officer")
FINANCIAL_ANALYST = Credentials("analyst@fleetflow.com", "analyst123", "Financial Analyst")
CUSTOMER = Credentials("customer@fleetflow.com", "customer123", "Customer")

# Invalid credentials for negative testing
INVALID_USER = Credentials("nobody@fleetflow.com", "wrong", "")
WRONG_PASSWORD = Credentials("admin@fleetflow.com", "wrongpassword", "")


# ── Vehicle test data ──
NEW_VEHICLE = {
    "license_plate": "RJ14TC9876",
    "make": "Tata",
    "model": "Ultra T.7",
    "year": 2024,
    "max_capacity_kg": 7000,
}

# ── Driver test data ──
NEW_DRIVER = {
    "name": "Arjun Mehta",
    "license_number": "RJ14-2023-0056789",
    "license_expiry": "2027-06-15",
}

# ── Trip test data ──
VALID_TRIP = {
    "origin": "Jaipur Depot",
    "destination": "Udaipur Hub",
    "cargo_weight": 5000,
}

OVERCAPACITY_TRIP = {
    "origin": "Jaipur Depot",
    "destination": "Udaipur Hub",
    "cargo_weight": 99999,  # exceeds any vehicle
}

# ── Maintenance test data ──
NEW_MAINTENANCE = {
    "type": "Oil Change",
    "description": "Routine oil change and filter replacement",
    "cost": 8500.00,
}

# ── Expense test data ──
NEW_EXPENSE = {
    "fuel_liters": 75.0,
    "fuel_cost": 6900.00,
}

# ── Sidebar items per role ──
SIDEBAR_ITEMS_BY_ROLE = {
    "Fleet Manager": ["Dashboard", "Vehicles", "Trips", "Drivers", "Maintenance", "Expenses", "Analytics", "Tracking"],
    "Dispatcher": ["Dashboard", "Vehicles", "Trips", "Drivers", "Maintenance", "Tracking"],
    "Safety Officer": ["Dashboard", "Vehicles", "Trips", "Drivers", "Maintenance", "Tracking"],
    "Financial Analyst": ["Dashboard", "Vehicles", "Trips", "Drivers", "Maintenance", "Expenses", "Analytics", "Tracking"],
    "Customer": ["Track Shipment"],
}
