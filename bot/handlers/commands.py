from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards import *
from utils import help as utils

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        'It unfortunately still work'
    )


@router.message(Command('add'))
async def add(message: Message, dispatcher):
    uid = utils.get_id(message)
    dispatcher.create_news(uid)
    await message.answer(
        'Write a date (<i>dd.mm.yy</i>), or choose below',
        reply_markup=day_poll_keyboard, parse_mode='HTML'
    )


@router.message(Command('state'))
async def cmd_state(message: Message):
    print(message.from_user.id, message.text)
    await message.answer('️❗️State: WORK❗️')
