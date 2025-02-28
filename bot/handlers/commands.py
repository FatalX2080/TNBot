from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from bot.keyboards import *
from config import GROUP_ID, BASE_MESSAGE_ID
from utils import dt_utils as mdatetime
from .strategy import AddNews
from loguru import logger

from utils.help import uinf, get_logs, formatted_output
from models.exceptions import VaultExceptions

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('It unfortunately still work')


@router.message(Command('state'))
async def cmd_state(message: Message):
    logger.info('User: {0}({1}) check state'.format(*uinf(message)))
    await message.answer('️❗️State: WORK❗️')


# ----------------------------------------------------------------------------------------------------------

@router.message(StateFilter(None), Command('add'))
async def add(message: Message, state: FSMContext):
    text = 'Write a date (<i>dd.mm.yy</i>), or choose below'
    logger.info("User {0}({1}) start adding a news".format(*uinf(message)))
    await message.answer(text, reply_markup=day_poll_keyboard, parse_mode='HTML')
    await state.set_state(AddNews.date)


@router.message(Command('del'))
async def dell(message: Message):
    logger.warning("User {0}(1) try delete a news".format(*uinf(message)))
    await message.answer("It's just a dummy", parse_mode='HTML')


@router.message(Command('log'))
async def log(message: Message):
    logger.warning("User {0}({1}) try get a log file".format(*uinf(message)))
    logs = get_logs()
    if logs is None:
        return await message.answer("Log file doesn't exist", parse_mode='HTML')
    await message.answer("Here is you logs:")
    await message.answer_document( FSInputFile(logs))


@router.message(Command('change'))
async def change(message: Message):
    logger.warning("User {0}({1}) try change a news".format(*uinf(message)))
    await message.answer("It's just a dummy", parse_mode='HTML')


@router.message(Command('print'))
async def cmf_force_print(message: Message, vault):
    if message.text == '/print':
        date = mdatetime.get_date()
    else:
        date = message.text.lstrip('/print ')
        correct = mdatetime.check_date(date)
        if correct: return await message.answer("Date ({0}) is not correct".format(date))
    log_text = "User {0}({1}) use FORCE print at ({2})"
    logger.warning(log_text.format(*uinf(message), date))
    try:
        data = vault.request(date, 1)
        text = formatted_output(date, data)
    except VaultExceptions:
        return await message.answer("Nothing is planned for this day")
    await message.answer("❗️FORCED❗️\n" + text, parse_mode='HTML')


@router.message(Command('group_print'))
async def cmf_force_group_print(message: Message, vault, bot):
    if message.text == '/group_print':
        date = mdatetime.get_date()
    else:
        date = message.text.lstrip('/group_print ')
        correct = mdatetime.check_date(date)
        if correct: return await message.answer("Date ({0}) is not correct".format(date))
    log_text = "User {0}({1}) use FORCE GROUP print at ({2})"
    logger.critical(log_text.format(*uinf(message), date.date()))
    try:
        data = vault.request(date, 1)
        text = formatted_output(date, data)
    except VaultExceptions:
        return await message.answer("Nothing is planned for this day")
    await bot.send_message(
        chat_id=GROUP_ID, text="❗️FORCED❗️\n" + text, parse_mode='HTML',
        reply_to_message_id=BASE_MESSAGE_ID
    )

@router.message(Command('shutdown'))
async def cmd_shutdown(message: Message):
    logger.critical("Shutdown command called")
    await message.answer("It's template")

@router.message(Command('next_few_days'))
async def cmd_next_few_days(message: Message, vault):
    date_delta = 7
    if message.text != '/next_few_days':
        date = message.text.lstrip('/next_few_days ')
        if not date.isdigit() or int(date) < 0:
            raise await message.answer("Days delta ({0}) is not correct".format(date))
        date_delta = int(date)

    days_set = set()
    now = mdatetime.now()
    for i in range(0, date_delta + 1):
        delta = mdatetime.days_delta(i)
        days_set.add(mdatetime.date_to_str(delta + now))
    try:
        res_set = vault.get_coming_days(days_set)
    except VaultExceptions:
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
