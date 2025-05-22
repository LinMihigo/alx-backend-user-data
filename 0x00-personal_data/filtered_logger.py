#!/usr/bin/env python3
"""Task 0
"""
import re
from typing import List


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
