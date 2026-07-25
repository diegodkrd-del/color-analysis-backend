FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=10000

# Install system dependencies required for WeasyPrint, OpenCV, and rembg
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 10000

# Command to run uvicorn server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
