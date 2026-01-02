# 1️⃣ Base image
FROM python:3.11-slim

# 2️⃣ Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Install system dependencies (Tesseract + OpenCV deps)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Set working directory
WORKDIR /app

# 5️⃣ Copy requirements first (for Docker cache)
COPY requirements.txt .

# 6️⃣ Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 7️⃣ Copy application code
COPY . ./app

# 8️⃣ Expose FastAPI port
EXPOSE 8000

# 9️⃣ Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
