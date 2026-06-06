from urllib.parse import urlencode
from datetime import datetime


def create_google_calendar_link(event):
    try:
        start = datetime.strptime(
            f"{event['date']} {event['time']}",
            "%B %d, %Y %I:%M %p"
        )
    except:
        start = datetime.now()

    end = start

    params = {
        "action": "TEMPLATE",
        "text": event["title"],
        "dates": f"{start.strftime('%Y%m%dT%H%M%S')}/{end.strftime('%Y%m%dT%H%M%S')}",
        "location": event["location"],
        "details": "Generated from AI Event Recognition App"
    }

    return "https://calendar.google.com/calendar/render?" + urlencode(params)