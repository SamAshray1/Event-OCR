import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import io
import json

# Initialize model and tokenizer
model_id = "vikhyatk/moondream2"
# Remove revision="2024-08-05" to avoid the 404 error
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading {model_id} onto {device}...")

# trust_remote_code=True is required for moondream
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    trust_remote_code=True, 
).to(device)

tokenizer = AutoTokenizer.from_pretrained(model_id)
model.eval() # Set to evaluation mode

def extract_event_with_vlm(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes))
    
    # We provide a prompt that forces the model to act as a structured extractor
    prompt = "Extract the event details from this image. Provide the Title, Date, Time, and Location. If a field is missing, say 'Unknown'."
    
    # Moondream specific inference
    enc_image = model.encode_image(image)
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