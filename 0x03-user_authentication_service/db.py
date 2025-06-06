#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments
        """
        if not kwargs:
            raise InvalidRequestError("No search criteria provided")

        query = self._session.query(User)

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid field: {key}")
            query = query.filter(getattr(User, key) == value)

        result = query.first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user by id with given attributes
        """
        invalid_fields = [key for key in kwargs if not hasattr(User, key)]

        if invalid_fields:
            raise ValueError(f"Invalid fields: {', '.join(invalid_fields)}")

        update_dict = {
            getattr(User, key): value for key, value in kwargs.items()
            }
        updated_rows = self._session.query(User).filter(User.id == user_id)\
            .update(
            update_dict,
            synchronize_session=False
        )

        if updated_rows == 0:
            raise NoResultFound(f"User with id {user_id} not found")

        self._session.commit()
