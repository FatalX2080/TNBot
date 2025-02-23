import asyncio
from contextlib import suppress

from bot import bot
from models import dispatcher
from models import vault


async def main(d, v):
    asyncio.create_task(bot.main(d, v))
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    print("Бот запущен")

    vault = vault.Vault()
    dispatcher = dispatcher.Dispatcher()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(dispatcher, vault))
    for task in asyncio.all_tasks(loop):
        task.cancel()
        while suppress(asyncio.CancelledError):
            loop.run_until_complete(task)

