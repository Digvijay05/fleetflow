"""Seed script — populates the database with Indian-context mock data."""

import asyncio
import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import async_session_factory
from app.models.driver import Driver, DriverStatus
from app.models.expense import Expense
from app.models.maintenance import MaintenanceLog, MaintenanceStatus, MaintenanceType
from app.models.trip import Trip, TripStatus
from app.models.user import Role, RoleEnum, User
from app.models.vehicle import Vehicle, VehicleStatus

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def seed_data() -> None:
    async with async_session_factory() as db:
        result = await db.execute(select(Role))
        if result.scalars().first():
            logger.info("Database already seeded. Skipping.")
            return

        logger.info("Seeding database with Indian-context mock data...")

        # 1. Roles
        roles = []
        for role_enum in RoleEnum:
            role = Role(name=role_enum)
            roles.append(role)
            db.add(role)
        await db.flush()

        # 2. Users
        fm_role = await db.scalar(select(Role).where(Role.name == RoleEnum.FLEET_MANAGER))
        disp_role = await db.scalar(select(Role).where(Role.name == RoleEnum.DISPATCHER))
        safety_role = await db.scalar(select(Role).where(Role.name == RoleEnum.SAFETY_OFFICER))
        analyst_role = await db.scalar(select(Role).where(Role.name == RoleEnum.FINANCIAL_ANALYST))
        cust_role = await db.scalar(select(Role).where(Role.name == RoleEnum.CUSTOMER))

        admin = User(
            email="admin@fleetflow.com",
            password_hash=hash_password("admin123"),
            role_id=fm_role.id,
        )
        dispatcher = User(
            email="dispatcher@fleetflow.com",
            password_hash=hash_password("dispatch123"),
            role_id=disp_role.id,
        )
        safety_officer = User(
            email="safety@fleetflow.com",
            password_hash=hash_password("safety123"),
            role_id=safety_role.id,
        )
        analyst = User(
            email="analyst@fleetflow.com",
            password_hash=hash_password("analyst123"),
            role_id=analyst_role.id,
        )
        customer = User(
            email="customer@fleetflow.com",
            password_hash=hash_password("customer123"),
            role_id=cust_role.id,
        )
        db.add_all([admin, dispatcher, safety_officer, analyst, customer])
        await db.flush()

        # 3. Vehicles (Indian fleet)
        vehicles = [
            Vehicle(
                name="Tata Signa 4825.TK",
                model="2023",
                license_plate="GJ01AB1234",
                max_capacity_kg=25000,
                odometer_km=48000,
                acquisition_cost=2500000.0,
                status=VehicleStatus.AVAILABLE,  # Trip COMPLETED → vehicle released
            ),
            Vehicle(
                name="Ashok Leyland Ecomet 1215",
                model="2022",
                license_plate="MH02CD5678",
                max_capacity_kg=12000,
                odometer_km=85000,
                acquisition_cost=1800000.0,
                status=VehicleStatus.ON_TRIP,  # Active trip: TRK-DLKJ4412
            ),
            Vehicle(
                name="Mahindra Blazo X 35",
                model="2023",
                license_plate="DL03EF9012",
                max_capacity_kg=35000,
                odometer_km=120000,
                acquisition_cost=3200000.0,
                status=VehicleStatus.ON_TRIP,
            ),
            Vehicle(
                name="BharatBenz 1617R",
                model="2021",
                license_plate="KA04GH3456",
                max_capacity_kg=16000,
                odometer_km=195000,
                acquisition_cost=2200000.0,
                status=VehicleStatus.IN_SHOP,
            ),
            Vehicle(
                name="Eicher Pro 2049",
                model="2024",
                license_plate="TN05IJ7890",
                max_capacity_kg=9000,
                odometer_km=12000,
                acquisition_cost=1400000.0,
                status=VehicleStatus.ON_TRIP,  # Active trip: TRK-KOPT5543
            ),
        ]
        db.add_all(vehicles)
        await db.flush()

        # 4. Drivers (Indian names & licenses)
        drivers = [
            Driver(
                name="Rajesh Patel",
                license_number="GJ07-2019-0045231",
                license_expiry=date.today() + timedelta(days=365),
                safety_score=98.5,
                status=DriverStatus.ON_DUTY,  # Trip COMPLETED → driver released
            ),
            Driver(
                name="Priya Sharma",
                license_number="MH12-2020-0078543",
                license_expiry=date.today() + timedelta(days=180),
                safety_score=100.0,
                status=DriverStatus.ON_TRIP,  # Active trip: TRK-DLKJ4412
            ),
            Driver(
                name="Amit Kumar",
                license_number="DL05-2018-0012890",
                license_expiry=date.today() + timedelta(days=700),
                safety_score=92.0,
                status=DriverStatus.ON_TRIP,
            ),
            Driver(
                name="Sunita Desai",
                license_number="KA03-2021-0034567",
                license_expiry=date.today() - timedelta(days=10),
                safety_score=85.5,
                status=DriverStatus.SUSPENDED,
            ),
            Driver(
                name="Vikram Singh",
                license_number="TN09-2022-0098123",
                license_expiry=date.today() + timedelta(days=500),
                safety_score=95.0,
                status=DriverStatus.ON_TRIP,  # Active trip: TRK-KOPT5543
            ),
        ]
        db.add_all(drivers)
        await db.flush()

        # 5. Trips (Indian cities, ₹ revenue)
        now = datetime.now(tz=timezone.utc)
        trips = [
            Trip(
                vehicle_id=vehicles[0].id,
                driver_id=drivers[0].id,
                customer_id=customer.id,
                tracking_id="TRK-ADMU8821",
                origin="Ahmedabad Warehouse",
                destination="Mumbai Distribution Center",
                cargo_weight=18000,
                distance_km=530.0,
                revenue=85000.0,
                status=TripStatus.COMPLETED,
                start_time=now - timedelta(days=2),
                end_time=now - timedelta(days=1, hours=14),
            ),
            Trip(
                vehicle_id=vehicles[1].id,
                driver_id=drivers[1].id,
                customer_id=customer.id,
                tracking_id="TRK-DLKJ4412",
                origin="Delhi Hub",
                destination="Jaipur Terminal",
                cargo_weight=9500,
                distance_km=280.0,
                revenue=45000.0,
                status=TripStatus.DISPATCHED,
                start_time=now - timedelta(hours=5),
                end_time=None,
            ),
            Trip(
                vehicle_id=vehicles[2].id,
                driver_id=drivers[2].id,
                customer_id=customer.id,
                tracking_id="TRK-BLCH7790",
                origin="Bengaluru Tech Park",
                destination="Chennai Port",
                cargo_weight=28000,
                distance_km=345.0,
                revenue=125000.0,
                status=TripStatus.IN_TRANSIT,
                start_time=now - timedelta(hours=8),
                end_time=None,
            ),
            Trip(
                vehicle_id=vehicles[4].id,
                driver_id=drivers[4].id,
                customer_id=customer.id,
                tracking_id="TRK-KOPT5543",
                origin="Kolkata Depot",
                destination="Patna Warehouse",
                cargo_weight=7000,
                distance_km=590.0,
                revenue=55000.0,
                status=TripStatus.OUT_FOR_DELIVERY,
                start_time=now - timedelta(hours=12),
                end_time=None,
            ),
        ]
        db.add_all(trips)
        await db.flush()

        # 6. Maintenance Logs (₹ costs)
        maint_logs = [
            MaintenanceLog(
                vehicle_id=vehicles[3].id,
                type=MaintenanceType.REACTIVE,
                description="Engine overheating — coolant system repair",
                cost=45000.0,
                date=date.today() - timedelta(days=3),
                odometer_km=194500,
                status=MaintenanceStatus.OPEN,
            ),
            MaintenanceLog(
                vehicle_id=vehicles[1].id,
                type=MaintenanceType.PREVENTATIVE,
                description="Oil change, air filter & tire rotation",
                cost=8500.0,
                date=date.today() - timedelta(days=45),
                odometer_km=80000,
                status=MaintenanceStatus.COMPLETED,
            ),
            MaintenanceLog(
                vehicle_id=vehicles[0].id,
                type=MaintenanceType.PREVENTATIVE,
                description="Brake pad replacement",
                cost=12000.0,
                date=date.today() - timedelta(days=20),
                odometer_km=45000,
                status=MaintenanceStatus.COMPLETED,
            ),
        ]
        db.add_all(maint_logs)
        await db.flush()

        # 7. Expenses (Indian diesel prices ~₹92/L)
        expenses = [
            Expense(
                vehicle_id=vehicles[0].id,
                trip_id=trips[0].id,
                fuel_liters=110.0,
                fuel_cost=10120.0,
                date=date.today() - timedelta(days=2),
            ),
            Expense(
                vehicle_id=vehicles[2].id,
                trip_id=trips[2].id,
                fuel_liters=85.0,
                fuel_cost=7820.0,
                date=date.today(),
            ),
            Expense(
                vehicle_id=vehicles[1].id,
                trip_id=trips[1].id,
                fuel_liters=60.0,
                fuel_cost=5520.0,
                date=date.today(),
            ),
        ]
        db.add_all(expenses)

        await db.commit()
        logger.info("Database successfully seeded with Indian-context data.")


if __name__ == "__main__":
    asyncio.run(seed_data())
