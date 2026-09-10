# 🌐 Hosting & Deployment Guide: National Land Acquisition & Alert Management Platform

This guide provides step-by-step instructions to host and share the **National Land Acquisition & Cadastral GIS AI Portal with Panchayat Alert System** across multiple environments.

---

## 🚀 Option 1: 1-Click Local & Network Hosting (Instant on Windows / Mac / Linux)

### On Windows:
Double-click `start_portal.bat` or run in PowerShell:
```powershell
.\start_portal.ps1
```
Or start both **FastAPI Backend (port 8000)** and **Streamlit Portal (port 8501)** together:
```cmd
start_full_stack.bat
```

### Access URLs:
- **Local Browser**: `http://localhost:8501`
- **Network Sharing (LAN)**: `http://<your-computer-ip>:8501`  
  *(Share this IP with hackathon evaluators connected to the same Wi-Fi / LAN!)*

---

## ☁️ Option 2: 100% Free Public Hosting on Streamlit Community Cloud (Recommended)

Streamlit Community Cloud gives you a permanent, free public URL (e.g. `https://land-acquisition-portal.streamlit.app`) connected directly to your GitHub repository.

### Steps:
1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Integrate Panchayat Alert Management and GIS Platform"
   git push origin main
   ```
2. **Open Streamlit Cloud**:
   - Navigate to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. **Deploy the App**:
   - Click **"New app"**.
   - Select your repository (e.g., `land-acquisition-delay-prediction`).
   - Branch: `main`
   - Main file path: `app.py` (or `enhanced_portal.py`).
   - Click **"Deploy!"**.
4. Your application will be live in 1-2 minutes with automatic HTTPS and global CDN.

---

## ⚡ Option 3: Instant Public URL from Laptop via Ngrok / Localtunnel (No Cloud Setup)

If you are running the app on your laptop during a hackathon or presentation and need an instant public URL to share with judges:

### Using Ngrok:
```bash
# 1. Start the Streamlit app
python -m streamlit run app.py --server.port 8501

# 2. In another terminal, expose port 8501
ngrok http 8501
```
*Ngrok gives you a temporary public HTTPS link (e.g., `https://a1b2-c3d4.ngrok-free.app`) that opens your app on any phone or laptop anywhere in the world!*

### Using Localtunnel (No Sign-up required):
```bash
npx localtunnel --port 8501
```

---

## 🐳 Option 4: Production Docker & Docker Compose Deployment

Run both the FastAPI ML API and Streamlit GIS Portal in isolated Docker containers:

```bash
# Build and launch both services
docker-compose up -d --build

# View container logs
docker-compose logs -f

# Check health status
docker-compose ps
```

- **Portal Web UI**: `http://localhost:8501`
- **FastAPI OpenAPI Swagger**: `http://localhost:8000/docs`
- **FastAPI Health Check**: `http://localhost:8000/health`

To stop:
```bash
docker-compose down
```

---

## ☁️ Option 5: Free Cloud Hosting on Render / Railway

### Render.com:
1. Go to [render.com](https://render.com) and create a free account.
2. Click **New +** → **Web Service** → Connect your GitHub repo.
3. Configure settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python ml_pipeline.py && python multi_state_sample_generator.py`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
4. Click **Create Web Service**.

---

## 📊 Summary of Active Platform Capabilities

| Module | Features & Capabilities | Localization |
|---|---|---|
| **🚨 Panchayat Alerts** | Statutory notice dispatch, Legal templates, SMS/Email simulator, Real-time status escalation (Pending → Acknowledged → Resolved), Response rate & SLA analytics | 🇬🇧 English & 🇮🇳 தமிழ் |
| **📊 Executive Dashboard** | 6 National KPIs, 5-State funnel breakdown, Financial disbursement stack, Active litigation scatter matrix | 🇬🇧 English & 🇮🇳 தமிழ் |
| **🗺️ Jurisdiction Explorer** | State & District drilldown across 38 registered mega infrastructure projects | 🇬🇧 English & 🇮🇳 தமிழ் |
| **🌍 GIS Cadastral Map** | Real Folium interactive layer, Survey Parcels 1-61 overlay, GPS pin markers, CSV registry export | 🇬🇧 English & 🇮🇳 தமிழ் |
| **📈 Analytics & Benchmarks** | State-wise progress comparison, average compensation disbursal velocity, dispute rankings | 🇬🇧 English & 🇮🇳 தமிழ் |
| **⚖️ 7-Stage Workflow** | RFCTLARR Act 2013 statutory milestone tracker (Sec 4 SIA to Sec 38 Possession) | 🇬🇧 English & 🇮🇳 தமிழ் |
| **📋 Project Dossier** | Comprehensive project records, physical possession %, R&R family rehabilitation tracking | 🇬🇧 English & 🇮🇳 தமிழ் |
| **🤖 AI Delay Engine** | XGBoost predictive delay scoring (0-100), SHAP feature importance, "What-If" policy mitigation sandbox | 🇬🇧 English & 🇮🇳 தமிழ் |
| **📑 Cadastral Registry** | Landowner registry, Field VAO data entry form, Citizen grievance & objection ticketing | 🇬🇧 English & 🇮🇳 தமிழ் |
| **⚙️ Admin & Security** | 4-tier Role-Based Access Control (Super Admin, CALA, RDO, Landowner) & dataset re-seeder | 🇬🇧 English & 🇮🇳 தமிழ் |
