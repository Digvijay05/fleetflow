"""Pydantic schemas for Trip endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.trip import TripStatus


class TripCreate(BaseModel):
    vehicle_id: str
    driver_id: str
    origin: str = Field(..., min_length=1, max_length=255)
    destination: str = Field(..., min_length=1, max_length=255)
    cargo_weight: int = Field(..., gt=0)
    distance_km: float | None = Field(default=None, ge=0)
    revenue: float | None = Field(default=None, ge=0)


class TripStatusUpdate(BaseModel):
    status: TripStatus
    odometer_km: int | None = Field(default=None, ge=0, description="Final odometer on completion")


class TripResponse(BaseModel):
    id: str
    vehicle_id: str
    driver_id: str
    origin: str
    destination: str
    cargo_weight: int
    distance_km: float | None
    revenue: float | None
    status: TripStatus
    start_time: datetime | None
    end_time: datetime | None

    model_config = {"from_attributes": True}
