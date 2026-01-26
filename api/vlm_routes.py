from fastapi import APIRouter, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from services.date_utils import parse_human_date
from services.time_utils import parse_time_range
from services.vision_service import (
    extract_event_vlm,
    extract_from_crop_vlm
)
from services.event_parser import parse_event_from_json_string
from services.google_calendar import create_google_calendar_link

import json

router = APIRouter(prefix="/vlm")
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_vlm_page(request: Request):
    """Serve the specialized VLM extraction page"""
    return templates.TemplateResponse("vlm.html", {"request": request})


@router.post("/process")
async def process_vlm(
    file: UploadFile = File(...),
    box: str | None = None
):
    """
    Handles both full image and cropped image processing using VLM.
    Then parses the result and generates a Google Calendar event link.
    """
    content = await file.read()

    # ---- VLM extraction ----
    if box:
        coords = json.loads(box)
        vlm_output = extract_from_crop_vlm(
            content,
            coords["x"],
            coords["y"],
            coords["w"],
            coords["h"],
        )
    else:
        vlm_output = extract_event_vlm(content)

    print("VLM out:", vlm_output)
    print("Start parsing")

    event = parse_event_from_json_string(vlm_output)
    # event = { title, date, time, location }

    print(event)
    print("Start gcal link")

    date_iso = parse_human_date(event["date"])
    start, end, overnight = parse_time_range(event["time"])

    gcal_link = create_google_calendar_link(
        title=event["title"],
        date=date_iso,
        start_time=start,
        end_time=end,
        location=event["location"],
        overnight=overnight,
    )

    return {
        "raw_vlm_output": vlm_output,
        "parsed_event": event,
        "google_calendar_link": gcal_link,
    }
