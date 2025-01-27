"""Models of bookings objects"""

from sqlalchemy import Column, Integer, ForeignKey, Date, Computed
from app.database import Base


class Bookings(Base):
    """ORM of bookings"""

    __tablename__ = 'bookings'

    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # внешний ключ на комнаты
    room_id = Column(ForeignKey('rooms.id'), nullable=False)
    # внешний ключ на пользователей
    user_id = Column(ForeignKey('users.id'), nullable=False)
    # дата заселения
    date_check_in = Column(Date, nullable=False)
    # дата выселения
    date_check_out = Column(Date, nullable=False)
    # стоимость за ночь на момент бронирования
    cost_at_time = Column(Integer, nullable=False)
    # общее кол-во дней
    total_days = Column(Integer, Computed('date_check_out - date_check_in'))
    # общая стоимость
    total_cost = Column(Integer, Computed('(date_check_out - date_check_in) * cost_at_time'))
