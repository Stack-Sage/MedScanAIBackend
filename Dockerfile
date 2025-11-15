# -------------------------------
# Base image
# -------------------------------
FROM python:3.10-slim

# -------------------------------
# Set working directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Install system dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libsm6 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Install Python dependencies
# -------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Copy application code
# -------------------------------
COPY app ./app

# -------------------------------
# Copy model download script
# -------------------------------
COPY download_model.sh /app/download_model.sh
RUN chmod +x /app/download_model.sh

# -------------------------------
# Create uploads folder
# -------------------------------
RUN mkdir -p /app/app/static/uploads

# -------------------------------
# Expose port
# -------------------------------
EXPOSE 8000

# -------------------------------
# Start container using the download script
# -------------------------------
CMD ["/app/download_model.sh"]
