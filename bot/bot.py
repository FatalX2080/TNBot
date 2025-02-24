from aiogram import Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from loguru import logger

from .filters import IsAdmin
from .handlers import commands, handlers, poll
from .middleware import VaultMiddleware


def routers_configuring(v):
    events_vault = VaultMiddleware(v)

    cmd_r = commands.router
    hand_r = handlers.router
    poll_r1 = poll.router
    poll_r2 = poll.router2

    cmd_r.message.middleware(events_vault)
    poll_r2.callback_query.middleware(events_vault)
    for r in (cmd_r.message, hand_r.message, poll_r1.callback_query, poll_r2.callback_query):
        r.filter(IsAdmin())
    logger.debug("Routers configured")
    return cmd_r, poll_r1, poll_r2, hand_r


async def main(vault, bot):
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
    routers = routers_configuring(vault)
    dp.include_routers(*routers)

    logger.debug("Starting bot")
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)
