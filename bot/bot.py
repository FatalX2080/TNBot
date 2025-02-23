import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy

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
    cmd_r.message.filter(IsAdmin())
    hand_r.message.filter(IsAdmin())
    poll_r1.callback_query.filter(IsAdmin())
    poll_r2.callback_query.filter(IsAdmin())

    return cmd_r, poll_r1, poll_r2, hand_r


async def main(vault):
    bot = Bot(token=os.environ['TOKEN'])
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

    routers = routers_configuring(vault)
    dp.include_routers(*routers)

    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
