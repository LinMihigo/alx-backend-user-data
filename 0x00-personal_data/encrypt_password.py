#!/usr/bin/env python3
"""Task 5
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with a salt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
