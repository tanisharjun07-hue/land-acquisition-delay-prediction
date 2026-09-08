#!/bin/bash

# Land Acquisition Prediction System - Quick Start Script
# Run this to set up everything in 5 minutes!

set -e

echo "🚀 Land Acquisition Delay Prediction - Quick Start"
echo "=================================================="
echo ""

# Step 1: Install dependencies
echo "📦 Step 1: Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 2: Train model
echo "🤖 Step 2: Training ML model..."
python ml_pipeline.py > /dev/null 2>&1
echo "✅ Model trained and saved to land_acquisition_model.pkl"
echo ""

# Step 3: Create necessary directories
mkdir -p data models logs

echo "📁 Step 3: Directory structure created"
echo ""

# Step 4: Information for running services
echo "🎯 Step 4: Ready to run!"
echo ""
echo "=================================================="
echo "To start the system, run these commands in separate terminals:"
echo "=================================================="
echo ""
echo "Terminal 1 - FastAPI Backend (Port 8000):"
echo "  python fastapi_backend.py"
echo ""
echo "Terminal 2 - Streamlit Dashboard (Port 8501):"
echo "  streamlit run streamlit_dashboard.py"
echo ""
echo "=================================================="
echo ""
echo "Once running:"
echo "  📍 API Docs: http://localhost:8000/docs"
echo "  📊 Dashboard: http://localhost:8501"
echo "  🏥 Health Check: http://localhost:8000/health"
echo ""
echo "=================================================="
echo "✨ System ready for hackathon! Good luck! 🏆"
echo "=================================================="
