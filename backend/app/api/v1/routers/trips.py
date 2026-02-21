"""Trip management router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import require_role
from app.db.session import get_db
from app.models.user import RoleEnum, User
from app.schemas.trip import TripCreate, TripResponse, TripStatusUpdate
from app.services.trip_service import TripService

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("/", response_model=list[TripResponse])
async def list_trips(db: AsyncSession = Depends(get_db)):
    """Return all trips."""
    return await TripService.list_trips(db)


@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    body: TripCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.DISPATCHER, RoleEnum.FLEET_MANAGER)),
):
    """Dispatch a new trip (Dispatcher / Fleet Manager only)."""
    try:
        trip = await TripService.dispatch_trip(db, body)
        return trip
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.patch("/{trip_id}/status", response_model=TripResponse)
async def update_trip_status(
    trip_id: str,
    body: TripStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.DISPATCHER, RoleEnum.FLEET_MANAGER)),
):
    """Progress a trip through its lifecycle."""
    try:
        trip = await TripService.update_trip_status(db, trip_id, body)
        return trip
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
