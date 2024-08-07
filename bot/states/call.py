from aiogram.fsm.state import State, StatesGroup

class CallState(StatesGroup):
    type = State()
    title = State()
    description = State()
    file = State()
    location = State()