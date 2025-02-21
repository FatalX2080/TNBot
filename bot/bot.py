import asyncio
from aiogram import Bot, Dispatcher

from . import handlers
from . import commands
from .middleware import DispatcherMiddleware

from models import dispatcher


async def main():
    bot = Bot(token="8195953458:AAHSfuJKNFe33uiezHI30xC5Ln0RjTjlxtI")
    dp = Dispatcher()

    events_dp = dispatcher.Dispatcher()
    commands.router.message.middleware(DispatcherMiddleware(events_dp))
    dp.include_routers(handlers.router, commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
