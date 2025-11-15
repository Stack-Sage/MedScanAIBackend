#!/bin/bash
set -e

# Create saved_models folder
mkdir -p /app/saved_models

# Google Drive model ID
MODEL_ID="1A2b3C4d5E6F7g8H9I0JklMnOpQrStUv"
MODEL_PATH="/app/saved_models/vgg16_medical.h5"

# Download model if missing
if [ ! -f "$MODEL_PATH" ]; then
    echo "Downloading VGG16 model..."
    gdown "https://drive.google.com/uc?id=${MODEL_ID}" -O "$MODEL_PATH"
else
    echo "Model already exists, skipping download."
fi

# Start FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000
