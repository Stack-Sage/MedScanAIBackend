#!/bin/bash
set -e  # stop if any command fails

# Create saved_models folder if it doesn't exist
mkdir -p /app/saved_models

# Download the model using gdown
MODEL_ID="1AbCDEfgHIjkLMNOPqrSTuvWxYz"
MODEL_PATH="/app/saved_models/vgg16_medical.h5"

if [ ! -f "$MODEL_PATH" ]; then
    echo "Downloading model..."
    gdown "https://drive.google.com/uc?id=${MODEL_ID}" -O "$MODEL_PATH"
else
    echo "Model already exists, skipping download."
fi

# Start FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000
