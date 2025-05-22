#!/usr/bin/env python3
"""Task 0
"""
import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")  # PII to redact


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """redactor function
    """
    pattern = fr'({"|".join(fields)})=.*?{re.escape(separator)}'
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}={redaction}{separator}",
        message
        )


def get_logger() -> logging.Logger:
    """Creates and returns a configured logger."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)

    return logger


def get_db():
    """Connects to a secure MySQL database using environment variables."""
    return mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main():
    """Fetch and display filtered user data from the database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    fields = [col[0] for col in cursor.description]
    logger = get_logger()

    for row in cursor:
        msg = "; ".join(
            f"{field}={value}" for field,
            value in zip(fields, row)) + ";"
        logger.info(msg)

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR
            )
        return super().format(record)


if __name__ == "__main__":
    main()
