from asyncore import poll3

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards import *
from utils import help as utils
from utils import dt_utils as mdatetime

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('It unfortunately still work')


@router.message(Command('add'))
async def add(message: Message, dispatcher):
    uid = utils.get_id(message)
    dispatcher.create_news(uid)
    text = 'Write a date (<i>dd.mm.yy</i>), or choose below'
    await message.answer(text, reply_markup=day_poll_keyboard, parse_mode='HTML')


@router.message(Command('state'))
async def cmd_state(message: Message):
    print(message.from_user.id, message.text)
    await message.answer('️❗️State: WORK❗️')


@router.message(Command('force_print'))
async def cmf_force_print(message: Message, dispatcher, vault):
    # /force_print 28.02.25
    if message.text == 'force_print':
        date = mdatetime.now()
    else:
        date = message.text.lstrip('/force_print ')
        correct = mdatetime.check_date(date)
        if correct: return Exception("Data not correct")

    data = vault.get_format(date, 1)
    if not data:
        return await message.answer("Nothing is planned for this day")
    data = "❗️FORCED❗️\n" + data
    await message.answer(data, parse_mode='HTML')