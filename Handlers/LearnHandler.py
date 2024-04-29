from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import  Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
from Database.orm_query import orm_get_rand_word

from states import Learn
from LOGGING.LoggerConfig import logger
from Handlers.defintions import button


# Learn Router
lr = Router()

@lr.message(StateFilter('*'), F.text == '/stop')
async def stop(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Урок окончен! 😁')

@lr.callback_query(StateFilter('*'), F.data == 'Учить слова')
async def learn_byb(call: CallbackQuery, state: FSMContext, session : AsyncSession):
    try:
        await state.set_state(Learn.Translate)
        await call.message.edit_text('Сейчас тебе отправится слово на Английском и ты должен(на) будешь записать его перевод на Русском.\n\nЕсли перевод будет неверным, то придется ввести его еще раз\n\nЕсли перевод верный, то тебе будет предложено следующее слово.\n\n<b>И так до тех пор, пока ты не нажмешь кнопку</b>')
        await sleep(5)

        word = await orm_get_rand_word(session=session)
        await call.message.answer(text=f"Word:<b>\n\n{word[0]}</b>\n\nNow enter it's translation:", reply_markup=button(text=['Остановить урок']))
        await state.update_data(Translate = word[1])
    except Exception as e:
        logger.debug(f'У пользователя {call.message.from_user.username} возникла ошибка в функции learn: {e}')


@lr.message(StateFilter(None), Command('learnwords'))
async def learn(message: Message, session: AsyncSession, state: FSMContext):
    try:
        await state.set_state(Learn.Translate)
        await message.answer('Сейчас тебе отправится слово на Английском и ты должен(на) будешь записать его перевод на Русском.\n\nЕсли перевод будет неверным, то придется ввести его еще раз\n\nЕсли перевод верный, то тебе будет предложено следующее слово.\n\n<b>И так до тех пор, пока ты не нажмешь кнопку</b>')
        await sleep(5)

        word = await orm_get_rand_word(session=session)
        await message.answer(text=f"Word:<b>\n\n{word[0]}</b>\n\nNow enter it's translation:", reply_markup=button(text=['Остановить урок']))
        await state.update_data(Translate = word[1])
    except Exception as e:
        logger.debug(f'У пользователя {message.from_user.username} возникла ошибка в функции learn: {e}')


@lr.message(StateFilter(Learn.Translate), F.text)
async def check(message: Message, state: FSMContext, session: AsyncSession):
    try:  
        state_data = await state.get_data()
        if message.text.lower() == state_data["Translate"]:
            await message.answer("<b>True!</b> 🥳\n\nLet's learn next word!")
            
            await sleep(1)

            word = await orm_get_rand_word(session=session)
            await message.answer(text=f"Word:\n\n<b>{word[0]}</b>\n\nNow enter it's translation:", reply_markup=button(text=['Остановить урок']))
            await state.update_data(Translate = word[1])
        else:
            await message.answer('<b>False!</b>  😨\n\nTry one more time!', reply_markup=button(['Пропустить']))
    except Exception as e:
        logger.debug(f'У пользователя {message.from_user.username} возникла ошибка при вводе перевода слова в функции check: {e}')


@lr.callback_query(StateFilter('*'), F.data == 'Пропустить')
async def skip(call : CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.answer()
    word = await orm_get_rand_word(session=session)
    await call.message.edit_text(text=f"Word:\n\n<b>{word[0]}</b>\n\nNow enter it's translation:", reply_markup=button(text=['Остановить урок']))
    await state.update_data(Translate = word[1])