# services/event_parser.py

import re
from datetime import datetime
from typing import Dict, Optional


DATE_PATTERNS = [
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",       # 12/03/2026
    r"\b\d{4}-\d{2}-\d{2}\b",                   # 2026-03-12
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?",
]

TIME_PATTERN = r"\b\d{1,2}(:\d{2})?\s?(AM|PM|am|pm)\b"


def _extract_date(text: str) -> Optional[str]:
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            try:
                dt = datetime.strptime(match.group(), "%Y-%m-%d")
                return dt.date().isoformat()
            except Exception:
                pass
    return None


def _extract_time(text: str) -> Optional[str]:
    match = re.search(TIME_PATTERN, text)
    if not match:
        return None

    time_str = match.group().upper().replace(" ", "")
    try:
        return datetime.strptime(time_str, "%I:%M%p").time().strftime("%H:%M")
    except ValueError:
        return datetime.strptime(time_str, "%I%p").time().strftime("%H:%M")


def _extract_location(text: str) -> Optional[str]:
    lines = text.splitlines()
    for line in lines:
        if any(k in line.lower() for k in ["street", "st", "road", "rd", "avenue", "ave", "hall", "center"]):
            return line.strip()
    return None


def parse_event_from_text(text: str) -> Dict[str, str]:
    """
    Convert raw OCR/VLM output into structured event data
    """

    lines = [l.strip() for l in text.splitlines() if l.strip()]

    title = lines[0] if lines else "Untitled Event"

    date = _extract_date(text) or ""
    time = _extract_time(text) or ""
    location = _extract_location(text) or ""

    return {
        "title": title,
        "date": date,
        "time": time,
        "location": location,
    }
