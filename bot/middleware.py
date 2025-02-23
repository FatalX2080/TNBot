from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from models.vault import Vault


class VaultMiddleware(BaseMiddleware):
    def __init__(self, vault: Vault):
        self.vault = vault

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['vault'] = self.vault
        return await handler(event, data)
