from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

import shutil
import os

from api.model import ask_model
from api.parser import parse_response
from api.calendar import create_google_calendar_link

app = FastAPI()

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ask AI model
    raw_response = ask_model(file_path)

    # Parse response
    event = parse_response(raw_response)

    # Create Google Calendar link
    calendar_link = create_google_calendar_link(event)

    return JSONResponse({
        "event": event,
        "calendar_link": calendar_link,
        "raw_model_output": raw_response
    })