import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from app.services.ocr_service import perform_ocr
from app.services.nlp_service import parse_event
from app.models.event import EventResponse
from app.services.calendar_ics import generate_ics
from fastapi import Form
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.services.ocr_service_old import extract_text_from_crop


app = FastAPI()

# Setup templates directory
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/api")

@router.get("/upload", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.post("/upload", response_model=EventResponse)
async def upload_invite(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        image_content = await file.read()
        ocr_data = perform_ocr(image_content)
        
        event_data = parse_event(ocr_data["body_text"])
        
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
    
router2 = APIRouter(prefix="/api2")

@router2.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@router2.post("/upload-crop")
async def upload_crop(file: UploadFile = File(...), box: str = Form(...)):
    try:
        coords = json.loads(box)
        image_content = await file.read()
        
        extracted_text = extract_text_from_crop(
            image_content, 
            coords['x'], coords['y'], coords['w'], coords['h']
        )
        
        return parse_event(extracted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))