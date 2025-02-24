from config import BASE_DELAY, SEND_TIME, GROUP_ID, BASE_MESSAGE_ID
from utils import dt_utils as mdatetime
import asyncio

from models.exceptions import VaultExceptions

# даты генерируются неправильно
async def notify(vault, bot):
    send_flag = 0
    while True:
        await asyncio.sleep(BASE_DELAY)
        print("проверка")
        if not send_flag and mdatetime.check_send_time(SEND_TIME):
            print("можно отправлять")
            date = mdatetime.get_date()
            send_flag = 1
            if vault.date_exist(date):
                try:
                    data = vault.get_format(date, 1)
                    await bot.send_message(text=data,
                        chat_id=GROUP_ID, parse_mode='HTML',
                        reply_to_message_id=BASE_MESSAGE_ID
                    )
                except VaultExceptions:
                    return Exception("Ошибка получения событий")
        elif send_flag and mdatetime.get_time() < mdatetime.tuple_to_time(SEND_TIME[0]):
            send_flag = 0
