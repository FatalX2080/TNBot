from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        'It unfortunately still work'
    )


@router.message(Command('add'))
async def add(message: Message, dispatcher):
    uid = message.from_user.id
    dispatcher.create_news(uid)
    await message.answer("Ok, now enter a date")
