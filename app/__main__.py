import asyncio
import logging

import aiogram.types
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app import load_config
from app.db_api.base import Base
from app.filters.bot_admin_filter import BotAdminFilter
from app.handlers.users.start import register_start
from app.middlewares.db_middleware import DBMiddleware
from app.middlewares.user_middleware import UserMiddleware

logger = logging.getLogger(__name__)


def create_db_factory(db_engine: AsyncEngine):
    return sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


def setup_handlers(dp: Dispatcher):
    register_start(dp)


def setup_middlewares(dp: Dispatcher, db_factory: sessionmaker):
    dp.middleware.setup(DBMiddleware(db_factory))
    dp.middleware.setup(UserMiddleware())


def setup_filters(dp: Dispatcher):
    dp.filters_factory.bind(BotAdminFilter)


async def main():
    logging.basicConfig(
        format=u"%(filename)s:%(lineno)-d #%(levelname)-16s [%(asctime)s] %(message)s",
        level=logging.INFO
    )

    config = load_config()

    db_engine = create_async_engine(
        f"postgresql+asyncpg://"
        f"{config.db_settings.user}:"
        f"{config.db_settings.pswd}@"
        f"{config.db_settings.host}/"
        f"{config.db_settings.name}"
    )

    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    db_factory = create_db_factory(db_engine)

    if config.bot_settings.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()

    bot = Bot(
        token=config.bot_settings.token,
        parse_mode=aiogram.types.ParseMode.HTML
    )
    dp = Dispatcher(bot=bot, storage=storage)

    setup_middlewares(dp, db_factory)
    setup_filters(dp)
    setup_handlers(dp)

    try:
        logging.info("Everything is ready to launch!")
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
