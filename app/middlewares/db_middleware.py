from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DBMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]
    
    def __init__(self, db_factory: async_sessionmaker):
        super().__init__()
        self.db_factory = db_factory

    async def pre_process(self, obj, data, *args):
        db: AsyncSession = self.db_factory()
        data["db"] = db

    async def post_process(self, obj, data, *args):
        db: AsyncSession = data.get("db")
        await db.close()
