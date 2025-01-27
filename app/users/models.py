"""Models of users objects"""

from sqlalchemy import Column, String, Integer, Date
from app.database import Base


class Users(Base):
    """ORM of users"""

    __tablename__ = 'users'

    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # имя
    first_name = Column(String, nullable=False)
    # фамилия
    second_name = Column(String)
    # отчество
    middle_name = Column(String)
    # дата рождения
    birth = Column(Date, nullable=False)
    # почта
    email = Column(String, nullable=False)
    # захешированный пароль (TODO: надо перенести в другую таблицу)
    hashed_password = Column(String, nullable=False)
