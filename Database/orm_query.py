from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import Words, User
from Loggs import logger


'''
Функция для получения id пользователя
'''
async def orm_get_user_id(session: AsyncSession, chat_id) -> str:
    user_query = select(User.user_id).where(User.chat_id == chat_id)
    user_result  = await session.execute(user_query)
    return user_result.scalars().first()


'''
Функция orm_add_user для добавления пользователя в базу данных
'''
async def orm_add_user(session: AsyncSession, username: str, chat_id: str) -> bool: 
# Проверка на наличие пользователя в базе при вводе команды регистарции
   
    query = select(User).where(User.chat_id == chat_id)
    result = await session.execute(query)

    if result.scalars().first(): 
        logger.info(f"Пользователь {username} попытался зарегистрироваться повторно") 
        return 
    
# Добавление нового пользователя в случае его отсутствия в базе
    user = User(
        username = username,
        chat_id = chat_id
    )

    session.add(user)
    await session.commit()


'''
Функция сохранения слов в личный словарь пользователей
'''
async def orm_save_word(data : dict, session : AsyncSession) -> None:
# Получение id пользователя 
    id = await orm_get_user_id(session=session, chat_id=data["chat_id"])

# Запрос на выборку слова из таблицы
    querry = (
        select(Words.word)
            .where(
                Words.word == data['word'], 
                Words.user_id == id
            )
            .limit(1)
    )

    result = await session.execute(querry)

# Проверка наличия слова в таблице
    if result.scalars().first():

    # Если слово в таблице имеется, то обновляем данные о нем (само слово и перевод)
        update_query = (
            update(Words)
                .where(
                    Words.word == data['word']
                )
                .values(
                    translation = data['translation']
                )
        )
    
        await session.execute(update_query)
        await session.commit()
    
# Сохраняем новое слово, его перевод и юзера в таблицу
    objects = Words(
        word = data['word'],
        translation = data['translation'],
        user_id = id
    )

    session.add(objects)
    await session.commit()


'''
Функция для получения случайного слова из таблицы пользователя
'''
async def orm_get_rand_personal_word(session: AsyncSession, chat_id : str) -> list:
# Получение id пользователя
    id = await orm_get_user_id(session=session, chat_id=chat_id)

# Сортировка слов в случайном порядке и выборка одного элемента
    querry = (
        select(Words)
            .where(
                Words.user_id == id
            )
            .order_by(
                func.random()
            )
            .limit(1)
    )
    
    result = await session.execute(querry)
    scl = result.scalars().first()

# возврат списка со словом и его переводом
    return scl.word, scl.translation



'''
Функция для получения списка слов для пользователя
'''
async def orm_get_all_words(session : AsyncSession, chat_id : str) -> list:

# Получение Id пользователя
    id = await orm_get_user_id(session=session, chat_id=chat_id)

# Получение списка слов
    query_words_list = (
        select(
            Words.word, 
            Words.translation
        )
            .where(
                Words.user_id == id
            )
            .order_by(Words.word.asc())
    )

    result = await session.execute(query_words_list)

    word_list = {row[0]: row[1] for row in result.fetchall()}

# Получения количества слов в списке пользователя
    query_count_words = select(func.count(Words.word)).where(Words.user_id == id)
    count_result = await session.execute(query_count_words)
    quantity = count_result.scalar_one()

    
    return word_list, quantity


'''
Функция удаления слова
'''
async def orm_delete_word(session : AsyncSession, word, chat_id) -> None:
# Получение id Пользователя
    id = await orm_get_user_id(session=session, chat_id=chat_id)

    query = (
        select(Words.word)
            .where(
                Words.word == word, 
                Words.user_id == id
            )
    )
    result = await session.execute(query)

    if result.scalars().first():
    # Запрос удаления слова
        query = (
            delete(Words)
                .where(
                    Words.word == word, 
                    Words.user_id == id
                )
        )
        await session.execute(query)
        await session.commit()
        return
    return "It seems like you don't have this word in your vocabulary yet 😨"