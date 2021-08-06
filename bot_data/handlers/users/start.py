from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart


async def start_process_message(m: types.Message, is_new_user: bool):
    if is_new_user:
        await m.answer("Hello!")
    else:
        await m.answer("We've already met!")


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_process_message, CommandStart())
