"""Test the maintenance endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_maintenance_log_unauthorized(client: AsyncClient):
    """Test that unauthorized users are blocked from creating maintenance logs."""
    response = await client.post(
        "/api/v1/maintenance/",
        json={
            "vehicle_id": "test-vehicle-id",
            "type": "Preventative",
            "cost": 150.0,
            "date": "2023-10-27"
        },
    )
    assert response.status_code == 403
