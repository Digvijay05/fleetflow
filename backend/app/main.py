"""FleetFlow — application entry point."""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.v1.routers import analytics, auth, drivers, expenses, maintenance, tracking, trips, vehicles
from app.core.config import settings

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

# --- Rate limiter ---
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Modular Fleet & Logistics Management System API",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Global exception handlers ---
@app.exception_handler(ValueError)
async def value_error_handler(_request: Request, exc: ValueError) -> JSONResponse:
    """Convert unhandled ValueErrors into clean 400 responses."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def generic_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unexpected errors — log and return 500."""
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# --- Routers ---
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(vehicles.router, prefix="/api/v1/vehicles")
app.include_router(drivers.router, prefix="/api/v1/drivers")
app.include_router(trips.router, prefix="/api/v1/trips")
app.include_router(maintenance.router, prefix="/api/v1/maintenance")
app.include_router(expenses.router, prefix="/api/v1/expenses")
app.include_router(analytics.router, prefix="/api/v1/analytics")
app.include_router(tracking.router, prefix="/api/v1/tracking")


@app.get("/health", tags=["system"])
async def health_check():
    """Liveness probe."""
    return {"status": "ok"}
