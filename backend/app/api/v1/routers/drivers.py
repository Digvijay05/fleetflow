"""Driver management router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import require_role
from app.db.session import get_db
from app.models.driver import Driver
from app.models.user import RoleEnum, User
from app.schemas.driver import DriverCreate, DriverResponse, DriverUpdate

router = APIRouter(tags=["drivers"])

@router.get("/", response_model=list[DriverResponse])
async def list_drivers(db: AsyncSession = Depends(get_db)):
    """Return all drivers."""
    result = await db.execute(select(Driver))
    return list(result.scalars().all())


@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(
    body: DriverCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER, RoleEnum.SAFETY_OFFICER)),
):
    """Register a new driver."""
    driver = Driver(**body.model_dump())
    db.add(driver)
    await db.commit()
    await db.refresh(driver)
    return driver


@router.patch("/{driver_id}", response_model=DriverResponse)
async def update_driver(
    driver_id: str,
    body: DriverUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER, RoleEnum.SAFETY_OFFICER)),
):
    """Update an existing driver."""
    driver = await db.get(Driver, driver_id)
    if driver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(driver, field, value)
    await db.commit()
    await db.refresh(driver)
    return driver
