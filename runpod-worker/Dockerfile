FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

WORKDIR /worker

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy worker code
COPY handler.py .
COPY workflows/ ./workflows/ 2>/dev/null || true
COPY models/ ./models/ 2>/dev/null || true

# Environment
ENV MODELS_DIR=/runpod-volume/models
ENV OUTPUT_DIR=/runpod-volume/outputs
ENV TEMP_DIR=/tmp/iyke-worker
ENV PYTHONUNBUFFERED=1

CMD ["python", "handler.py"]
