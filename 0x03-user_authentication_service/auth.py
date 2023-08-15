#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar(User):
        """Creates a user if not existing"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            password = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=password)
            return user
        else:
            raise ValueError("User {} already exists".format(email))
