#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
import uuid
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    return hashed


def _generate_uuid() -> str:
    """Return a string representation of uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar(User):
        """Creates a user if not existing"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except (NoResultFound, InvalidRequestError):
            password = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation"""
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode()

            if bcrypt.checkpw(password, user.hashed_password):
                return True
        except (NoResultFound, InvalidRequestError):
            return False
        else:
            return False
