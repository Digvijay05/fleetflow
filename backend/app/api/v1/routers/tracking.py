"""Tracking API router — customer-facing shipment tracking."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.trip import Trip
from app.models.user import RoleEnum, User

router = APIRouter(tags=["tracking"])


@router.get("/my-shipments")
async def get_my_shipments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all shipments for the current customer."""
    stmt = (
        select(Trip)
        .where(Trip.customer_id == current_user.id)
        .order_by(Trip.start_time.desc())
    )
    result = await db.execute(stmt)
    trips = result.scalars().all()

    return [
        {
            "tracking_id": t.tracking_id,
            "origin": t.origin,
            "destination": t.destination,
            "status": t.status.value,
            "start_time": t.start_time.isoformat() if t.start_time else None,
        }
        for t in trips
    ]


@router.get("/{tracking_id}")
async def get_tracking_status(
    tracking_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetch shipment status by tracking ID. Customers can only see their own."""
    stmt = (
        select(Trip)
        .options(joinedload(Trip.vehicle), joinedload(Trip.driver))
        .where(Trip.tracking_id == tracking_id)
    )
    result = await db.execute(stmt)
    trip = result.unique().scalar_one_or_none()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tracking ID not found"
        )

    # Customers can only track their own shipments
    if current_user.role_rel.name == RoleEnum.CUSTOMER:
        if trip.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only track your own shipments",
            )

    return {
        "tracking_id": trip.tracking_id,
        "status": trip.status.value,
        "origin": trip.origin,
        "destination": trip.destination,
        "vehicle_plate": trip.vehicle.license_plate if trip.vehicle else "N/A",
        "driver_name": trip.driver.name if trip.driver else "N/A",
        "cargo_weight": trip.cargo_weight,
        "distance_km": float(trip.distance_km) if trip.distance_km else None,
        "start_time": trip.start_time.isoformat() if trip.start_time else None,
        "end_time": trip.end_time.isoformat() if trip.end_time else None,
    }
