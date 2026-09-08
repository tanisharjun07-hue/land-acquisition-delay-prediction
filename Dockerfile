FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ml_pipeline.py .
COPY fastapi_backend.py .
COPY streamlit_dashboard.py .

# Train model on startup
RUN python ml_pipeline.py

# Expose ports
EXPOSE 8000 8501

# Default to running FastAPI (can override with CMD)
CMD ["python", "fastapi_backend.py"]
