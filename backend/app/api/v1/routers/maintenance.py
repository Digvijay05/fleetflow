"""Maintenance API router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import require_role
from app.db.session import get_db
from app.models.maintenance import MaintenanceLog, MaintenanceStatus
from app.models.user import RoleEnum, User
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.maintenance import MaintenanceLogCreate, MaintenanceLogResponse, MaintenanceLogUpdate

router = APIRouter(tags=["maintenance"])

@router.get("/", response_model=list[MaintenanceLogResponse])
async def list_maintenance_logs(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER, RoleEnum.FINANCIAL_ANALYST)),
):
    """List all maintenance logs."""
    result = await db.execute(select(MaintenanceLog))
    return list(result.scalars().all())


@router.post("/", response_model=MaintenanceLogResponse, status_code=status.HTTP_201_CREATED)
async def create_maintenance_log(
    body: MaintenanceLogCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER)),
):
    """Create a new maintenance log and set Vehicle status to 'In Shop' (Fleet Manager only)."""
    # Verify vehicle exists and is NOT on an active trip or retired.
    # To put a vehicle in shop, it should usually be Available (or at least not On Trip).
    vehicle = await db.get(Vehicle, body.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    if vehicle.status in [VehicleStatus.ON_TRIP, VehicleStatus.RETIRED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot put vehicle in shop while it is {vehicle.status.value}",
        )

    # Change vehicle status
    vehicle.status = VehicleStatus.IN_SHOP

    # Create log
    log = MaintenanceLog(**body.model_dump())
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.patch("/{log_id}", response_model=MaintenanceLogResponse)
async def complete_maintenance_log(
    log_id: str,
    body: MaintenanceLogUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER)),
):
    """Update a maintenance log status. Completing it sets Vehicle back to 'Available'."""
    log = await db.get(MaintenanceLog, log_id)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance log not found")

    if body.status == MaintenanceStatus.COMPLETED and log.status != MaintenanceStatus.COMPLETED:
        # Update vehicle back to available
        vehicle = await db.get(Vehicle, log.vehicle_id)
        if vehicle and vehicle.status == VehicleStatus.IN_SHOP:
            vehicle.status = VehicleStatus.AVAILABLE

    log.status = body.status
    await db.commit()
    await db.refresh(log)
    return log
