"""Data access object for bookings"""

from datetime import date
from sqlalchemy import select, and_, or_, func

from app.database import session_maker
from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.rooms.models import Rooms


class BookingsDAO(BaseDAO):
    """Data access object for bookings"""

    model = Bookings

    @staticmethod
    def _query_available_rooms(
            choised_room_id: int, choised_date_check_in: date,
            choised_date_check_out: date):
        """Checking availability of rooms for selected dates

                  |                             |
        choised_date_check_in         choised_date_check_out
                  |                             |
                  |        [--------------------|-------->
                  |                             |
        [---------|-----------------------------|-------->
                  |                             |

        WITH booked_rooms AS (
            SELECT *
            FROM bookings
            WHERE
                room_id = `choised_room_id`
                AND
                (
                    date_check_in >= `choised_date_check_in`
                    AND
                    date_check_in <= `choised_date_check_out`
                )
                OR
                (
                    date_check_in <= `choised_date_check_in`
                    AND
                    date_check_out >= `choised_date_check_in`
                )
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) as available_rooms FROM rooms
        LEFT JOIN booked_rooms
        ON rooms.id = booked_rooms.room_id
        WHERE rooms.id = `choised_room_id`
        GROUP BY rooms.quantity, booked_rooms.room_id;
        """
        cte_booked_rooms = \
            select(Bookings).where(
                and_(
                    Bookings.room_id == choised_room_id,
                    or_(
                        and_(
                            Bookings.date_check_in >= choised_date_check_in,
                            Bookings.date_check_in <= choised_date_check_out
                        ),
                        and_(
                            Bookings.date_check_in <= choised_date_check_in,
                            Bookings.date_check_out >= choised_date_check_in
                        ),
                    )
                )
            ).cte('booked_rooms')

        query_available_rooms = \
            select(
                (Rooms.quantity - func.count(cte_booked_rooms.c.room_id)).label('available_rooms')
            ).select_from(Rooms).join(
                cte_booked_rooms, cte_booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(
                Rooms.id == choised_room_id
            ).group_by(
                Rooms.quantity, cte_booked_rooms.c.room_id)

        return query_available_rooms


    @staticmethod
    def _query_room_cost(choised_room_id: int):
        query_room_cost = \
            select(
                Rooms.cost
            ).select_from(Rooms).where(Rooms.id == choised_room_id)

        return query_room_cost


    @classmethod
    async def check_room_availability(
            cls, user_id: int, room_id: int, date_check_in: date,
            date_check_out: date):
        """Checking availability of rooms for selected dates"""

        query_available_rooms = cls._query_available_rooms(room_id, date_check_in, date_check_out)
        query_room_cost = cls._query_room_cost(room_id)

        async with session_maker() as session:
            result_available_rooms = await session.execute(query_available_rooms)

            available_rooms: int = result_available_rooms.scalar()

            if available_rooms > 0:
                result_room_cost = await session.execute(query_room_cost)

                room_cost: int = result_room_cost.scalar()
                rest_period: int = (date_check_out - date_check_in).days
                rest_cost: int = room_cost * rest_period

                return {
                    'available_rooms': available_rooms,
                    'room_cost': room_cost,
                    'rest_period': rest_period,
                    'rest_cost': rest_cost}

            return None


    @classmethod
    async def add_booking(
            cls, user_id: int, room_id: int, date_check_in: date,
            date_check_out: date):
        """Adds booking

        TODO Checking of season coefficient:

        season_coefficients = {
            '2025-01-01': 1.11, '2025-01-02': 1.08,
            '2025-01-03': 1.01, '2025-01-04': 0.99, ...}
        dates = ['2025-01-01', '2025-01-02']

        rest_cost = sum(season_coefficients[date] * room_cost for date in dates)

        TODO Checking of individual user discount

        user_status = 'VIP'
        user_coefficient = 0.97

        rest_cost = user_coefficient * final_cost

        на фронтенде написать цена до персональной скидки и цена после

        TODO Checking of promocodes

        promocode = '38490jdfvi9jrt2'
        promocode_coefficient = 0.94

        rest_cost = promocode_coefficient * final_cost

        предусмотреть истекание промокода

        TODO Checking that user has not booked other rooms for the selected dates
        """

        query_available_rooms = cls._query_available_rooms(room_id, date_check_in, date_check_out)
        query_room_cost = cls._query_room_cost(room_id)

        async with session_maker() as session:
            result_available_rooms = await session.execute(query_available_rooms)

            available_rooms: int = result_available_rooms.scalar()

            if available_rooms > 0:
                result_room_cost = await session.execute(query_room_cost)

                room_cost: int = result_room_cost.scalar()
                rest_period: int = (date_check_out - date_check_in).days
                rest_cost: int = room_cost * rest_period

                await cls.insert(
                    room_id=room_id,
                    user_id=user_id,
                    date_check_in=date_check_in,
                    date_check_out=date_check_out,
                    cost_at_time=room_cost,
                )

                return {
                    'available_rooms': available_rooms,
                    'room_cost': room_cost,
                    'rest_period': rest_period,
                    'rest_cost': rest_cost}

            return None
