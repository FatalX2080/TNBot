from aiogram import Bot, types
from aiogram.filters import Filter

from config import ADMINS


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in ADMINS