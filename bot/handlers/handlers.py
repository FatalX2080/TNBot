from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards import *
from utils import dt_utils as mdatetime
from utils.help import get_id
from .strategy import AddNews

router = Router()


@router.message(AddNews.date, F.text.regexp(r"\d{2}.\d{2}.\d\d{1,3}"))
async def date_stage(message: Message, state: FSMContext):
    date_correct = mdatetime.check_date(message.text)
    if date_correct == 0:
        entry_date = message.text
        entry_date = entry_date[:6] + entry_date[8:] if len(entry_date) > 8 else entry_date
        await state.update_data(date=entry_date)
        await message.answer("Choose a subject", reply_markup=subject_poll_keyboard)
        return await state.set_state(AddNews.subj)
    await message.answer('Be carefully. Error date has wrong form (DD.MM.YY).\nRepeat enter',
                         reply_markup=day_poll_keyboard)


@router.message(AddNews.text)
async def text_stage(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    message_text = '<b>Date:</b> {0}\n<b>Subject:</b> {1}\n<b>Text:</b> {2}'
    entry = await state.get_data()
    text = message_text.format(entry['date'], entry['subj'], entry['text'])
    await message.answer(text, reply_markup=correct_poll_keyboard, parse_mode='HTML')
    await state.set_state(AddNews.correct)
