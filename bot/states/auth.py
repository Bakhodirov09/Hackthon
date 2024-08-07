from aiogram.fsm.state import State, StatesGroup

class LoginState(StatesGroup):
    phone_number = State()
    password = State()

class LoginOrRegisterState(StatesGroup):
    command = State()