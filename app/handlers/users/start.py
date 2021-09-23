from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart

from app.filters.bot_admin_filter import BotAdminFilter


async def start_process_message(m: types.Message, is_new_user: bool):
    if is_new_user:
        await m.answer("Hello!")
    else:
        await m.answer("We've already met!")


async def admin_start_process_message(m: types.Message):
    await m.answer("Welcome, Administrator!")


def register_start(dp: Dispatcher):
    dp.register_message_handler(admin_start_process_message, CommandStart(), BotAdminFilter())
    dp.register_message_handler(start_process_message, CommandStart())
