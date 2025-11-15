FROM python:3.10-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libsm6 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gdown

# Copy app code
COPY app ./app

# Copy saved models (classes.json already there)
COPY saved_models ./saved_models

# Copy and make the download script executable
COPY download_model.sh /app/download_model.sh
RUN chmod +x /app/download_model.sh

# Create uploads folder
RUN mkdir -p /app/app/static/uploads

# Expose port
EXPOSE 8000

# Start container with the download script
CMD ["/app/download_model.sh"]
