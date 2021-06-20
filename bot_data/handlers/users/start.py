from aiogram import types, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from bot_data.db_api.models import User


async def start_process_message(m: types.Message, db: AsyncSession, user: User):
    
    if user is None:
        user = User(tg_id=m.from_user.id, username=m.from_user.username)
        db.add(user)
        await db.commit()
        
        await m.answer("Добро пожаловать")
    else:
        await m.answer("Вы уже зарегистрированы")


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_process_message, commands=['start'])
