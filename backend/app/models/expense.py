"""Expense (fuel log) ORM model."""

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vehicle_id: Mapped[str] = mapped_column(ForeignKey("vehicles.id", ondelete="RESTRICT"), nullable=False, index=True)
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True)
    fuel_liters: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    fuel_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    vehicle: Mapped["Vehicle"] = relationship(back_populates="expenses", lazy="selectin")  # noqa: F821
    trip: Mapped["Trip"] = relationship(back_populates="expenses", lazy="selectin")  # noqa: F821
