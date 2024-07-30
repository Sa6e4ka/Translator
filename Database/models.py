from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
class Base(DeclarativeBase):
    pass


'''
Таблица с пользователями
'''
class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(32))
    chat_id: Mapped[str] = mapped_column(String(50))
    

    # Обозначение связи с таблицей слов
    words: Mapped[list["Words"]] = relationship("Words", back_populates="user")


'''
Таблица со словами
'''
class Words(Base):
    __tablename__ = 'words'

    word_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(100))
    translation: Mapped[str] = mapped_column(String(100))

# внешний ключ для присвоения каждому пользователю своего "словаря"
    # Т.е. у каждого пользователя будет свой набор слов
    user_id: Mapped[str] = mapped_column(ForeignKey("user.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="words")