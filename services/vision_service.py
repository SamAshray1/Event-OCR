import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import io

model_id = "vikhyatk/moondream2"

# Load the model with 4-bit quantization for CPU speed
# trust_remote_code is essential for Moondream's custom vision tower
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    trust_remote_code=True,
    low_cpu_mem_usage=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)
model.eval()

def extract_event_vlm(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Pre-processing: Resize to 768px to drastically reduce CPU cycles
    image.thumbnail((768, 768)) 
    
    # Encode the image once
    enc_image = model.encode_image(image)
    
    # Precise prompt for JSON-like output
    prompt = "Identify the Title, Date, Time, and Location from this poster. Return the result in a clear list format."
    
    # High-level helper provided by the Moondream authors
    response = model.answer_question(enc_image, prompt, tokenizer)
    
    return response

def extract_from_crop_vlm(image_bytes: bytes, x, y, w, h):
    full_img = Image.open(io.BytesIO(image_bytes))
    # Standard PIL crop
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = x1 + abs(w), y1 + abs(h)
    cropped_img = full_img.crop((x1, y1, x2, y2))
    
    enc_image = model.encode_image(cropped_img)
    prompt = "Read the text in this image exactly as it appears."
    return model.answer_question(enc_image, prompt, tokenizer)