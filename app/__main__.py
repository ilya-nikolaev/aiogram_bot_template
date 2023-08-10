import asyncio
import logging

import aiogram.types
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.loader import load_config
from db.utils import create_async_engine_from_config, create_async_db_factory
from app.filters.bot_admin_filter import BotAdminFilter
from app.handlers.users.start import register_start
from app.middlewares.db_middleware import DBMiddleware
from app.middlewares.user_middleware import UserMiddleware

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher):
    register_start(dp)


def setup_middlewares(dp: Dispatcher, db_factory: async_sessionmaker):
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

    db_engine = create_async_engine_from_config(config)
    db_factory = create_async_db_factory(db_engine)

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
