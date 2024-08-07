#Импортируем нужные дополнительные модули
import os
import asyncio
from Loggs import logger, logging_router

# Импортируем нужные модули из aiogram
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import BotCommandScopeAllPrivateChats, Message
from aiogram.client.default import DefaultBotProperties

#Достаем токен бота и url базы данных из переменной окружения
from dotenv import load_dotenv
load_dotenv()

# Имопртируем функцию создания базы данных
try:
    from Database.engine import create_db, session_maker
except Exception as e:
    logger.error(f'Ошибка в запросе к sql: {e}')

#Из папки handlers импортируем все хендлеры 
from Handlers import (
    delete_router,
    words_router,
    learn_router,
    start_router,
    save_personal_router
)

# Импортируем команды
from Auxiliaries import private


#Создаем объект бота (передаем ему режим парсига получаемых ответов)
bot= Bot(token="6479697379:AAEH12a_YKMxPV-ADTy3esucoVc9YPVJf5A", default=DefaultBotProperties(parse_mode='HTML'))
#Создаем объект диспетчера
dp = Dispatcher()

# Добавляем Middlewares 
    # Чтобы использовать не одно конкретное событие, а любое можно заменить message на update
from Auxiliaries.middleware import DataBaseSession

#Подключаем к диспетчеру все роутеры из содаваемых хендлеров.   
dp.include_routers(delete_router, words_router, learn_router, start_router, save_personal_router, logging_router) 


# Добавляем основные "глобальные" хендлеры
@dp.message(Command('state'))
async def state_get(message: Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(
        text=f'Текущее состояние: {current_state}'
    )


# Команда очистки состояния
@dp.message(Command('stateclear'))
async def clear_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    await state.clear()
    clear_state = await state.get_state()
    await message.answer(f'Состояние <b>{current_state}</b> сменилось на <b>{clear_state}</b>')


#Запускаем бота, помещаем доступные апдейты в start_polling
# отключаем обработку незавершившихся запросов
# Подключаем базу данных
async def main():
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private,scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot,allowed_updates=dp.resolve_used_update_types())


# Запуск main
if __name__ == "__main__":
    try:   
        logger.info(f"Бот успешно запущен по ссылке: {os.environ.get("BOT_LINK")}")
        asyncio.run(main())
    except KeyboardInterrupt:   
        logger.error('Бот остановлен')
        pass
    except Exception as e:  
        logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: {e}')