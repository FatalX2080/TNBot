from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards import *
from utils import dt_utils as mdatetime
from utils.help import get_id
from .strategy import AddNews

router = Router()


@router.message(AddNews.date, F.text.regexp(r"\d{2}.\d{2}.\d\d{1,3}"))
async def date_stage(message: Message, dispatcher, state: FSMContext):
    date_correct = mdatetime.check_date(message.text)
    if date_correct == 0:
        entry_date = message.text
        uid = get_id(message)
        entry_date = entry_date[:6] + entry_date[8:] if len(entry_date) > 8 else entry_date
        dispatcher.add_info(uid, 1, entry_date)
        await message.answer("Choose a subject", reply_markup=subject_poll_keyboard)
        return await state.set_state(AddNews.subj)
    await message.answer('Be carefully. Error date has wrong form (DD.MM.YY).\nRepeat enter',
                         reply_markup=day_poll_keyboard)


@router.message(AddNews.text)
async def text_stage(message: Message, dispatcher, state: FSMContext):
    text = message.text
    uid = get_id(message)
    dispatcher.add_info(get_id(message), 3, text)
    message_text = '<b>Date:</b> {0}\n<b>Subject:</b> {1}\n<b>Text:</b> {2}'
    entry = dispatcher.get(uid)
    text = message_text.format(*entry.info())
    await message.answer(text, reply_markup=correct_poll_keyboard, parse_mode='HTML')
    await state.set_state(AddNews.correct)
