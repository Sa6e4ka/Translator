'''
Сохранение слов в личный словарь пользователя
'''
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter,  or_f

from sqlalchemy.ext.asyncio import AsyncSession
from Database import orm_save_word

from Auxiliaries import Savewords, button
from Loggs import error_handler_func


# Save Personal Router
save_personal_router = Router()
 

'''
Обработчик нажатия кнопки для сохранения слова в личный словарь пользователя
'''
@save_personal_router.callback_query(or_f(F.data == 'Save words', F.data == "Save one more"))
@error_handler_func
async def enter_eng_word_byb(call: CallbackQuery, state: FSMContext):
    await state.set_state(Savewords.English)
    await call.answer()
    await call.message.edit_text('Please enter the word <b>in English:</b>', reply_markup=button(["Cancel"]))


'''
Обработчик команды для сохранения слов в личный словарь
'''
@save_personal_router.message(StateFilter(None) ,Command('saveword'))
@error_handler_func
async def enter_eng_word(message: Message, state: FSMContext):
    await state.set_state(Savewords.English)
    await message.answer('Please enter the word <b>in English:</b>', reply_markup=button(["Cancel"]))
    
    
'''
Сохранение в словарь состояния слова на иврите и chat_id пользователя
'''
@save_personal_router.message(StateFilter(Savewords.English), F.text)
@error_handler_func
async def enter_rus_word_orm(message: Message, state: FSMContext):
    await state.update_data(word = message.text.lower(), chat_id = message.chat.id)
    await message.answer("Now enter it's <b>translation</b>")
    await state.set_state(Savewords.Translate)


'''
Сохранения в словарь состояния транскрипции слова
Сохранения слова в таблице
'''
@save_personal_router.message(StateFilter(Savewords.Translate), F.text)
@error_handler_func
async def saveword_orm_with_translation(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(translation = message.text.lower())
    sd = await state.get_data()
    # Функция сохранения слова в таблице
    await orm_save_word(session=session, data=sd)

    await state.clear()
    await message.answer('Word was uploaded successfully!\n\n<b>Now you are able to learn all your words via button below 👇</b>', reply_markup=button(["Learn words", "Save one more"]))
   

