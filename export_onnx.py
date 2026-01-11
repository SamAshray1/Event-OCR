from models.model_utils import load_llm, export_model

def export_to_onnx(output_path: str):
    llm = load_llm()
    export_model(llm, output_path)
