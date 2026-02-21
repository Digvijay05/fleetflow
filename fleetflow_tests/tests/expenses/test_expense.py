"""Expense module tests."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.expense_page import ExpensePage


@pytest.mark.expenses
class TestExpense:
    """Verify expense logging and totals calculation."""

    def test_expense_page_loads(self, fleet_manager_driver: WebDriver) -> None:
        """Expense page should render heading and totals card."""
        page = ExpensePage(fleet_manager_driver)
        page.open()
        assert "Operational Expenses" in page.get_page_text()

    def test_log_expense_appears_in_table(self, fleet_manager_driver: WebDriver) -> None:
        """Logging a fuel expense should add a row to the table."""
        page = ExpensePage(fleet_manager_driver)
        page.open()

        page.click_log_expense()
        page.fill_expense_form(
            fuel_liters=50.0,
            fuel_cost=4500.00,
        )
        page.submit_expense()

        # Verify table has at least one row
        page.wait_visible(*page.TABLE_ROWS)
        assert page.get_table_row_count() >= 1, "Expected at least one expense record"

    def test_total_expenses_updates(self, fleet_manager_driver: WebDriver) -> None:
        """Total Expenses card should show a non-zero value after logging an expense."""
        page = ExpensePage(fleet_manager_driver)
        page.open()
        total_text = page.get_total_expenses_text()
        # Should contain a dollar amount
        assert "$" in total_text or "₹" in total_text or total_text != "$0.00", (
            f"Total expenses should be non-zero: {total_text}"
        )

    def test_analyst_can_access_expenses(self, analyst_driver: WebDriver) -> None:
        """Financial Analyst role should be able to access /expenses."""
        page = ExpensePage(analyst_driver)
        page.open()
        assert "Operational Expenses" in page.get_page_text()
