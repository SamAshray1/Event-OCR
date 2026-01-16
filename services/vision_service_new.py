import io
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

MODEL_ID = "vikhyatk/moondream2"

# ---------------------------
# CPU OPTIMIZATION (VERY IMPORTANT)
# ---------------------------
torch.set_num_threads(4)
torch.set_num_interop_threads(4)
torch.backends.quantized.engine = "qnnpack"

# ---------------------------
# Load model (CPU only)
# ---------------------------
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
    low_cpu_mem_usage=True,
    device_map="cpu",
    torch_dtype=torch.float32
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model.eval()

# TorchScript vision tower (safe + big speedup)
model.vision_tower = torch.jit.script(model.vision_tower)

# ---------------------------
# Helpers
# ---------------------------
def _load_image(image_bytes: bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img.thumbnail((512, 512))  # CRITICAL for Docker CPU
    return img

# ---------------------------
# Public API
# ---------------------------
def extract_event_with_vlm(image_bytes: bytes):
    image = _load_image(image_bytes)

    with torch.inference_mode():
        image_embeds = model.encode_image(image)
        prompt = (
            "Identify the Title, Date, Time, and Location from this poster. "
            "Return the result in a clear list format."
        )
        return model.answer_question(
            image_embeds,
            prompt,
            tokenizer,
            max_new_tokens=64
        )


def extract_from_crop_vlm(image_bytes: bytes, x, y, w, h):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = x1 + abs(w), y1 + abs(h)
    crop = image.crop((x1, y1, x2, y2))
    crop.thumbnail((512, 512))

    with torch.inference_mode():
        image_embeds = model.encode_image(crop)
        return model.answer_question(
            image_embeds,
            "Read the text in this image exactly as it appears.",
            tokenizer,
            max_new_tokens=64
        )
