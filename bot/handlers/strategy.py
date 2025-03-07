from aiogram.fsm.state import StatesGroup, State


class AddNews(StatesGroup):
    date = State()
    subj = State()
    text = State()
    correct = State()


class DelNews(StatesGroup):
    date = State()
    iex = State()
    correct = State()
