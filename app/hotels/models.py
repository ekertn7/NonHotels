"""Models of hotels objects"""

from sqlalchemy import Column, Integer, String, JSON
from app.database import Base


class Hotels(Base):
    """ORM of hotels"""

    __tablename__ = 'hotels'

    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # название отеля
    name = Column(String, nullable=False)
    # расположение отеля
    location = Column(String, nullable=False)
    # услуги в отеле
    services = Column(JSON)
    # кол-во номеров
    rooms_quantity = Column(Integer, nullable=False)
