"""Driver ORM model."""

import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class DriverStatus(str, enum.Enum):
    """Driver lifecycle states (aligned across PRD / TDD / CDB)."""

    ON_DUTY = "On Duty"
    OFF_DUTY = "Off Duty"
    SUSPENDED = "Suspended"
    ON_TRIP = "On Trip"


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    license_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    license_expiry: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    safety_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True, default=100.00)
    status: Mapped[DriverStatus] = mapped_column(
        Enum(DriverStatus), nullable=False, default=DriverStatus.OFF_DUTY, index=True
    )

    trips: Mapped[list["Trip"]] = relationship(back_populates="driver", lazy="selectin")  # noqa: F821
