"""Password hashing and JWT token utilities."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def hash_password(plain: str) -> str:
    """Return a bcrypt hash of *plain*."""
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    hashed_bytes = bcrypt.hashpw(plain.encode('utf-8'), salt)
    return hashed_bytes.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """Return ``True`` if *plain* matches *hashed*."""
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except ValueError:
        return False


def create_access_token(subject: str, role: str) -> str:
    """Create a signed JWT containing *subject* (user id) and *role*."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and return the JWT payload.  Raises on expiry / tamper."""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
