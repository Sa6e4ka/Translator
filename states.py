from aiogram.fsm.state import State, StatesGroup

class Savewords(StatesGroup):
    English = State()
    Translate = State()

class Learn(StatesGroup):
    Translate = State()

class Delete(StatesGroup):
    Delete = State()

class Definitions(StatesGroup):
    first = State()