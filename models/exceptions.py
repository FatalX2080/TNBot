from aiogram.exceptions import AiogramError


class AiogramExceptions(AiogramError):
    pass


class UtilsExceptions(Exception):
    pass


class VaultExceptions(Exception):
    def __init__(self, message: str = '', *kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return self.message
