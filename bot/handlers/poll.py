from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from loguru import logger

from bot.keyboards import *
from config import SUBJECTS
from models.exceptions import VaultExceptions
from utils import dt_utils as mdatetime
from .strategy import AddNews

router = Router()
router2 = Router()


@router.callback_query(AddNews.subj, F.data.regexp(r"\d{1,2}_00000"))  # subjects
async def subject_poll(call, state: FSMContext):
    iex = int(call.data.split('_')[0])
    text = 'You choose <b>{0}</b>.\nEnter a text please'
    subj = SUBJECTS[iex]
    await state.update_data(subj=subj)
    await call.message.answer(text.format(subj), parse_mode='HTML')
    await state.set_state(AddNews.text)


@router2.callback_query(AddNews.correct,F.data.regexp(r"[01]_00001"))  # correction
async def check_poll(call, vault, state: FSMContext):
    is_correct = int(call.data.split('_')[0])
    if not is_correct:
        await call.message.answer("Choose an point for editing", reply_markup=editing_poll_keyboard)
    entry  = await state.get_data()
    vault.append(entry)
    logger.info("Entry {0} has been added".format(tuple(entry.values())))
    await call.message.answer("The entry has been added")
    await state.clear()


@router2.callback_query(AddNews.date, F.data.regexp(r"\d_00002"))  # date
async def date_poll(call, state: FSMContext):
    day = int(call.data.split('_')[0])
    str_date = mdatetime.poll_date_calculating(day)
    await state.update_data(date=str_date)
    text = 'You choose: <b>{0}</b>\nSubject'.format(str_date)
    await call.message.answer(text, reply_markup=subject_poll_keyboard, parse_mode='HTML')
    await state.set_state(AddNews.subj)


@router2.callback_query(F.data.regexp(r"\d{1,2}_\d\d.\d\d.\d\d_00004"))  # force prin poll
async def check_poll(call, vault):
    date = call.data[2:10]
    try:
        data = vault.get_format(date, 1)
        data = "❗️FORCED❗️\n" + data
        logger.warning("FORCED print {0} date to user {1}".format(date, call.message.from_user.id))
        await call.message.answer(data, parse_mode='HTML')
    except VaultExceptions:
        await call.message.answer("There is no any events")