from aiogram import Bot, types
from aiogram.filters import Filter
from loguru import logger
from config import ADMINS, ADMINS_DEBUG
from utils.help import uinf


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        if ADMINS_DEBUG and message.from_user.id not in ADMINS:
            logger.warning("Request from an unauthorized user: {0}({1})".format(*uinf(message)))
        return message.from_user.id in ADMINS


class FromUser(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.chat.id > 0
