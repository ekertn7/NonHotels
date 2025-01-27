"""Bookings exceptions"""

from fastapi import HTTPException, status as status_codes


RoomCanNotBeBooked = HTTPException(
    status_code=status_codes.HTTP_409_CONFLICT,
    detail='Room can not be booked, there are no available rooms left',)
