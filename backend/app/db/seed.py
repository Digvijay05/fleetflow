"""Database seed script — inserts initial roles and a test admin user."""

import asyncio
import logging

from app.core.security import hash_password
from app.db.session import async_session_factory
from app.models.user import Role, RoleEnum, User

logger = logging.getLogger(__name__)

ROLES = [
    RoleEnum.FLEET_MANAGER,
    RoleEnum.DISPATCHER,
    RoleEnum.SAFETY_OFFICER,
    RoleEnum.FINANCIAL_ANALYST,
]

ADMIN_EMAIL = "admin@fleetflow.local"
ADMIN_PASSWORD = "admin1234"


async def seed() -> None:
    """Populate the database with system roles and a test admin."""
    async with async_session_factory() as session:
        # --- Roles ---
        role_map: dict[RoleEnum, Role] = {}
        for role_enum in ROLES:
            role = Role(name=role_enum)
            session.add(role)
            role_map[role_enum] = role
        await session.flush()

        # --- Admin user ---
        admin = User(
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
            role_id=role_map[RoleEnum.FLEET_MANAGER].id,
        )
        session.add(admin)
        await session.commit()
        logger.info("Seed complete: %d roles, 1 admin user.", len(ROLES))


if __name__ == "__main__":
    asyncio.run(seed())
