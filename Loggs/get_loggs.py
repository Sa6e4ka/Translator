'''
Отправка логов по команде
'''
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import  Message, FSInputFile
from Auxiliaries import button
from .error_hadler import error_handler_func

#Logging Router
logging_router = Router() 


'''
Обработчик команды для отправки логов
'''
@logging_router.message(Command("loggs"))
@error_handler_func
async def send_to_channel(message: Message):
      file_info = FSInputFile("Loggs/debug.log")
      await message.answer_document(document=file_info, caption="Last loggs:", reply_markup=button(["Main menu"]))



