"""Alembic env.py — async migration runner."""

import asyncio
import sys
from logging.config import fileConfig
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.core.config import settings
from app.db.base_class import Base

# Import all models so Alembic detects them
from app.models import driver, expense, maintenance, trip, user, vehicle  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(settings.DATABASE_URL)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
