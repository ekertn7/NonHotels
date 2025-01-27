"""Main app"""

from datetime import date
from typing import Optional
from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings


app = FastAPI()


app.include_router(router_users)
app.include_router(router_bookings)


# class SearchHotelsArgs:
#     def __init__(
#             self,
#             location: str,
#             date_from: date,
#             date_to: date,
#             stars: Optional[int] = Query(None, ge=1, le=5),
#             has_spa: Optional[bool] = None):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.stars = stars
#         self.has_spa = has_spa


# class SchemaHotel(BaseModel):
#     address: str
#     name: str
#     stars: int


# class SchemaBooking(BaseModel):
#     hotel_id: int
#     room_id: int
#     date_from: date
#     date_to: date


# @app.get('/hotels')
# def search_hotels(args: SearchHotelsArgs = Depends()):
#     """Filter by hotels"""
#     hotels = ['Hotel Beach Resort', 'Hotel Kerpeach Resort']


# @app.post('/booking')
# def add_booking(booking: SchemaBooking):
#     """
#     Параметры передаются не в url запроса, а в теле запроса
#     post = изменение системы с целью добавить в нее что-то (бронь, емаил)
#     post = передача чувствительных данных
#     """
