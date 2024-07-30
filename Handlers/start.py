'''
Хендлеры приветствия и кнопок перехода в главное меню
'''
from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, or_f, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import  Message, CallbackQuery
 
from sqlalchemy.ext.asyncio import AsyncSession
from Database import orm_add_user
from Auxiliaries import hello, StartKB
from Loggs import error_handler_func

# Start Router
start_router = Router()


'''
Обработчик команды старт
'''
@start_router.message(StateFilter(None) ,CommandStart())
@error_handler_func
async def start(message : Message, session : AsyncSession):
    # Сохранение пользователя в таблице
    await orm_add_user(session=session, username=message.from_user.username, chat_id=message.chat.id)
    await message.answer(text= hello, reply_markup=StartKB.as_markup())


'''
Обработчик кнопки для перехода в главное меню
'''
@start_router.callback_query(or_f(F.data == "Main menu", F.data == "Cancel"))
@error_handler_func
async def start_on_button(call : CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text= hello,reply_markup=StartKB.as_markup())

'''
Команда для открытия главного меню
'''
@start_router.message(Command("menu"))
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text= hello, reply_markup=StartKB.as_markup())


