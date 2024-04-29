from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import  Message

from sqlalchemy.ext.asyncio import AsyncSession
from Database.orm_query import orm_delete_word

from states import Delete
from LOGGING.LoggerConfig import logger

# deleterouter
dr = Router()

@dr.message(StateFilter(None), Command('delete'))
async def delete(message : Message, state: FSMContext):
    await message.answer('Please enter the word to delete:')
    await state.set_state(Delete.Delete)
    

@dr.message(StateFilter(Delete.Delete), F.text)
async def delete_(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(word = message.text.lower())
    state_data = await state.get_data()
    await orm_delete_word(data=state_data, session=session)

    await state.clear()
    await message.answer('word deleted succefully')