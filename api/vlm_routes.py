from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.templating import Jinja2Templates
from services.vision_service_new import extract_event_with_vlm, extract_from_crop_vlm
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/vlm")
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_vlm_page(request: Request):
    """Serve the specialized VLM extraction page"""
    return templates.TemplateResponse("vlm.html", {"request": request})

@router.post("/process")
async def process_vlm(file: UploadFile = File(...), box: str = None):
    """
    Handles both full image and cropped image processing using VLM.
    If 'box' is provided, it crops first.
    """
    content = await file.read()
    
    if box:
        import json
        coords = json.loads(box)
        # Targeted recognition
        result_text = extract_from_crop_vlm(
            content, coords['x'], coords['y'], coords['w'], coords['h']
        )
    else:
        # Full smart recognition
        result_text = extract_event_with_vlm(content)
        
    return {"raw_vlm_output": result_text}