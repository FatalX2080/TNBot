import asyncio, os
from contextlib import suppress
from dotenv import load_dotenv
from aiogram import Bot
from loguru import logger

from bot import bot
from models import vault
from utils import notification
from utils.help import config_logs, check_env


async def main(v):
    logger.debug('Starting main')
    load_dotenv(dotenv_path='.env')
    check_env()
    tg_bot = Bot(token=os.getenv('TOKEN'))

    asyncio.create_task(bot.main(v, tg_bot))
    await notification.notify(v, tg_bot)


if __name__ == "__main__":
    config_logs()
    vault = vault.Vault()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(vault))
    for task in asyncio.all_tasks(loop):
        task.cancel()
        while suppress(asyncio.CancelledError):
            loop.run_until_complete(task)
