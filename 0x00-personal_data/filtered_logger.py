#!/usr/bin/env python3
"""Task 0
"""
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ):
    """Returns the log message obsfuscated
    """
    # Find the keyword in fields
    # Then change what's btn = and ; after the keyword
    list = message.split(separator)[:-1]

    for l in list:
        for f in fields:
            if l.startswith(f):
                