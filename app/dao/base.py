"""Base data access object (or service or repository)"""

from sqlalchemy import select, insert
from app.database import session_maker


class BaseDAO:
    """Base data access object"""

    model = None

    @classmethod
    async def find_by_id(cls, id: int):
        """Returns one or none by id"""
        async with session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filters):
        """Returns one or none by filter"""
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, **filters):
        """Returns all by filter"""
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def insert(cls, **data):
        """Insert new values into table, returns id of added tuple"""
        async with session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result
