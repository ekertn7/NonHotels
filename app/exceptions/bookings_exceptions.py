"""Bookings exceptions"""

from fastapi import HTTPException, status as status_codes


NoAvailableRoomsLeftException = HTTPException(
    status_code=status_codes.HTTP_409_CONFLICT,
    detail='There are no available rooms left',)


WrongDatesIntervalException = HTTPException(
    status_code=status_codes.HTTP_409_CONFLICT,
    detail='Wrong dates interval',)
