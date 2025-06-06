#!/usr/bin/env python3
"""Task 4
"""
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """takes a string and returns bytes
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    try:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    except Exception as e:
        raise ValueError("Password hashing failed") from e


class Auth:
    """Auth class to interact with the authentication db.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with email and hashed password.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(
                email=email,
                hashed_password=hashed.decode("utf-8")
            )
