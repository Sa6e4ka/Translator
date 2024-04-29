from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text

class Base(DeclarativeBase):
    pass

class words(Base):
    __tablename__ = 'words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(Text(200))
    translate: Mapped[str] = mapped_column(Text(200))
    defenition: Mapped[str] = mapped_column(Text(500))
    prompt: Mapped[str] = mapped_column(Text(500))
    
