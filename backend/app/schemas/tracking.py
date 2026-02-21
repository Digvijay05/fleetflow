"""Pydantic schemas for Tracking endpoints."""

from pydantic import BaseModel


class TrackingResponse(BaseModel):
    tracking_id: str
    status: str
    origin: str
    destination: str
    vehicle_plate: str
    driver_name: str
    cargo_weight: int
    distance_km: float | None
    start_time: str | None
    end_time: str | None

    model_config = {"from_attributes": True}
