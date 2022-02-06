from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_api.models import User


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserMiddleware, self).__init__()

    async def on_process_message(self, m: types.Message, data: dict):
        await self.process_user(m.from_user, data)
    
    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        await self.process_user(cq.from_user, data)
    
    async def process_user(self, db_user: types.User, data: dict):
        db_user, is_new_user = await self.get_user(db_user, data['db'])
        
        if db_user.banned:
            raise CancelHandler()
        
        data["is_new_user"] = is_new_user
        data["user"] = db_user
    
    @staticmethod
    async def get_user(tg_user: types.User, db: AsyncSession) -> tuple[User, bool]:
        db_user = await db.get(User, tg_user.id)

        is_new_user = False
        user_updated = False

        if db_user is None:
            db_user = User(tg_id=tg_user.id, username=tg_user.username)
            db.add(db_user)

            is_new_user = True

        elif db_user.username != tg_user.username:
            db_user.username = tg_user.username
            user_updated = True

        if user_updated or is_new_user:
            await db.commit()
            await db.refresh(db_user)
        
        return db_user, is_new_user
