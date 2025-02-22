from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import SUBJECTS, WEEK_DAYS

subject_poll_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=subj, callback_data='{0}_00000'.format(iex))
        ] for iex, subj in enumerate(SUBJECTS)
    ]
)

correct_poll_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Correct✅", callback_data='1_00001'),
            InlineKeyboardButton(text="Incorrect❌", callback_data='0_00001')
        ]
    ]
)

editing_poll_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Date🗓", callback_data='0_00003'),
            InlineKeyboardButton(text="Subject🏫", callback_data='1_00003'),
            InlineKeyboardButton(text="Text💬", callback_data='2_00003'),
            InlineKeyboardButton(text="Clear🗑", callback_data='3_00003'),
            InlineKeyboardButton(text="Confirm✅", callback_data='4_00003')
        ]
    ]
)

day_poll_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=day, callback_data='{0}_00002'.format(iex)),
        ] for iex, day in enumerate(WEEK_DAYS)
    ]
)


def nearest_days_poll_keyboard(dates: list | tuple):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=subj, callback_data='{0}_00004'.format(iex))
            ] for iex, subj in enumerate(dates)
        ]
    )
