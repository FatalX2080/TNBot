from aiogram import Router, F

from bot.keyboards import *
from config import SUBJECTS
from utils import dt_utils as mdatetime
from utils.help import get_id

router = Router()
router2 = Router()


@router.callback_query(F.data.regexp(r"\d{1,2}_00000"))  # subjects
async def subject_poll(call, dispatcher):
    iex = int(call.data.split('_')[0])
    text = 'You choose <b>{0}</b>.\nEnter a text please'
    subj = SUBJECTS[iex]
    uid = get_id(call)
    dispatcher.add_info(uid, 2, subj)
    await call.message.answer(text.format(subj), parse_mode='HTML')


@router2.callback_query(F.data.regexp(r"[01]_00001"))  # correction
async def check_poll(call, dispatcher, vault):
    is_correct = int(call.data.split('_')[0])
    uid = get_id(call)
    if not is_correct:
        await call.message.answer("Choose an point for editing", reply_markup=editing_poll_keyboard)
    entry = dispatcher.pop(uid)
    vault.append(entry)
    await call.message.answer("The entry has been added")


@router2.callback_query(F.data.regexp(r"\d_00002"))  # date
async def date_poll(call, dispatcher):
    day_id = int(call.data.split('_')[0])
    now = mdatetime.now()
    cur_day = now.weekday()
    delta = 6 - cur_day + day_id + 1 if cur_day >= day_id else day_id - cur_day + 1
    date = now + mdatetime.days_delta(delta)
    str_date = mdatetime.format_date(date.date())
    dispatcher.add_info(get_id(call), 1, str_date)
    text = 'You choose: <b>{0}</b>\nSubject'.format(str_date)
    await call.message.answer(text, reply_markup=subject_poll_keyboard, parse_mode='HTML')
