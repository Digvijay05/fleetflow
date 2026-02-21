"""Authentication router."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])

limiter = Limiter(key_func=get_remote_address)


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
async def login(request: Request, body: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate a user and return a JWT. Rate-limited to 5 req/min per IP."""
    try:
        token, role = await AuthService.authenticate(db, body.email, body.password)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return LoginResponse(access_token=token, role=role)
