from huggingface_hub import snapshot_download
import os

MODEL_ID = "vikhyatk/moondream2"
MODEL_DIR = "/app/models/moondream2"

def download_model():
    """
    Downloads Moondream2 ONNX artifacts if not already present.
    Uses HF_TOKEN automatically if set.
    """
    if os.path.exists(MODEL_DIR) and os.listdir(MODEL_DIR):
        return MODEL_DIR

    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=MODEL_DIR,
        local_dir_use_symlinks=False,
        allow_patterns=[
            "*.onnx",
            "*.json",
            "*.txt"
        ]
    )

    return MODEL_DIR
