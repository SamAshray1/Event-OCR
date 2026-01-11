FROM ghcr.io/abetlen/llama-cpp-python:latest

WORKDIR /app

# Only Python deps that are NOT llama.cpp
COPY requirements.txt .
RUN pip install --no-cache-dir pillow requests

COPY . .
COPY main.py .

RUN mkdir -p /models
ENV PYTHONPATH=/app

CMD ["python", "main.py"]
