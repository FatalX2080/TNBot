import asyncio, os
from contextlib import suppress
from dotenv import load_dotenv
from aiogram import Bot

from bot import bot
from models import vault
from utils import notification


async def main(v):
    load_dotenv(dotenv_path='.env')
    tg_bot = Bot(token=os.getenv('TOKEN'))

    asyncio.create_task(bot.main(v, tg_bot))
    await notification.notify(v, tg_bot)


if __name__ == "__main__":
    print("Бот запущен")

    vault = vault.Vault()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(vault))
    for task in asyncio.all_tasks(loop):
        task.cancel()
        while suppress(asyncio.CancelledError):
            loop.run_until_complete(task)
