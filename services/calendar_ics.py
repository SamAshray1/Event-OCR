from ics import Calendar, Event
from app.models.event import EventResponse
from datetime import timedelta

def generate_ics(event: EventResponse) -> str:
    c = Calendar()
    e = Event()
    e.name = event.title
    e.begin = event.start_time
    e.end = event.start_time + timedelta(hours=2)
    e.location = event.location or ""

    c.events.add(e)

    file_path = f"/tmp/{event.title.replace(' ', '_')}.ics"
    with open(file_path, "w") as f:
        f.writelines(c)

    return file_path
