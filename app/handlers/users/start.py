from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart

from app.filters.bot_admin_filter import BotAdminFilter


async def start_process_message(m: types.Message):
    await m.answer("Hello!")


async def admin_start_process_message(m: types.Message):
    await m.answer("Hello, admin!")


def register_start(dp: Dispatcher):
    dp.register_message_handler(admin_start_process_message, CommandStart(), BotAdminFilter())
    dp.register_message_handler(start_process_message, CommandStart())
