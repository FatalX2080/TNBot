import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from . import mdatetime
from config import LOG_ACCESS, LOG_PATH
from models.exceptions import VaultExceptions
from config import LOG_ACCESS, BACKUP_ACCESS, ADMINS_DEBUG, SEND_TIME

def uinf(msg) -> tuple[str, int]:
    return msg.from_user.username, msg.from_user.id


def config_logs():
    if LOG_ACCESS:
        if not os.path.exists(LOG_PATH[0]):
            os.makedirs(LOG_PATH[0])
        path = os.path.join(*LOG_PATH)
        if not os.path.exists(path):
            open(path, 'w').close()
        logger.debug("Log file path: {0}".format(path))
        logger.add(path, enqueue=True, compression='.zip')

    logger_msg = 'starting params FILE_LOGGING [{0}] BACKUP [{1}] ADMIN_DEBUG [{2}] SEND_TIME [{3}]'
    send_time = '{0}:{1}-{2}:{3}'.format(*SEND_TIME[0], *SEND_TIME[1])
    format_params = (int(LOG_ACCESS), int(BACKUP_ACCESS), int(ADMINS_DEBUG), send_time)
    logger.warning(logger_msg.format(*format_params))



def get_logs():
    if not os.path.exists(LOG_PATH[0]):
        os.makedirs(LOG_PATH[0])
        return None
    path = os.path.join(*LOG_PATH)
    if not os.path.exists(path):
        open(path, 'w').close()
        return None
    return path


def check_env():
    dotenv_path = os.path.join(Path(__file__).resolve().parents[0], '..', '.env')
    load_dotenv(dotenv_path=dotenv_path)
    if os.getenv("TOKEN") is None:
        logger.critical("Environment variable 'TOKEN' is not set")
        raise KeyError("TOKEN environment variable not set")


def formatted_output(date: str, data: list) -> str:
    base = "News at <b>{0}({1})</b>:\n".format(date, len(data))
    subjects_dict = {}

    for news in sorted(data):
        subjects_dict.setdefault(news[0], []).append(news[1])

    for key in subjects_dict.keys():
        information = '  · ' + '\n  · '.join(subjects_dict[key])
        base += key + '\n' + information + '\n'

    return base


def get_nfd(vault, date_delta: int = 7) -> None | list:  # fet next few days
    days_set = set()
    now = mdatetime.now()
    for i in range(0, date_delta + 1):
        delta = mdatetime.days_delta(i)
        days_set.add(mdatetime.date_to_str(delta + now))
    try:
        res_set = vault.get_coming_days(days_set)
    except VaultExceptions:
        return None

    res_list = list(res_set)
    res_list.sort(key=lambda x: mdatetime.dt_comp_prepare(x), reverse=True)
    return res_list
