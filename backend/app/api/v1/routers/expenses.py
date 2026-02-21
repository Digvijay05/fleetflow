"""Expense API router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import require_role
from app.db.session import get_db
from app.models.expense import Expense
from app.models.trip import Trip
from app.models.user import RoleEnum, User
from app.models.vehicle import Vehicle
from app.schemas.expense import ExpenseCreate, ExpenseResponse

router = APIRouter(tags=["expenses"])

@router.get("/", response_model=list[ExpenseResponse])
async def list_expenses(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER, RoleEnum.FINANCIAL_ANALYST)),
):
    """List all expenses for financial analytics."""
    result = await db.execute(select(Expense))
    return list(result.scalars().all())


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def log_expense(
    body: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER, RoleEnum.FINANCIAL_ANALYST)),
):
    vehicle = await db.get(Vehicle, body.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    trip = await db.get(Trip, body.trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

    if trip.vehicle_id != body.vehicle_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Mismatched vehicle_id and trip_id"
        )

    expense = Expense(**body.model_dump())
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense
