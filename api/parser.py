import json
import re


def parse_response(text: str):
    try:
        json_match = re.search(r"\{.*\}", text, re.DOTALL)

        if json_match:
            json_text = json_match.group()

            data = json.loads(json_text)

            return {
                "title": data.get("title", "Unknown Event"),
                "date": data.get("date", "January 1, 2026"),
                "time": data.get("time", "10:00 AM"),
                "location": data.get("location", "Unknown")
            }

    except Exception as e:
        print("Parsing error:", e)

    return {
        "title": "Unknown Event",
        "date": "January 1, 2026",
        "time": "10:00 AM",
        "location": "Unknown"
    }