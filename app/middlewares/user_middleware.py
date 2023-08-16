from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserMiddleware, self).__init__()

    async def on_process_message(self, m: types.Message, data: dict):
        await self.process_user(m.from_user, data)
    
    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        await self.process_user(cq.from_user, data)
    
    async def process_user(self, tg_user: types.User, data: dict):
        db_user = await self.get_or_create_user(tg_user, data['db'])
        
        if db_user.banned:
            raise CancelHandler()
        
        data["user"] = db_user
    
    @staticmethod
    async def get_or_create_user(tg_user: types.User, db: AsyncSession) -> User:
        new_db_user = User(
            id=tg_user.id,
            username=tg_user.username,
        )

        db_user = await db.get(User, tg_user.id)
        if db_user is None:
            db_user = new_db_user
            db.add(db_user)
        else:
            await db.merge(new_db_user)

        await db.commit()
        await db.refresh(db_user)

        return db_user
