import pytesseract
import cv2
import numpy as np
import easyocr
from typing import Dict, Any

# Initialize EasyOCR once (global scope or within a class)
easyocr_reader = easyocr.Reader(['en'], gpu=False)

OCR_CONFIGS = ["--oem 3 --psm 6", "--oem 3 --psm 11", "--oem 3 --psm 4"]

def preprocess_variants(img: np.ndarray):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variants = [
        gray,
        cv2.GaussianBlur(gray, (5, 5), 0),
        cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    ]
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    variants.append(otsu)
    return variants

def ocr_with_bboxes(image: np.ndarray, config: str) -> Dict[str, Any]:
    data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DICT)
    text_blocks, confidences = [], []
    
    for i in range(len(data["text"])):
        txt = data["text"][i].strip()
        conf = int(data["conf"][i])
        if txt and conf > 0:
            text_blocks.append(txt)
            confidences.append(conf)
            
    full_text = " ".join(text_blocks)
    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    return {
        "text": full_text, 
        "confidence": avg_conf, 
        "word_count": len(text_blocks), 
        "data": data
    }

def extract_title_from_bboxes(data: Dict[str, Any]) -> str:
    candidates = []
    for i in range(len(data["text"])):
        txt = data["text"][i].strip()
        conf = int(data["conf"][i])
        if not txt or conf < 40:
            continue
        candidates.append({"text": txt, "height": data["height"][i], "top": data["top"][i]})
    
    if not candidates:
        return ""
    
    # Sort by height (descending) to find the largest text
    candidates.sort(key=lambda x: (-x["height"], x["top"]))
    base_top = candidates[0]["top"]
    title_words = [c["text"] for c in candidates if abs(c["top"] - base_top) < 10]
    return " ".join(title_words)

def extract_title_easyocr(img: np.ndarray) -> str:
    results = easyocr_reader.readtext(img)
    if not results:
        return ""
    # Find result with largest bounding box height
    results.sort(key=lambda r: abs(r[0][0][1] - r[0][2][1]), reverse=True)
    return results[0][1] if results else ""

def perform_ocr(image_bytes: bytes) -> Dict[str, str]:
    """Main entry point for extracting text from image bytes."""
    image_np = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Could not decode image.")

    variants = preprocess_variants(img)
    best_result = {"text": "", "confidence": 0, "word_count": 0, "data": {}}
    
    for variant in variants:
        for config in OCR_CONFIGS:
            result = ocr_with_bboxes(variant, config)
            # Scoring mechanism to find the best OCR pass
            score = result["confidence"] * 0.6 + result["word_count"] * 0.4
            best_score = best_result["confidence"] * 0.6 + best_result["word_count"] * 0.4
            if score > best_score:
                best_result = result

    # Title Extraction Logic
    title = extract_title_from_bboxes(best_result["data"])
    if not title or len(title.strip()) < 3:
        h, w = img.shape[:2]
        top_crop = img[0:int(h * 0.3), 0:w]  # Look at the top 30% for title
        title = extract_title_easyocr(top_crop)

    return {
        "title": title or "Untitled Event",
        "body_text": best_result["text"]
    }