from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from app.services.ocr_service import perform_ocr
from app.services.nlp_service import parse_event
from app.models.event import EventResponse
from app.services.calendar_ics import generate_ics

router = APIRouter(prefix="/api")

@router.get("/upload", response_class=HTMLResponse)
def upload_page():
    return """
    <html>
        <body>
            <h2>Upload Event Invitation</h2>
            <form action="/api/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*">
                <button type="submit">Extract Event</button>
            </form>
        </body>
    </html>
    """

@router.post("/upload", response_model=EventResponse)
async def upload_invite(file: UploadFile = File(...)):
    # 1. Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        # 2. Extract raw text via OCR
        image_content = await file.read()
        ocr_data = perform_ocr(image_content)
        
        # 3. Parse text into structured event using NLP service
        # We pass the OCR text to your NLP logic
        event_data = parse_event(ocr_data["body_text"])
        
        # Override title if OCR found a high-confidence title
        if ocr_data["title"] and not event_data.title:
            event_data.title = ocr_data["title"]

        return event_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@router.post("/calendar/ics")
async def create_ics(event: EventResponse):
    try:
        path = generate_ics(event)
        return {"ics_file": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ICS generation failed: {str(e)}")