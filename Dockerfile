FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN python3 -c "import easyocr; easyocr.Reader(['en'], gpu=False)"

RUN python -c "from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('vikhyatk/moondream2', trust_remote_code=True)"

COPY . ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
