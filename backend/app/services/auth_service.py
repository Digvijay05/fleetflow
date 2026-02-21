"""Authentication service — login verification and token issuance."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.models.user import User


class AuthService:
    """Stateless authentication operations."""

    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str) -> tuple[str, str]:
        """Verify credentials and return ``(access_token, role_name)``.

        Raises:
            ValueError: If credentials are invalid.
        """
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        role_name = user.role_rel.name.value
        token = create_access_token(subject=user.id, role=role_name)
        return token, role_name
