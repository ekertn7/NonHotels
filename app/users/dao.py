"""Data access object for users"""

from app.dao.base import BaseDAO
from app.users.models import Users


class UsersDAO(BaseDAO):
    """Data access object for users"""

    model = Users
