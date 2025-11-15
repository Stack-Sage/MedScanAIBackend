#!/bin/bash
set -e

# Create saved_models folder in root
mkdir -p saved_models

# Google Drive model ID
MODEL_ID="1HhLKKSu1iG0iEBnDB5BTqDlMdTSgnyKM"
MODEL_PATH="/saved_models/vgg16_medical.h5"

# Download model if missing
if [ ! -f "$MODEL_PATH" ]; then
    echo "Downloading VGG16 model..."
    gdown --id $MODEL_ID -O "$MODEL_PATH"
else
    echo "Model already exists, skipping download."
fi

# Start FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000
