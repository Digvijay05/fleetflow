"""Vehicle ORM model."""

import enum
import uuid

from sqlalchemy import CheckConstraint, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class VehicleStatus(str, enum.Enum):
    """Vehicle lifecycle states (aligned across PRD / TDD / CDB)."""

    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    IN_SHOP = "In Shop"
    RETIRED = "Retired"


class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = (
        CheckConstraint("max_capacity_kg > 0", name="ck_vehicles_positive_capacity"),
        CheckConstraint("odometer_km >= 0", name="ck_vehicles_non_negative_odometer"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    license_plate: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    max_capacity_kg: Mapped[int] = mapped_column(Integer, nullable=False)
    odometer_km: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    acquisition_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[VehicleStatus] = mapped_column(
        Enum(VehicleStatus), nullable=False, default=VehicleStatus.AVAILABLE, index=True
    )

    trips: Mapped[list["Trip"]] = relationship(back_populates="vehicle", lazy="selectin")  # noqa: F821
    maintenance_logs: Mapped[list["MaintenanceLog"]] = relationship(  # noqa: F821
        back_populates="vehicle", lazy="selectin"
    )
    expenses: Mapped[list["Expense"]] = relationship(back_populates="vehicle", lazy="selectin")  # noqa: F821
