import os
import sys
import requests
from pathlib import Path

MODEL_URL = (
    "https://huggingface.co/"
    "TheBloke/llava-phi-3-mini-GGUF/resolve/main/"
    "llava-phi-3-mini.Q4_K_M.gguf"
)

MODEL_DIR = Path(os.getenv("MODEL_DIR", "/models"))
MODEL_PATH = MODEL_DIR / "llava.gguf"


def download_model():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 100_000_000:
        print(f"✅ Model already exists: {MODEL_PATH}")
        return MODEL_PATH

    print(f"⬇️ Downloading model to {MODEL_PATH}")

    with requests.get(MODEL_URL, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    if MODEL_PATH.stat().st_size < 100_000_000:
        raise RuntimeError("❌ Model download incomplete or corrupted")

    print("✅ Model downloaded successfully")
    return MODEL_PATH


if __name__ == "__main__":
    download_model()
