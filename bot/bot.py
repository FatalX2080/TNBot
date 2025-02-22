import asyncio
from aiogram import Bot, Dispatcher

from .handlers import commands, handlers, poll
from .middleware import DispatcherMiddleware, VDMiddleware

from models import vault
from models import dispatcher


def routers_configuring(d, v):
    events_dp = DispatcherMiddleware(d)
    events_vdp = VDMiddleware(d, v)

    commands.router.message.middleware(events_dp)
    handlers.router.message.middleware(events_dp)
    poll.router.callback_query.middleware(events_dp)
    poll.router2.callback_query.middleware(events_vdp)

    return commands.router, poll.router, poll.router2, handlers.router


async def main():
    bot = Bot(token="8195953458:AAHSfuJKNFe33uiezHI30xC5Ln0RjTjlxtI")
    dp = Dispatcher()

    events_dispatcher = dispatcher.Dispatcher()
    events_vault = vault.Vault()
    routers = routers_configuring(events_dispatcher, events_vault)
    dp.include_routers(*routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
