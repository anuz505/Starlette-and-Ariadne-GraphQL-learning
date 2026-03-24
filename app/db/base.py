from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from app.core import DATABASE_URL, DEBUG
from app.models import Base

engine_kwargs = {
    "url": DATABASE_URL,
    "echo": DEBUG,
    "future": True,
    "pool_pre_ping": True
}

if DEBUG:
    engine_kwargs["poolclass"] = NullPool

engine: AsyncEngine = create_async_engine(**engine_kwargs)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
