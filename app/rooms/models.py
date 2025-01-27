"""Models of rooms objects"""

from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from app.database import Base


class Rooms(Base):
    """ORM of rooms"""

    __tablename__ = 'rooms'

    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # внешний ключ на отели
    hotel_id = Column(ForeignKey('hotels.id'), nullable=False)
    # название номера
    name = Column(String, nullable=False)
    # описание номера
    description = Column(String, nullable=False)
    # стоимость номера
    cost = Column(Integer, nullable=False)
    # услуги в номере
    services = Column(JSON)
    # кол-во номеров (TODO: надо удалить)
    quantity = Column(Integer, nullable=False)
