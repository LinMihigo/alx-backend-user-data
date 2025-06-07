#!/usr/bin/env python3
"""Task 4
"""
from db import DB
import bcrypt
import uuid
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


def _hash_password(password: str) -> bytes:
    """takes a string and returns bytes
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    try:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    except Exception as e:
        raise ValueError("Password hashing failed") from e


def _generate_uuid() -> str:
    """Generate a new UUID and return it as a string"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password.encode("utf-8"),
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> Optional[str]:
        """Create a session ID for the user and store it in DB
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """Return the user corresponding to the given session_id"""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user's session by setting session_id to None"""
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for a user."""
        user = self._db.find_user_by(email=email)
        if user is None:
            raise ValueError("User not found")

        token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password using a valid reset token."""
        if not reset_token or not password:
            raise ValueError("Missing token or password")

        user = self._db.find_user_by(reset_token=reset_token)
        if user is None:
            raise ValueError("Invalid reset token")

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self._db.update_user(
            user.id,
            hashed_password=hashed_pw,
            reset_token=None
        )
