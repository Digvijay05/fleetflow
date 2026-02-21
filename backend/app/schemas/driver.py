"""Pydantic schemas for Driver endpoints."""

from datetime import date

from pydantic import BaseModel, Field

from app.models.driver import DriverStatus


class DriverCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    license_number: str = Field(..., min_length=1, max_length=100)
    license_expiry: date
    safety_score: float | None = Field(default=100.00, ge=0, le=100)


class DriverUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    license_expiry: date | None = None
    safety_score: float | None = Field(default=None, ge=0, le=100)
    status: DriverStatus | None = None


class DriverResponse(BaseModel):
    id: str
    name: str
    license_number: str
    license_expiry: date
    safety_score: float | None
    status: DriverStatus

    model_config = {"from_attributes": True}
