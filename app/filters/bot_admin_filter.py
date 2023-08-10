from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Filter

from config.loader import load_config


class BotAdminFilter(Filter):
    def __init__(self):
        self.config = load_config()
    
    async def check(self, u: Union[types.Message, types.CallbackQuery, types.InlineQuery]) -> bool:
        return u.from_user.id in self.config.bot_settings.admins
