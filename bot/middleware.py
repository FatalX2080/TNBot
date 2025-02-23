from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from models.dispatcher import Dispatcher
from models.vault import Vault


class DispatcherMiddleware(BaseMiddleware):
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['dispatcher'] = self.dispatcher
        return await handler(event, data)


class VDMiddleware(BaseMiddleware):
    def __init__(self, dispatcher: Dispatcher, vault: Vault):
        self.dispatcher = dispatcher
        self.vault = vault

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['dispatcher'] = self.dispatcher
        data['vault'] = self.vault
        return await handler(event, data)
