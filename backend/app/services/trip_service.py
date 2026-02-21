"""Trip dispatching service — core business logic and state machine."""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.driver import Driver, DriverStatus
from app.models.trip import Trip, TripStatus
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.trip import TripCreate, TripStatusUpdate


class TripService:
    """Orchestrates trip creation, dispatch validation, and lifecycle transitions."""

    @staticmethod
    async def dispatch_trip(db: AsyncSession, trip_in: TripCreate) -> Trip:
        """Create and dispatch a trip after full business-rule validation.

        Validation rules (PRD §4, Page 4):
          - Vehicle.status == Available
          - Driver.status == On Duty
          - Driver.license not expired
          - cargo_weight <= vehicle.max_capacity_kg

        On success:
          - Trip.status → Dispatched
          - Vehicle.status → On Trip
          - Driver.status → On Trip

        Raises:
            ValueError: On any validation failure.
        """
        # --- Lock vehicle and driver rows to prevent concurrent dispatch ---
        vehicle = await db.get(Vehicle, trip_in.vehicle_id, with_for_update=True)
        if vehicle is None:
            raise ValueError("Vehicle not found")
        if vehicle.status != VehicleStatus.AVAILABLE:
            raise ValueError(f"Vehicle is not available (current: {vehicle.status.value})")
        if trip_in.cargo_weight > vehicle.max_capacity_kg:
            raise ValueError("Cargo exceeds vehicle capacity")

        driver = await db.get(Driver, trip_in.driver_id, with_for_update=True)
        if driver is None:
            raise ValueError("Driver not found")
        if driver.status != DriverStatus.ON_DUTY:
            raise ValueError(f"Driver is not on duty (current: {driver.status.value})")
        if driver.license_expiry < datetime.now(timezone.utc).date():
            raise ValueError("Driver license has expired")

        # --- Create trip ---
        trip = Trip(
            vehicle_id=trip_in.vehicle_id,
            driver_id=trip_in.driver_id,
            origin=trip_in.origin,
            destination=trip_in.destination,
            cargo_weight=trip_in.cargo_weight,
            distance_km=trip_in.distance_km,
            revenue=trip_in.revenue,
            status=TripStatus.DISPATCHED,
            start_time=datetime.now(timezone.utc),
        )
        db.add(trip)

        # --- Transition states ---
        vehicle.status = VehicleStatus.ON_TRIP
        driver.status = DriverStatus.ON_TRIP

        await db.commit()
        await db.refresh(trip)
        return trip

    @staticmethod
    async def update_trip_status(db: AsyncSession, trip_id: str, payload: TripStatusUpdate) -> Trip:
        """Progress a trip through its lifecycle.

        Valid transitions:
          - Draft → Dispatched (handled by dispatch_trip)
          - Dispatched → Completed
          - Draft → Cancelled

        On completion:
          - Vehicle.status → Available
          - Driver.status → On Duty
          - Update final odometer if provided

        Raises:
            ValueError: On invalid transition.
        """
        trip = await db.get(Trip, trip_id, with_for_update=True)
        if trip is None:
            raise ValueError("Trip not found")

        target = payload.status

        # --- Validate transition ---
        valid_transitions: dict[TripStatus, list[TripStatus]] = {
            TripStatus.DRAFT: [TripStatus.DISPATCHED, TripStatus.CANCELLED],
            TripStatus.DISPATCHED: [TripStatus.IN_TRANSIT, TripStatus.COMPLETED, TripStatus.CANCELLED],
            TripStatus.IN_TRANSIT: [TripStatus.OUT_FOR_DELIVERY, TripStatus.COMPLETED, TripStatus.CANCELLED],
            TripStatus.OUT_FOR_DELIVERY: [TripStatus.DELIVERED, TripStatus.COMPLETED, TripStatus.CANCELLED],
            TripStatus.DELIVERED: [TripStatus.COMPLETED],
        }
        allowed = valid_transitions.get(trip.status, [])
        if target not in allowed:
            raise ValueError(f"Cannot transition from {trip.status.value} to {target.value}")

        trip.status = target

        # Release vehicle and driver on terminal completion states
        if target in (TripStatus.COMPLETED, TripStatus.DELIVERED, TripStatus.CANCELLED):
            trip.end_time = datetime.now(timezone.utc)

            vehicle = await db.get(Vehicle, trip.vehicle_id, with_for_update=True)
            driver = await db.get(Driver, trip.driver_id, with_for_update=True)

            if vehicle:
                vehicle.status = VehicleStatus.AVAILABLE
                if payload.odometer_km is not None:
                    vehicle.odometer_km = payload.odometer_km
            if driver:
                driver.status = DriverStatus.ON_DUTY

        await db.commit()
        await db.refresh(trip)
        return trip

    @staticmethod
    async def list_trips(db: AsyncSession) -> list[Trip]:
        """Return all trips."""
        result = await db.execute(select(Trip))
        return list(result.scalars().all())
