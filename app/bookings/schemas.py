"""Schemas for bookings"""

from datetime import date
from pydantic import BaseModel


class BookingsSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_check_in: date
    date_check_out: date
    cost_at_time: int
    total_days: int
    total_cost: int
