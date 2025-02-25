import os
from config import LOG_ACCESS, LOG_PATH
from loguru import logger


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
    if os.getenv("TOKEN") is None:
        logger.critical("Environment variable 'TOKEN' is not set")
        raise KeyError("TOKEN environment variable not set")