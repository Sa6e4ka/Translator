'''
Получение списка слов из словаря пользователя, сохранение новой темы, переход на сайт pealim.com
'''
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import  Message

from sqlalchemy.ext.asyncio import AsyncSession
from Database import orm_get_all_words

from Auxiliaries import button
from Loggs import error_handler_func

# Words Router
words_router = Router()


'''
Обработчик команды для получения списка слов из личного словаря
'''
@words_router.message(StateFilter(None), Command("words"))
@error_handler_func
async def get_all_words(message: Message, session : AsyncSession):
    words = await orm_get_all_words(session=session, chat_id=message.chat.id) 
    
    string = ""
    for i, k in words[0].items():
        string += f"<b>{i} : {k}</b>\n\n"
    
    await message.answer(f"{string}Quantity of words in your vocabulary: <b>{words[1]}</b>", reply_markup=button(["Main menu"]))
