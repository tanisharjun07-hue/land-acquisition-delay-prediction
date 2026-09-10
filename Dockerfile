FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files and data
COPY . .

# Ensure model and sample data are pre-generated
RUN python ml_pipeline.py && python multi_state_sample_generator.py

# Expose ports (FastAPI on 8000, Streamlit on 8501)
EXPOSE 8000 8501

# Default command: launch the National Land Acquisition & GIS Portal
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

