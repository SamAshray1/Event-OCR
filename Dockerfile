FROM python:3.10-slim

WORKDIR /app

# System deps required by torch + PIL
RUN apt-get update && apt-get install -y \
    git \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Prevent torch thread explosion in Docker
ENV OMP_NUM_THREADS=4
ENV MKL_NUM_THREADS=4
ENV TOKENIZERS_PARALLELISM=false

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
