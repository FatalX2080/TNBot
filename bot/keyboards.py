from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUBJECTS, WEEK_DAYS
from random import shuffle

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
                InlineKeyboardButton(text=date, callback_data='{0}_{1}_00004'.format(iex, date[:8]))
            ] for iex, date in enumerate(dates)
        ]
    )


def nearest_days_delete_poll_keyboard(dates: list | tuple):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=date, callback_data='{0}_{1}_00005'.format(iex, date[:8]))
            ] for iex, date in enumerate(dates)
        ]
    )


def delete_poll_keyboard():
    options = [
        InlineKeyboardButton(text="DELETE❌", callback_data='0_00006'),
        InlineKeyboardButton(text="KEEP✅", callback_data='1_00006')
    ]
    shuffle(options)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            options
        ]
    )


def delete_events_poll_keyboard(dates: list | tuple):
    date = [d[0] + ' ' + d[1][:min(len(d[1]), 10)] for d in dates]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=date, callback_data='{0}_00007'.format(iex))
            ] for iex, date in enumerate(date)
        ]
    )