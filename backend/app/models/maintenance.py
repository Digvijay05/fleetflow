"""MaintenanceLog ORM model."""

import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class MaintenanceType(str, enum.Enum):
    PREVENTATIVE = "Preventative"
    REACTIVE = "Reactive"


class MaintenanceStatus(str, enum.Enum):
    OPEN = "Open"
    COMPLETED = "Completed"


class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vehicle_id: Mapped[str] = mapped_column(ForeignKey("vehicles.id", ondelete="RESTRICT"), nullable=False, index=True)
    type: Mapped[MaintenanceType] = mapped_column(Enum(MaintenanceType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    odometer_km: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[MaintenanceStatus] = mapped_column(
        Enum(MaintenanceStatus), nullable=False, default=MaintenanceStatus.OPEN
    )

    vehicle: Mapped["Vehicle"] = relationship(back_populates="maintenance_logs", lazy="selectin")  # noqa: F821
