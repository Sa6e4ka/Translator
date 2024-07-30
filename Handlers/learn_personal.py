'''
Режим обучения словам из личного словаря пользователя
'''
from typing import Union
from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import  Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
from Database import orm_get_rand_personal_word

from Auxiliaries import button, Learn
from Loggs import error_handler_func

# Learn Router
learn_router = Router()


'''
Функция для режима обучения словам из личного словаря пользователя.
Обрабатывает 2 сценария:
    Ввод команды
    Нажатие кнопки
'''
async def process_learn(state: FSMContext, session: AsyncSession, chat_id: int, message_or_call: Union[Message, CallbackQuery]):
    try:
        word = await orm_get_rand_personal_word(session=session, chat_id=chat_id)
        await state.set_state(Learn.Translate)
        intro_message = (
            "<b>Get ready!</b>\n\nLesson starts in 3 seconds!"
        )
        
        if isinstance(message_or_call, Message):
            await message_or_call.answer(intro_message)
            await sleep(3)

            await message_or_call.answer(
            text=f"The word:<b>\n\n{word[0]}</b>\n\nNow enter it's translation:",
            reply_markup=button(text=['Skip', "Stop lesson"])
        )
            await state.update_data(translation=word[1], word=word[0])
            return
        
        await message_or_call.message.edit_text(intro_message)
        await sleep(5)
        await message_or_call.message.edit_text(
            text=f"The word:<b>\n\n{word[0]}</b>\n\nNow enter it's translation:",
            reply_markup=button(text=['Skip', "Stop lesson"])
        )
        await state.update_data(translation=word[1], word=word[0])
    except AttributeError:
        error_messaage = "It seems like you stil don't have any words in your vocabulary 🤷‍♂️"
        if isinstance(message_or_call, Message):
            await message_or_call.answer(error_messaage, reply_markup=button(["Main menu", "Save word"]))
            return
        await message_or_call.message.edit_text(error_messaage, reply_markup=button(text=["Main menu", "Save word"]))


'''
Обработчик нажатия кнопки для остановки режима обучения
'''
@learn_router.callback_query(or_f(F.data == "Stop lesson"))
@error_handler_func
async def stop_lesson(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text="The lesson was stopped!\n\nI hope that you're not going to give up so easily 😈", reply_markup=button(["Main menu"]))


'''
Обработчик нажатия кнопки для начала режима обучения
'''
@learn_router.callback_query(or_f(F.data == 'Learn words'))
@error_handler_func
async def learn_byb(call: CallbackQuery, state: FSMContext, session : AsyncSession):
    await process_learn(state, session, call.message.chat.id, call)


'''
Обработчик ввода команды для начала режима обучения
'''
@learn_router.message(StateFilter(None), Command('learnwords'))
@error_handler_func
async def learn(message: Message, session: AsyncSession, state: FSMContext):
    await process_learn(state, session, message.chat.id, message)


'''
Обработчик введенного пользователем перевода:
    Проверяет его и дает ввести заново если он не правильный
'''
@learn_router.message(StateFilter(Learn.Translate), F.text)
@error_handler_func
async def check(message: Message, state: FSMContext, session: AsyncSession):
     
    state_data = await state.get_data()
    if message.text.lower() == state_data["translation"]:
        await message.answer("<b>True</b> 🥳\n\nCatch the next one 👇")
        
        await sleep(1)

        # Получение случайного слова из личной таблицы пользователя
        word = await orm_get_rand_personal_word(session=session, chat_id=message.chat.id)
        await message.answer(text=f"The word:<b>\n\n{word[0]}</b>\n\nNow enter it's translation:", reply_markup=button(text=['Skip', "Stop lesson"]))
        await state.update_data(translation = word[1], word = word[0])
        return
    
    await message.answer("<b>Wrong</b> 😨\n\nLets try one more time!", reply_markup=button(['Skip', "Stop lesson"]))


'''
Обработчие нажатия кнопки для пропуска слова
'''
@learn_router.callback_query(F.data == 'Skip')
@error_handler_func
async def skip(call : CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.answer()
    sd = await state.get_data()
    await call.message.edit_text(
        text=f"The word - {sd["word"]}\n\nIt's translation - <b>{sd["translation"]}</b>"
    )
    await sleep(3)
    
    # Получение случайного слова из личной таблицы пользователя
    word = await orm_get_rand_personal_word(session=session, chat_id=call.message.chat.id)
    await call.message.edit_text(text=f"The word:<b>\n\n{word[0]}</b>\n\nNow enter it's translation:", reply_markup=button(text=['Skip', "Stop lesson"]))
    
    await state.update_data(translation = word[1], word = word[0])