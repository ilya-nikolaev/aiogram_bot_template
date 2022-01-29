from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app.db_api.models import User


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserMiddleware, self).__init__()

    async def on_process_message(self, m: types.Message, data: dict):
        await self.process_user(m.from_user, data)
    
    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        await self.process_user(cq.from_user, data)
    
    async def process_user(self, user: types.User, data: dict):
        user, is_new_user = await self.get_user(user, data['db'])
        
        if user.banned:
            raise CancelHandler()
        
        data["is_new_user"] = is_new_user
        data["user"] = user
    
    @staticmethod
    async def get_user(tg_user: types.User, db: AsyncSession) -> tuple[User, bool]:
        result = await db.execute(select(User).where(User.tg_id == tg_user.id))
        user = result.scalars().first()

        is_new_user = False
        if user is None:
            user = User(tg_id=tg_user.id, username=tg_user.username)
            db.add(user)

            await db.commit()
            await db.refresh(user)

            is_new_user = True
        
        if user.username != tg_user.username:
            user.username = tg_user.username
            await db.commit()
            await db.refresh(user)
        
        return user, is_new_user
