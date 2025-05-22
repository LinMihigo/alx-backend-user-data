#!/usr/bin/env python3
"""Task 0
"""
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Returns the log message obsfuscated
    """
    # Find the keyword in fields
    # Then change what's btn = and ; after the keyword
    strings = message.split(separator)[:-1]
    newstring = []

    for s in strings:
        for f in fields:
            if s.startswith(f):
                s = s[:s.index('=') + 1] + redaction
        newstring.append(s)
    return separator.join(newstring) + separator
