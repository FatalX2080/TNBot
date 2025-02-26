import asyncio
from loguru import logger

from config import BASE_DELAY, SEND_TIME, GROUP_ID, BASE_MESSAGE_ID
from models.exceptions import VaultExceptions
from utils import dt_utils as mdatetime


async def notify(vault, bot):
    send_flag = 0
    logger.debug("Sending notification")
    while True:
        await asyncio.sleep(BASE_DELAY)
        if not send_flag and mdatetime.check_send_time(SEND_TIME):
            logger.debug("Start sending...")
            date = mdatetime.get_date()
            send_flag = 1
            if vault.date_exist(date):
                logger.debug("Date exist...")
                try:
                    data = vault.get_format(date, 1)
                    logger.success("Data was sanded")
                    await bot.send_message(text=data,
                        chat_id=GROUP_ID, parse_mode='HTML',
                        reply_to_message_id=BASE_MESSAGE_ID
                    )
                except VaultExceptions:
                    logger.error("Data was not sanded")
            else:
                logger.debug("Date ({0}) does not exist".format(date))
        elif send_flag and mdatetime.get_time() < mdatetime.tuple_to_time(SEND_TIME[0]):
            logger.debug("Resen a flag")
            send_flag = 0
