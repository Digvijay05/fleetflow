"""Expense Pydantic schemas."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    vehicle_id: str
    trip_id: str
    fuel_liters: float = Field(gt=0.0)
    fuel_cost: float = Field(gt=0.0)
    date: date


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
