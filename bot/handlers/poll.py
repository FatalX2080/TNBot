from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from loguru import logger

from bot.keyboards import *
from config import SUBJECTS
from models.exceptions import VaultExceptions
from utils import mdatetime
from utils.help import formatted_output, uinf
from .strategy import AddNews, DelNews

router = Router()


@router.callback_query(AddNews.subj, F.data.regexp(r"\d{1,2}_00000"))  # subjects
async def subject_poll(call, state: FSMContext):
    iex = int(call.data.split('_')[0])
    text = 'You choose <b>{0}</b>.\nEnter a text please'
    subj = SUBJECTS[iex]
    await state.update_data(subj=subj)
    await call.message.answer(text.format(subj), parse_mode='HTML')
    await state.set_state(AddNews.text)


@router.callback_query(AddNews.correct, F.data.regexp(r"[01]_00001"))  # correction
async def check_poll(call, state: FSMContext, vault):
    is_correct = int(call.data.split('_')[0])
    if not is_correct:
        # await call.message.answer("Choose an point for editing", reply_markup=editing_poll_keyboard)
        await call.message.answer("The entry was deleted")
        return await state.clear()
    entry = await state.get_data()
    vault.append(entry)
    logger.info("Entry {0} has been added".format(tuple(entry.values())))
    await call.message.answer("The entry has been added")
    await state.clear()


@router.callback_query(AddNews.date, F.data.regexp(r"\d_00002"))  # date
async def date_poll(call, state: FSMContext):
    day = int(call.data.split('_')[0])
    str_date = mdatetime.poll_date_calculating(day)
    await state.update_data(date=str_date)
    text = 'You choose: <b>{0}</b>\nSubject'.format(str_date)
    await call.message.answer(text, reply_markup=subject_poll_keyboard, parse_mode='HTML')
    await state.set_state(AddNews.subj)


@router.callback_query(F.data.regexp(r"\d{1,2}_\d\d.\d\d.\d\d_00004"))  # force prin poll
async def check_poll(call, vault):
    date = call.data[2:10]
    try:
        data = vault.request(date, 1)
        text = formatted_output(date, data)
        text = "❗️FORCED❗️\n" + text
        logger.warning("FORCED print {0} date to user ({1})".format(date, call.from_user.id))
        await call.message.answer(text, parse_mode='HTML')
    except VaultExceptions:
        await call.message.answer("There is no any events")


@router.callback_query(DelNews.date, F.data.regexp(r"\d{1,2}_\d\d.\d\d.\d\d_00005"))  # delete date
async def date_for_deleting_poll(call, vault, state: FSMContext):
    date = call.data[2:10]
    data = vault.request(date, 1)
    kb = delete_events_poll_keyboard(data)
    text = "This day has <b>{0}</b> entries choose one: ".format(len(data))
    await state.update_data(date=date)
    await state.set_state(DelNews.iex)
    await call.message.answer(text, reply_markup=kb, parse_mode='HTML')


@router.callback_query(DelNews.iex, F.data.regexp(r"\d{1,2}_00007"))  # delete entry iex
async def entry_for_deleting_poll(call, vault, state: FSMContext):
    iex = int(call.data.split('_')[0])
    date = (await state.get_data())['date']
    entry = vault.request(date, 1)[iex]
    text = "<b>You want delete entry:</b>\nDate: {0}\nSubject: {1}\nText: {2}"
    text = text.format(date, *entry)
    kb = delete_poll_keyboard()
    await state.update_data(iex=iex)
    await state.set_state(DelNews.correct)
    await call.message.answer(text, reply_markup=kb, parse_mode='HTML')


@router.callback_query(DelNews.correct, F.data.regexp(r"\d_00006"))  # delete correction
async def entry_for_deleting_poll(call, vault, state: FSMContext):
    if call.data[0] == '0':
        date = await state.get_data()
        entry = vault.delete(date['date'], date['iex'])
        await call.message.answer('Entry was removed', parse_mode='HTML')
        logger.warning('Entry ({0}) was removed by {1}({2})'.format(entry, *uinf(call)))
    else:
        logger.info("The deletion has been suspended")
        await call.message.answer("The deletion has been suspended")
    await state.clear()
