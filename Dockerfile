# ---------------------------
# Base Python image
# ---------------------------
FROM python:3.10-slim

# ---------------------------
# Install system dependencies
# ---------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libsm6 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------
# Set working directory
# ---------------------------
WORKDIR /app

# ---------------------------
# Copy dependency files
# ---------------------------
COPY requirements.txt .

# ---------------------------
# Install Python packages
# ---------------------------
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------
# Copy entire app code
# ---------------------------
COPY . .

# ---------------------------
# Expose FastAPI port
# ---------------------------
EXPOSE 8000

# ---------------------------
# Start the app
# ---------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
