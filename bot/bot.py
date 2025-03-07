from aiogram import Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from loguru import logger

from .filters import IsAdmin, FromUser
from .handlers import commands, handlers, poll
from .middleware import VaultMiddleware


async def main(vault, bot):
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
    routers = routers_configuring(vault)
    dp.include_routers(*routers)

    logger.debug("Starting bot")
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)


# ----------------------------------------------------------------------------------------------------------
def routers_configuring(v):
    events_vault = VaultMiddleware(v)

    cmd_r = commands.router
    hand_r = handlers.router
    poll_r = poll.router

    cmd_r.message.middleware(events_vault)
    poll_r.callback_query.middleware(events_vault)
    for r in (cmd_r.message, hand_r.message, poll_r.callback_query):
        r.filter(FromUser(), IsAdmin())
    logger.debug("Routers configured")
    return cmd_r, poll_r, hand_r
