"""Connect to database"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import settings


# создание асинхронного движка
engine = create_async_engine(settings.postgresql_url)


# создание сессии (для совершения транзакций), AsyncSession = асинхронная сессия,
# expire_on_commit = закрывать ли сессию после коммита
session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# класс, в котором аккумулируются данные о моделях в процессе миграции
class Base(DeclarativeBase):
    """Using to accumulate models data (needs for migrations)"""
