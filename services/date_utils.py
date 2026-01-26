# services/date_utils.py

from datetime import datetime


def parse_human_date(date_str: str) -> str:
    """
    Converts 'Saturday 23 December' → 'YYYY-MM-DD'
    Assumes next occurrence if year is missing
    """

    today = datetime.today()
    parsed = datetime.strptime(date_str, "%A %d %B")
    parsed = parsed.replace(year=today.year)

    if parsed.date() < today.date():
        parsed = parsed.replace(year=today.year + 1)

    return parsed.date().isoformat()
