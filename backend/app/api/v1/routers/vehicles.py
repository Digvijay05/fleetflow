"""Vehicle management router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import require_role
from app.db.session import get_db
from app.models.user import RoleEnum, User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate

router = APIRouter(tags=["vehicles"])

@router.get("/", response_model=list[VehicleResponse])
async def list_vehicles(db: AsyncSession = Depends(get_db)):
    """Return all vehicles."""
    result = await db.execute(select(Vehicle))
    return list(result.scalars().all())


@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    body: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER)),
):
    """Register a new vehicle (Fleet Manager only)."""
    vehicle = Vehicle(**body.model_dump())
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


@router.patch("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: str,
    body: VehicleUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER)),
):
    """Update an existing vehicle (Fleet Manager only)."""
    vehicle = await db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(vehicle, field, value)
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def retire_vehicle(
    vehicle_id: str,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER)),
):
    """Soft-delete (retire) a vehicle (Fleet Manager only)."""
    vehicle = await db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    from app.models.vehicle import VehicleStatus

    vehicle.status = VehicleStatus.RETIRED
    await db.commit()
