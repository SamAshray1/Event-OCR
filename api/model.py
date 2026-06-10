from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import torch

MODEL_ID = "vikhyatk/moondream2"

print("Loading Moondream model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
    torch_dtype=torch.float32
).eval()

print("Model loaded successfully")


def ask_model(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")

    prompt = """
    Extract event details from this poster.

    Return ONLY valid JSON.

    Format:
    {
        "title": "",
        "date": "",
        "time": "",
        "location": ""
    }
    """

    response = model.answer_question(
        image,
        prompt,
        tokenizer
    )

    return response