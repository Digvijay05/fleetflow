"""Test the analytics endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_analytics_dashboard_unauthorized(client: AsyncClient):
    """Test that unauthorized users are blocked from analytics."""
    response = await client.get("/api/v1/analytics/dashboard")
    assert response.status_code == 403


# Note: Further tests require authenticated user mocks depending on how the
# dependencies are overridden in conftest.py
