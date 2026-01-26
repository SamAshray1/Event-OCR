# services/google_calendar.py

from datetime import datetime, timedelta
from urllib.parse import urlencode, quote


def create_google_calendar_link(
    title: str,
    date: str,
    start_time: str,
    end_time: str,
    location: str,
    overnight: bool = False,
) -> str:

    start_dt = datetime.fromisoformat(f"{date}T{start_time}")
    end_dt = datetime.fromisoformat(f"{date}T{end_time}")

    if overnight:
        end_dt += timedelta(days=1)

    start = start_dt.strftime("%Y%m%dT%H%M%S")
    end = end_dt.strftime("%Y%m%dT%H%M%S")

    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": f"{start}/{end}",
        "location": location,
        "details": "Created via Event-OCR",
    }

    return "https://www.google.com/calendar/render?" + urlencode(params, quote_via=quote)
