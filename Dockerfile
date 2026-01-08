FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# 🚀 ADD THIS: Ensure 'app' folder is discoverable
ENV PYTHONPATH=/app 

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN python -c "from transformers import AutoModelForCausalLM; \
AutoModelForCausalLM.from_pretrained('vikhyatk/moondream2', trust_remote_code=True)"

COPY . .

EXPOSE 8000
# Ensure this matches your file path: if main.py is in /app/app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]