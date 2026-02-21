"""Pydantic schemas for Vehicle endpoints."""

from pydantic import BaseModel, Field

from app.models.vehicle import VehicleStatus


class VehicleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    model: str = Field(..., min_length=1, max_length=255)
    license_plate: str = Field(..., min_length=1, max_length=50)
    max_capacity_kg: int = Field(..., gt=0)
    odometer_km: int = Field(default=0, ge=0)
    acquisition_cost: float = Field(..., gt=0)


class VehicleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    model: str | None = Field(default=None, min_length=1, max_length=255)
    odometer_km: int | None = Field(default=None, ge=0)
    status: VehicleStatus | None = None


class VehicleResponse(BaseModel):
    id: str
    name: str
    model: str
    license_plate: str
    max_capacity_kg: int
    odometer_km: int
    acquisition_cost: float
    status: VehicleStatus

    model_config = {"from_attributes": True}
