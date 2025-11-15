FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libsm6 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install gdown (needed for downloading model)
RUN pip install gdown

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create model directory
RUN mkdir -p saved_models

# Download the model file from Google Drive
# Replace FILE_ID with your actual ID
RUN gdown "https://drive.google.com/uc?id=YOUR_GOOGLE_DRIVE_ID" \
    -O saved_models/vgg16_medical.h5

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
