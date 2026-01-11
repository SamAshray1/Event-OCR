import re
from dateparser.search import search_dates
from models.event import EventResponse

def extract_title(lines):
    for line in lines:
        if not re.search(r'\d', line):
            return line
    return lines[0] if lines else "Untitled Event"

def extract_location(text):
    match = re.search(r'at (.+)', text, re.IGNORECASE)
    return match.group(1) if match else None

def parse_event(text: str) -> EventResponse:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    dates = search_dates(text)

    start_time = dates[0][1] if dates else None
    title = extract_title(lines)
    location = extract_location(text)

    return EventResponse(
        title=title,
        start_time=start_time,
        location=location,
        raw_text=text
    )
