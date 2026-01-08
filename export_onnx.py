import os
from optimum.onnxruntime import ORTModelForVision2Seq
from transformers import AutoTokenizer

model_id = "vikhyatk/moondream2"
save_dir = os.environ.get("ONNX_MODEL_DIR", "onnx_model")

print(f"🚀 Exporting {model_id} to ONNX...")

# Task is inferred automatically, so we remove it to fix the ValueError
model = ORTModelForVision2Seq.from_pretrained(
    model_id,
    export=True,
    trust_remote_code=True
)

# Save the converted model and tokenizer
model.save_pretrained(save_dir)
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.save_pretrained(save_dir)

print(f"✅ Model successfully baked into {save_dir}")