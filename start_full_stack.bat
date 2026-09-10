@echo off
title National Land Acquisition Platform - Full Stack Launcher
color 0E
cls
echo ===============================================================================
echo     LAUNCHING FULL STACK: FASTAPI (8000) + STREAMLIT PORTAL (8501)
echo ===============================================================================
echo.

echo [1/2] Starting FastAPI Backend on port 8000 in background...
start "FastAPI Backend (Port 8000)" cmd /k "python -m uvicorn fastapi_backend:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Starting Streamlit Portal on port 8501...
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0

pause
