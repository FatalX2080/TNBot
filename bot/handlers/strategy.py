from aiogram.fsm.state import StatesGroup, State

class AddNews(StatesGroup):
    date = State()
    subj = State()
    text = State()
    correct = State()