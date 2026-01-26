# services/event_parser.py

import json
from typing import Dict


def parse_event_from_json_string(event_json_str: str) -> Dict[str, str]:
    """
    Accepts a JSON string and returns structured event fields
    Expected JSON format:
    {
        "title": "...",
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "location": "..."
    }
    """

    try:
        data = json.loads(event_json_str)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON string passed to event parser")

    return {
        "title": data.get("title", "").strip(),
        "date": data.get("date", "").strip(),
        "time": data.get("time", "").strip(),
        "location": data.get("location", "").strip(),
    }
