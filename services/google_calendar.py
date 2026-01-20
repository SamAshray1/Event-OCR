# services/google_calendar.py

from datetime import datetime, timedelta
from urllib.parse import urlencode, quote


def _format_datetime(date: str, time: str) -> datetime:
    return datetime.fromisoformat(f"{date}T{time}")


def create_google_calendar_link(
    title: str,
    date: str,
    time: str,
    location: str,
    duration_minutes: int = 60,
) -> str:
    """
    Generates a Google Calendar event creation link
    """

    if not date or not time:
        return ""

    start_dt = _format_datetime(date, time)
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    start = start_dt.strftime("%Y%m%dT%H%M%S")
    end = end_dt.strftime("%Y%m%dT%H%M%S")

    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": f"{start}/{end}",
        "location": location,
        "details": "Created via Event-OCR",
    }

    return (
        "https://www.google.com/calendar/render?"
        + urlencode(params, quote_via=quote)
    )
