import pytesseract
import cv2
import numpy as np
from app.services.ocr_service import perform_ocr

def extract_text(image_bytes: bytes) -> str:
    image_np = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    text = pytesseract.image_to_string(gray)
    return text

import cv2
import numpy as np

def extract_text_from_crop(image_bytes: bytes, x, y, w, h):
    image_np = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Backend failed to decode image. Format might be unsupported.")

    img_h, img_w = img.shape[:2]

    # 2. Normalize and constraint coordinates
    x1 = max(0, int(x))
    y1 = max(0, int(y))
    x2 = min(img_w, x1 + int(abs(w)))
    y2 = min(img_h, y1 + int(abs(h)))

    # 3. Check if crop is valid
    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"Invalid crop dimensions: {x1, y1, x2, y2}")

    cropped_img = img[y1:y2, x1:x2]

    # 4. Perform OCR (Example using EasyOCR)
    import easyocr
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(cropped_img, detail=0)
    
    return " ".join(results)