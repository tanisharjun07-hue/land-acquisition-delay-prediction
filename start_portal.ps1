# National Land Acquisition & Cadastral GIS Platform - PowerShell Launcher
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "    NATIONAL LAND ACQUISITION & CADASTRAL GIS AI PLATFORM (SIH 2024)" -ForegroundColor Yellow
Write-Host "    Real Maps + Survey Numbers + Alert Messaging + Tamil Localization" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Verifying Python Environment..." -ForegroundColor Green
$pyVer = python --version 2>&1
Write-Host "      Detected: $pyVer" -ForegroundColor Gray

Write-Host "[2/3] Checking Datasets & AI ML Pipeline..." -ForegroundColor Green
python -c "from multi_state_sample_generator import get_or_create_multi_state_data; get_or_create_multi_state_data(); print('      ✓ Dataset Verified.')"
python -c "from land_ownership_loader import load_ownership_data; load_ownership_data(); print('      ✓ Cadastral Registry Loaded.')"

Write-Host "[3/3] Launching Portal on Port 8501..." -ForegroundColor Green
Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  Local Web URL:     http://localhost:8501" -ForegroundColor Yellow
Write-Host "  Network Web URL:   http://0.0.0.0:8501" -ForegroundColor Yellow
Write-Host "  Alert Management:  Integrated Live (SMS / Email / WhatsApp)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
