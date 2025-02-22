import asyncio
from aiogram import Bot, Dispatcher

from .handlers import commands, handlers, poll
from .middleware import DispatcherMiddleware, VDMiddleware
from .filters import IsAdmin


def routers_configuring(d, v):
    events_dp = DispatcherMiddleware(d)
    events_vdp = VDMiddleware(d, v)

    cmd_r = commands.router
    hand_r = handlers.router
    poll_r1 = poll.router
    poll_r2 = poll.router2

    cmd_r.message.middleware(events_vdp)
    cmd_r.message.filter(IsAdmin())
    hand_r.message.middleware(events_dp)
    hand_r.message.filter(IsAdmin())
    poll_r1.callback_query.middleware(events_dp)
    poll_r1.callback_query.filter(IsAdmin())
    poll_r2.callback_query.middleware(events_vdp)
    poll_r2.callback_query.filter(IsAdmin())

    return cmd_r, poll_r1, poll_r2, hand_r


async def main(dispatcher, vault):
    bot = Bot(token="8195953458:AAHSfuJKNFe33uiezHI30xC5Ln0RjTjlxtI")
    dp = Dispatcher()

    routers = routers_configuring(dispatcher, vault)
    dp.include_routers(*routers)

    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
