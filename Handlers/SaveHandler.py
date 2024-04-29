from aiogram import F, Router
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
from Database.orm_query import orm_save_word, orm_get_all_words

from states import Savewords
from LOGGING.LoggerConfig import logger

from gemini import gen_def, prompt
from Handlers.defintions import button

# Save Router
sr = Router()

@sr.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello! This bot is designed for uploading and learning English words!\n\nChoose the option by the buttons below and start to learn English!\n\nYou can also use commands by menu button on the left side", reply_markup=button(text=['Учить слова', 'Учить слова по дефенициям', 'Загрузить слова']))


@sr.callback_query(F.data == 'Загрузить слова')
async def enter_eng_word_byb(call: CallbackQuery, state: FSMContext):
    await state.set_state(Savewords.English)
    await call.answer()
    await call.message.edit_text('Please, upload English word:')


@sr.message(StateFilter(None) ,Command('saveword'))
async def enter_eng_word(message: Message, state: FSMContext):
    await state.set_state(Savewords.English)
    await message.answer('Please, upload English word:')
    
    
@sr.message(StateFilter(Savewords.English), F.text)
async def enter_rus_word_orm(message: Message, state: FSMContext):
    try: 
        await state.update_data(word = message.text.lower())
        await message.answer('Now enter translation:')
        await state.set_state(Savewords.Translate)

    except Exception as e:
        logger.debug(f'у пользователя {message.from_user.username} возникла ошибка в функции enter_rus_word_orm при загрузке слова: {e}')


@sr.message(StateFilter(Savewords.Translate), F.text)
async def saveword_orm_with_translation(message: Message, state: FSMContext, session: AsyncSession):
    try:
        await state.update_data(translate = message.text.lower())
        state_data = await state.get_data()

        definition = gen_def(word=f'{state_data['word']} - {state_data['translate']}')
        prompt_ = prompt(f"{state_data['word']} - {state_data['translate']} - {definition}")

        sd = await state.update_data(definition=definition, prompt=prompt_)
        await orm_save_word(session=session, data=sd)

        await state.clear()
        await message.answer('Word has uploaded succefully!\n\n<b>Now you can learn new words!</b>\n\nJust tap the button below, or enter command /learnwords', reply_markup=button(['Учить слова']))
    except Exception as e:
        logger.debug(f'у пользователя {message.from_user.username} возникла ошибка в функции async def saveword_orm_with_translation при загрузке слова: {e}')


@sr.message(StateFilter(None) ,Command('words'))
async def enter_eng_word(message: Message, session: AsyncSession):
    words = await orm_get_all_words(session=session)
    print(words)
    await message.answer(str(words))       