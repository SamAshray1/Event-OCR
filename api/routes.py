from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from app.services.ocr_service_old import extract_text
from app.services.nlp_service import parse_event
from app.models.event import EventResponse
from app.services.calendar_ics import generate_ics

router = APIRouter(prefix="/api")

@router.get("/upload", response_class=HTMLResponse)
def upload_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Invite Upload</title>
    </head>
    <body>
        <h2>Upload Invitation Image</h2>
        <form action="/api/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required />
            <br><br>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """

@router.post("/upload", response_model=EventResponse)
async def upload_invite(file: UploadFile = File(...)):
    text = extract_text(await file.read())
    # event = parse_event(text)
    return text

@router.post("/calendar/ics")
async def create_ics(event: EventResponse):
    path = generate_ics(event)
    return {"ics_file": path}
