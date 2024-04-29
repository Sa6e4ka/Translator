from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import  Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
from Database.orm_query import orm_get_def, orm_get_prompt

from states import Definitions
from LOGGING.LoggerConfig import logger

from aiogram.utils.keyboard import InlineKeyboardBuilder

# deleterouter
defr = Router()


def button(text : list):
    KB = InlineKeyboardBuilder()
    for i in text:
        KB.button(text=i, callback_data=i)
    KB.adjust(1,)
    return KB.as_markup()


@defr.callback_query(F.data == 'Учить слова по дефенициям')
async def define_byb(call: CallbackQuery, state: FSMContext, session : AsyncSession):
    await call.answer()
    await call.message.answer('Сейчас тебе отправится определения какого-то изученного ранее нами слова и ты должен будешь написать его на Английском.\n\nЕсли не получается, то ты можешь воспользоваться подсказкой, если не получится даже так, то ты можешь пропустит дефиницию и учить следующую, просто нажав на кнопку.')
    await state.set_state(Definitions.first)

    await sleep(2)

    define = await orm_get_def(session=session)
    await state.update_data(word = define[0])
    await call.message.answer(text=f'<b>definition</b>\n\n{define[1]}\n\n<b>Now enter the word:</b>', reply_markup=button(text=['Остановить урок']))


@defr.message(StateFilter(None),Command('definitions'))
async def define(message : Message, state:FSMContext, session: AsyncSession):
    await message.answer('Сейчас тебе отправится определения какого-то изученного ранее нами слова и ты должен будешь написать его на Английском.\n\nЕсли не получается, то ты можешь воспользоваться подсказкой, если не получится даже так, то ты можешь пропустит дефиницию и учить следующую, просто нажав на кнопку.')
    await state.set_state(Definitions.first)

    await sleep(2)

    define = await orm_get_def(session=session)
    await state.update_data(word = define[0])
    await message.answer(text=f'<b>definition</b>\n\n{define[1]}\n\n<b>Now enter the word:</b>', reply_markup=button(text=['Остановить урок']))


@defr.message(StateFilter(Definitions.first), F.text)
async def check(message: Message, state: FSMContext, session: AsyncSession):
    word = await state.get_data()
    if message.text.lower() == word['word']:
        await message.answer("<b>True!</b>\n\nLet's learn another definition!")

        await sleep(1)

        define = await orm_get_def(session=session)
        await message.answer(text=f'<b>definition</b>\n\n{define[1]}\n\n<b>Now enter the word:</b>', reply_markup=button(text=['Остановить урок']))
        await state.update_data(word = define[0], prompt=define[1])
    elif message.text == '/prompt':
        sd = await state.get_data()
        define = await orm_get_prompt(session=session, data=sd)
        await message.answer(f'prompt to this definition:\n\n{define}')
    else:
        await message.answer('<b>False!</b>\nTry one more time!\n\nIf you will not get it, you can use the prompt --> /prompt\n\nOr you can skip this definition 👇', reply_markup=button(['Пропустить дефиницию'])) 


@defr.callback_query(StateFilter('*'), F.data == 'Остановить урок')
async def stop(call : CallbackQuery, state: FSMContext):
    await call.answer("DO NOT GIVE UP!!")
    await call.message.edit_text("Please don't go away 🥺\n\nTry another functions!", reply_markup=button(text=['Учить слова', 'Учить слова по дефенициям', 'Загрузить слова']))
    await state.clear()

@defr.callback_query(StateFilter('*'), F.data == 'Пропустить дефиницию')
async def stop(call : CallbackQuery, state: FSMContext, session : AsyncSession):
    await call.answer()
    define = await orm_get_def(session=session)
    await call.message.answer(text=f'<b>definition</b>\n\n{define[1]}\n\n<b>Now enter the word:</b>', reply_markup=button(text=['Остановить урок']))
    await state.update_data(word = define[0], prompt=define[1])