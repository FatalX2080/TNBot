import asyncio, os
from contextlib import suppress
from aiogram import Bot
from loguru import logger

from bot import bot
from models import vault
from utils import notification
from utils.help import config_logs, check_env


async def main():
    logger.debug('START')
    check_env()
    tg_bot = Bot(token=os.getenv('TOKEN'))

    events_vault = vault.Vault()
    asyncio.create_task(bot.main(events_vault, tg_bot))
    await notification.notify(events_vault, tg_bot)


if __name__ == "__main__":
    config_logs()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    for task in asyncio.all_tasks(loop):
        task.cancel()
        while suppress(asyncio.CancelledError):
            loop.run_until_complete(task)
