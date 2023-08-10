from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from config.loader import Config


def create_async_db_factory(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=db_engine, expire_on_commit=False)


def create_async_engine_from_config(config: Config) -> AsyncEngine:
    return create_async_engine(get_db_url(config))


def get_db_url(config: Config) -> str:
    return (
        f"postgresql+asyncpg://"
        f"{config.db_settings.user}:"
        f"{config.db_settings.pswd}@"
        f"{config.db_settings.host}:"
        f"{config.db_settings.port}/"
        f"{config.db_settings.name}"
    )
