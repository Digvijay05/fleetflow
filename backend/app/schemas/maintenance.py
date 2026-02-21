"""Maintenance Pydantic schemas."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.maintenance import MaintenanceStatus, MaintenanceType


class MaintenanceLogBase(BaseModel):
    vehicle_id: str
    type: MaintenanceType
    description: Optional[str] = None
    cost: float = Field(ge=0.0)
    date: date
    odometer_km: Optional[int] = Field(None, ge=0)


class MaintenanceLogCreate(MaintenanceLogBase):
    pass


class MaintenanceLogUpdate(BaseModel):
    status: MaintenanceStatus


class MaintenanceLogResponse(MaintenanceLogBase):
    id: str
    status: MaintenanceStatus

    model_config = ConfigDict(from_attributes=True)
