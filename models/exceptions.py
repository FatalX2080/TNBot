from aiogram.exceptions import AiogramError
from loguru import logger

class AiogramExceptions(AiogramError):
    pass


class UtilsExceptions(Exception):
    pass


class VaultExceptions(Exception):
    def __init__(self, message: str = '', *kwargs):
        self.message = message
        self.kwargs = kwargs
        logger.error("VaultError. {0}".format(message))

    def __str__(self):
        return self.message
