# services/time_utils.py

import re
from datetime import datetime, timedelta


TIME_RANGE_PATTERN = r"(\d{1,2}(:\d{2})?\s?[APap][Mm])\s*to\s*(\d{1,2}(:\d{2})?\s?[APap][Mm])"


def parse_time_range(time_str: str):
    """
    '4:00 PM to 12:00 AM' → ('16:00', '00:00', overnight=True)
    """

    match = re.search(TIME_RANGE_PATTERN, time_str)
    if not match:
        raise ValueError("Invalid time range format")

    start_raw, _, end_raw, _ = match.groups()

    start = datetime.strptime(start_raw.upper().replace(" ", ""), "%I:%M%p")
    end = datetime.strptime(end_raw.upper().replace(" ", ""), "%I:%M%p")

    overnight = end <= start

    return (
        start.time().strftime("%H:%M"),
        end.time().strftime("%H:%M"),
        overnight,
    )
