"""Router for bookings"""

from datetime import date
from fastapi import APIRouter, Depends

from app.bookings.dao import BookingsDAO
from app.bookings.schemas import BookingsSchema
from app.users.models import Users
from app.users.dependencies import get_current_user

from app.exceptions.bookings_exceptions import RoomCanNotBeBooked


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования'],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[BookingsSchema]:
    result = await BookingsDAO.find_all(user_id=user.id)
    return result


@router.post('/check')
async def check_availability(
        room_id: int, date_check_in: date, date_check_out: date,
        user: Users = Depends(get_current_user)):
    """Endpoint to check rooms availability"""

    if date_check_in >= date_check_out:
        raise RoomCanNotBeBooked

    return await BookingsDAO.check_room_availability(
        user_id=user.id, room_id=room_id, date_check_in=date_check_in,
        date_check_out=date_check_out)


@router.post('/add')
async def add_booking(
        room_id: int, date_check_in: date, date_check_out: date,
        user: Users = Depends(get_current_user)):
    """Endpoint to add booking"""

    if date_check_in >= date_check_out:
        raise RoomCanNotBeBooked

    result = await BookingsDAO.add_booking(
        user_id=user.id, room_id=room_id, date_check_in=date_check_in,
        date_check_out=date_check_out)
    if result is None:
        raise RoomCanNotBeBooked
    return result
