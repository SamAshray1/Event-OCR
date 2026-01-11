from PIL import Image
import io
import base64
import os
from llama_cpp import Llama
from models.model_utils import download_model

MODEL_PATH = download_model()

llm = Llama(
    model_path=str(MODEL_PATH),
    n_threads=os.cpu_count(),
    n_ctx=4096,
    verbose=False,
)
# ==========================
# Helpers
# ==========================

def _image_to_base64(image: Image.Image) -> str:
    """
    Convert PIL Image → base64 PNG
    """
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def _run_vlm(prompt: str, image: Image.Image) -> str:
    """
    Send image + prompt to llama.cpp VLM
    """
    image_b64 = _image_to_base64(image)

    response = llm.create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_b64}"
                        },
                    },
                ],
            }
        ],
        temperature=0.1,
        max_tokens=256,
    )

    return response["choices"][0]["message"]["content"]


# ==========================
# Public API
# ==========================

def extract_event_vlm(image_bytes: bytes) -> str:
    """
    Extract Title, Date, Time, Location from a poster
    """
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # CPU optimization
    image.thumbnail((768, 768))

    prompt = (
        "Identify the event details from this poster.\n"
        "Return the following fields clearly:\n"
        "- Title\n"
        "- Date\n"
        "- Time\n"
        "- Location"
    )

    return _run_vlm(prompt, image)


def extract_from_crop_vlm(image_bytes: bytes, x, y, w, h) -> str:
    """
    OCR-like exact text extraction from a cropped region
    """
    full_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    x1, y1 = max(0, x), max(0, y)
    x2, y2 = x1 + abs(w), y1 + abs(h)

    cropped = full_img.crop((x1, y1, x2, y2))
    cropped.thumbnail((768, 768))

    prompt = "Read the text in this image exactly as it appears."

    return _run_vlm(prompt, cropped)
