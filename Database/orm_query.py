from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import words
from LOGGING.LoggerConfig import logger


async def orm_save_word(data : dict, session : AsyncSession):
    try:
        querry = select(words).where(words.word == data['word']).order_by(words.id.desc()).limit(1)
        result = await session.execute(querry)
        word = result.scalars().first()

        if word:
            await session.execute(update(words).where(words.word == data['word']).values(translate = data['translate'], defenition = data['definition'], prompt=data['prompt']))
            await session.commit()
        else: 
            objects = words(
                word = data['word'],
                translate = data['translate'],
                defenition = data['definition'], 
                prompt = data['prompt']
            )
            session.add(objects)
            await session.commit()
    except Exception as e:
                logger.debug(f'возникла ошибка в функции orm_save_word: {e}')


async def orm_get_rand_word(session: AsyncSession):
    querry = select(words).order_by(func.random()).limit(1)

    result = await session.execute(querry)
    scl = result.scalars().first()

    word = scl.word
    translate = scl.translate
    return word, translate


async def orm_get_all_words(session : AsyncSession):
    query = select(words).column(words.word)
    result = await session.execute(query)

    words_list = [row[1] for row in result.fetchall()]
    return words_list


async def orm_delete_word(session : AsyncSession, data):
    query = delete(words).where(words.word == data['word'])
    await session.execute(query)
    await session.commit()

async def orm_get_def(session : AsyncSession):
    query = select(words).order_by(func.random()).limit(1)
    result = await session.execute(query)
    scl = result.scalars().first()

    return scl.word,  scl.defenition

async def orm_get_prompt(session : AsyncSession, data : dict):
    query = select(words).where(words.word == data['word']).order_by(func.random()).limit(1)
    result = await session.execute(query)
    scl = result.scalars().first()
    
    return scl.prompt


