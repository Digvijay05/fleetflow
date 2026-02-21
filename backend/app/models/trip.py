"""Trip ORM model."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class TripStatus(str, enum.Enum):
    """Trip lifecycle states (aligned across PRD / TDD / CDB)."""

    DRAFT = "Draft"
    DISPATCHED = "Dispatched"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Trip(Base):
    __tablename__ = "trips"
    __table_args__ = (
        CheckConstraint("cargo_weight > 0", name="ck_trips_positive_cargo"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vehicle_id: Mapped[str] = mapped_column(ForeignKey("vehicles.id"), nullable=False, index=True)
    driver_id: Mapped[str] = mapped_column(ForeignKey("drivers.id"), nullable=False, index=True)
    origin: Mapped[str] = mapped_column(String(255), nullable=False)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo_weight: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_km: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    revenue: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[TripStatus] = mapped_column(
        Enum(TripStatus), nullable=False, default=TripStatus.DRAFT, index=True
    )
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    vehicle: Mapped["Vehicle"] = relationship(back_populates="trips", lazy="selectin")  # noqa: F821
    driver: Mapped["Driver"] = relationship(back_populates="trips", lazy="selectin")  # noqa: F821
    expenses: Mapped[list["Expense"]] = relationship(back_populates="trip", lazy="selectin")  # noqa: F821
