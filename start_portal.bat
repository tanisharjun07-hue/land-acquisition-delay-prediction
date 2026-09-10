@echo off
title National Land Acquisition GIS & Alert Management Portal
color 0B
cls
echo ===============================================================================
echo     NATIONAL LAND ACQUISITION & CADASTRAL GIS AI PLATFORM (SIH 2024)
echo     Real Maps + Survey Numbers + Alert Messaging + Tamil Localization
echo ===============================================================================
echo.
echo [1/3] Verifying Python Environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b 1
)

echo [2/3] Checking Datasets & AI ML Pipeline...
python -c "from multi_state_sample_generator import get_or_create_multi_state_data; get_or_create_multi_state_data(); print(' Dataset Verified.')"
python -c "from land_ownership_loader import load_ownership_data; load_ownership_data(); print(' Cadastral Registry Loaded.')"

echo [3/3] Launching Streamlit Portal on Port 8501...
echo.
echo ===============================================================================
echo   Local Web URL:     http://localhost:8501
echo   Network Web URL:   http://0.0.0.0:8501
echo   Alert Management:  Integrated Live (SMS / Email / WhatsApp)
echo ===============================================================================
echo.

python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0

pause
