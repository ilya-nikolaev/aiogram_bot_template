from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.config_loader import Config


def create_async_db_factory(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=db_engine, expire_on_commit=False)


def create_async_engine_from_config(config: Config) -> AsyncEngine:
    return create_async_engine(
        f"postgresql+asyncpg://"
        f"{config.db_settings.user}:"
        f"{config.db_settings.pswd}@"
        f"{config.db_settings.host}/"
        f"{config.db_settings.name}"
    )
