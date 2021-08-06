from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from bot_data.db_api.models import User


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserMiddleware, self).__init__()
    
    async def on_process_message(self, m: types.Message, data: dict):
        user = await self.get_user(m.from_user.id, data['db'])
        self.check_banned(user)
        data["user"] = user
    
    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        user = await self.get_user(cq.from_user.id, data['db'])
        self.check_banned(user)
        data["user"] = user
    
    @staticmethod
    def check_banned(user: User):
        if getattr(user, 'banned', False):
            raise CancelHandler()
    
    @staticmethod
    async def get_user(user_id: int, db: AsyncSession) -> User:
        result = await db.execute(select(User).where(User.tg_id == user_id))
        return result.scalars().first()
