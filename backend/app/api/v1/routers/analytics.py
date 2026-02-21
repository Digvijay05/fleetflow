"""Analytics API router."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api.dependencies import require_role
from app.db.session import get_db
from app.models.expense import Expense
from app.models.maintenance import MaintenanceLog
from app.models.trip import Trip, TripStatus
from app.models.user import RoleEnum, User
from app.models.vehicle import Vehicle, VehicleStatus

router = APIRouter(tags=["analytics"])


@router.get("/dashboard")
async def get_dashboard_metrics(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER, RoleEnum.FINANCIAL_ANALYST)),
):
    """Retrieve high-level KPIs for the command center dashboard."""
    active_fleet_result = await db.execute(
        select(func.count(Vehicle.id)).where(Vehicle.status == VehicleStatus.ON_TRIP)
    )
    active_fleet = active_fleet_result.scalar_one()

    in_shop_result = await db.execute(
        select(func.count(Vehicle.id)).where(Vehicle.status == VehicleStatus.IN_SHOP)
    )
    maintenance_alerts = in_shop_result.scalar_one()

    total_fleet_result = await db.execute(
        select(func.count(Vehicle.id)).where(Vehicle.status != VehicleStatus.RETIRED)
    )
    total_fleet = total_fleet_result.scalar_one()

    utilization_rate = (active_fleet / total_fleet) if total_fleet > 0 else 0.0

    return {
        "activeFleet": active_fleet,
        "maintenanceAlerts": maintenance_alerts,
        "utilizationRate": round(utilization_rate, 2),
        "totalFleet": total_fleet,
    }


@router.get("/roi")
async def get_financial_roi(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER, RoleEnum.FINANCIAL_ANALYST)),
):
    """Aggregate financial ROI across the fleet."""
    # Total trip revenue
    revenue_result = await db.execute(
        select(func.coalesce(func.sum(Trip.revenue), 0))
    )
    total_revenue = float(revenue_result.scalar_one())

    # Total fuel cost
    fuel_result = await db.execute(
        select(func.coalesce(func.sum(Expense.fuel_cost), 0))
    )
    total_fuel_cost = float(fuel_result.scalar_one())

    # Total maintenance cost
    maint_result = await db.execute(
        select(func.coalesce(func.sum(MaintenanceLog.cost), 0))
    )
    total_maint_cost = float(maint_result.scalar_one())

    total_expenses = total_fuel_cost + total_maint_cost

    # Vehicle acquisition cost
    acq_result = await db.execute(
        select(func.coalesce(func.sum(Vehicle.acquisition_cost), 0))
    )
    total_acquisition = float(acq_result.scalar_one())

    # ROI = (Revenue - Expenses) / Acquisition * 100
    roi_pct = ((total_revenue - total_expenses) / total_acquisition * 100) if total_acquisition > 0 else 0.0

    # Total distance for cost-per-km
    dist_result = await db.execute(
        select(func.coalesce(func.sum(Trip.distance_km), 0))
    )
    total_distance = float(dist_result.scalar_one())
    cost_per_km = (total_expenses / total_distance) if total_distance > 0 else 0.0

    # Fuel efficiency
    liters_result = await db.execute(
        select(func.coalesce(func.sum(Expense.fuel_liters), 0))
    )
    total_liters = float(liters_result.scalar_one())
    fuel_efficiency = (total_distance / total_liters) if total_liters > 0 else 0.0

    return {
        "currency": "INR",
        "totalRevenue": round(total_revenue, 2),
        "totalFuelCost": round(total_fuel_cost, 2),
        "totalMaintenanceCost": round(total_maint_cost, 2),
        "totalExpenses": round(total_expenses, 2),
        "netProfit": round(total_revenue - total_expenses, 2),
        "roiPercentage": round(roi_pct, 2),
        "costPerKm": round(cost_per_km, 2),
        "fuelEfficiencyKmPerL": round(fuel_efficiency, 2),
    }


@router.get("/active-trips")
async def get_active_trips(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role(RoleEnum.FLEET_MANAGER, RoleEnum.DISPATCHER)),
):
    """List currently active (dispatched/in-transit) trips with driver & vehicle info."""
    stmt = (
        select(Trip)
        .options(joinedload(Trip.vehicle), joinedload(Trip.driver))
        .where(Trip.status.in_([TripStatus.DISPATCHED, TripStatus.IN_TRANSIT, TripStatus.OUT_FOR_DELIVERY]))
    )
    result = await db.execute(stmt)
    trips = result.unique().scalars().all()

    return [
        {
            "id": t.id,
            "tracking_id": t.tracking_id,
            "origin": t.origin,
            "destination": t.destination,
            "status": t.status.value,
            "vehicle_plate": t.vehicle.license_plate if t.vehicle else "N/A",
            "driver_name": t.driver.name if t.driver else "N/A",
            "cargo_weight": t.cargo_weight,
            "start_time": t.start_time.isoformat() if t.start_time else None,
        }
        for t in trips
    ]
