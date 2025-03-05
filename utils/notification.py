import asyncio

from loguru import logger

from config import BASE_DELAY, SEND_TIME, GROUP_ID, BASE_MESSAGE_ID
from models.exceptions import VaultExceptions
from utils import mdatetime
from utils.help import formatted_output


async def notify(vault, bot):
    send_flag = 0
    while True:
        await asyncio.sleep(BASE_DELAY)
        if not send_flag and mdatetime.check_send_time(SEND_TIME):
            date = mdatetime.get_date()
            send_flag = 1
            logger.debug("Start sending...")

            try:
                data = vault.request(date, 1)
                text = formatted_output(date, data)
                logger.success("Data was sanded")
                await send(text, bot)
            except VaultExceptions:
                logger.error("Data was not sanded")

            deleted_dates = vault.garbage_collector(date)
            if deleted_dates:
                logger.debug("Deleted dates: {0}".format(deleted_dates))
        elif send_flag and mdatetime.get_time() < mdatetime.tuple_to_time(SEND_TIME[0]):
            logger.debug("Resen a flag")
            send_flag = 0


async def send(text: str, bot):
    await bot.send_message(
        text=text,
        chat_id=GROUP_ID,
        parse_mode='HTML',
        reply_to_message_id=BASE_MESSAGE_ID
    )
