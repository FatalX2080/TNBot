from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards import *
from utils import help as utils
from utils import dt_utils as mdatetime
from utils.dt_utils import days_delta

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('It unfortunately still work')


@router.message(Command('state'))
async def cmd_state(message: Message):
    print(message.from_user.id, message.text)
    await message.answer('️❗️State: WORK❗️')


# ----------------------------------------------------------------------------------------------------------

@router.message(Command('add'))
async def add(message: Message, dispatcher):
    uid = utils.get_id(message)
    dispatcher.create_news(uid)
    text = 'Write a date (<i>dd.mm.yy</i>), or choose below'
    await message.answer(text, reply_markup=day_poll_keyboard, parse_mode='HTML')


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


@router.message(Command('next_few_days'))
async def next_few_days(message: Message, dispatcher, vault):
    date_delta = 7
    if message.text != '/next_few_days':
        date = message.text.lstrip('/next_few_days ')
        print(date)
        if not date.isdigit() or int(date) < 0:
            raise Exception("Invalid date")
        date_delta = int(date)

    days_set = set()
    now = mdatetime.now()
    for i in range(1, date_delta + 1):
        delta = mdatetime.days_delta(i)
        days_set.add(mdatetime.date_to_str(delta + now))

    res_set = vault.get_coming_days(days_set)
    if not res_set:
        text = "There are no events for the next <b>{0}</b> days".format(date_delta)
        return await message.answer(text, parse_mode='HTML')

    res_list = list(res_set)
    res_list.sort(key=lambda x: (x[4], x[5], x[2], x[3], x[0], x[1]))
    for i in range(len(res_list)):
        wd = WEEK_DAYS[mdatetime.week_day(res_list[i])]
        res_list[i] += " {0}".format(wd)
    kb = nearest_days_poll_keyboard(res_list)
    text = "The next <b>{0}</b> days:".format(date_delta)
    return await message.answer(text, reply_markup=kb, parse_mode='HTML')
