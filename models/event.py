from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventResponse(BaseModel):
    title: str
    start_time: Optional[datetime]
    location: Optional[str]
    raw_text: str
