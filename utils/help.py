import os
from config import LOG_ACCESS, LOG_PATH
from loguru import logger
from dotenv import load_dotenv
from pathlib import Path


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
