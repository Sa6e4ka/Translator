'''
Удаление слова из словарей
'''
from aiogram import F, Router
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import  Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
from Database import orm_delete_word

from Auxiliaries import Delete, button
from Loggs import error_handler_func


# Delete Router
delete_router = Router()


'''
Обработчик команды для удаления слова
'''
@delete_router.message(StateFilter(None), Command("delete"))
@error_handler_func
async def choose_dict_to_delete(message : Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Please type the word that you want delete", reply_markup=button(["Main menu"]))
    await state.set_state(Delete.Delete)


'''
Обработчик нажатия кнопок с выбором словаря
'''
@delete_router.callback_query(or_f(F.data == "Delete words",F.data == "Delete one more", F.data == "Delete right one")) 
@error_handler_func
async def choose_on_button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(text="Please type the word that you want delete")   
    await state.set_state(Delete.Delete)


'''
Удаление слова из личного словаря
'''
@delete_router.message(StateFilter(Delete.Delete), F.text)
@error_handler_func
async def delete_personal_word(message: Message, state: FSMContext, session: AsyncSession):
        result = await orm_delete_word(
             word = message.text.lower(), chat_id = message.chat.id, session=session
        )

        if result is not None:
            await message.answer(result, reply_markup=button(["Delete right one", "Main menu"]))
            await state.clear()
            return
        
        await message.answer('Word was deleted successfully', reply_markup=button(["Delete one more", "Main menu"]))
        await state.clear()
   
