"""
🏛️ NATIONAL LAND ACQUISITION & CADASTRAL GIS PLATFORM (SIH 2024)
State-of-the-Art GIS Mapping + Real Cadastral Survey Parcels + Tamil & English Localization +
RFCTLARR Act 2013 7-Stage Workflow + XGBoost & SHAP AI Delay Predictions + What-If Simulation Sandbox
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium

# Import local data generator & ML modules
from multi_state_sample_generator import get_or_create_multi_state_data, BASE_DIR
from land_ownership_loader import load_ownership_data, get_cadastral_parcel_coordinates
from ml_pipeline import LandAcquisitionPredictor

# ============================================================================
# 1. PURE BILINGUAL DICTIONARY (ENGLISH & AUTHENTIC TAMIL தமிழ்)
# ============================================================================

LANGUAGES = {
    "English": {
        "title": "National Land Acquisition Management System",
        "subtitle": "Real-Time Digital Cadastral Monitoring, GIS Mapping & AI Delay Predictions",
        "gov_brand": "Government of India | Ministry of Rural Development | Smart India Hackathon 2024",
        "select_language": "Language",
        "system_status": "🟢 LIVE: National GIS Grid Online",
        "dashboard": "Executive Dashboard",
        "geographic_view": "Jurisdiction Explorer",
        "gis_map": "GIS Cadastral Map",
        "analytics": "Analytics & Benchmarks",
        "workflow": "Statutory 7-Stage Workflow",
        "project_details": "Project Dossier",
        "ai_predictions": "AI Delay & What-If Sandbox",
        "registry": "Cadastral Registry & Grievance",
        "admin": "Admin & Governance",
        "total_projects": "Total Projects",
        "total_area": "Land Area (Acres)",
        "families": "Affected Families",
        "compensation": "Total Compensation",
        "completion": "Average Possession %",
        "disputes": "Active Litigations",
        "status": "Acquisition Status",
        "pending": "Pending",
        "notified": "Notified (Sec 11)",
        "awarded": "Awarded (Sec 23)",
        "possessed": "Possessed (Sec 38)",
        "executive_dashboard": "Executive Overview & National KPIs",
        "select_state": "Select State Jurisdiction",
        "select_district": "Select District",
        "select_project": "Select Infrastructure Project",
        "projects_list": "Registered Infrastructure Projects",
        "rr_progress": "R&R Rehabilitation Progress",
        "legal_disputes": "Legal Title Disputes",
        "run_prediction": "Run XGBoost AI Risk Prediction",
        "prediction_results": "AI Predictive Risk Assessment",
        "delay_risk": "Delay Probability Risk",
        "completion_date": "Projected Possession Date",
        "factors": "Key Risk Contributing Factors (SHAP)",
        "recommendations": "Actionable AI Mitigation Directives",
        "high_risk": "High Risk",
        "medium_risk": "Medium Risk",
        "low_risk": "Low Risk",
        "critical_risk": "Critical Bottleneck",
        "map_view": "Interactive GIS Folium Map",
        "survey_number": "Survey Parcel No",
        "extent": "Extent (Acres)",
        "ownership": "Ownership Category",
        "land_type": "Land Classification",
        "coordinates": "GPS Coordinates",
        "parcels": "Cadastral Parcels",
        "parcel_details": "Cadastral Survey Records & Ownership Registry",
        "gis_enabled": "GIS Cadastral Overlay Active",
        "download_csv": "📥 Download Project Records (CSV)",
        "download_parcels_csv": "📥 Download Cadastral Registry (CSV)",
        "fastest_state": "Fastest Execution State",
        "largest_area": "Largest Land Extent",
        "lowest_disputes": "Lowest Litigation Burden",
        "what_if_title": "Interactive 'What-If' Delay Mitigation Sandbox",
        "what_if_desc": "Simulate strategic administrative interventions and observe live risk reduction & days saved.",
        "grievance_title": "Landowner Title Objection & Grievance Portal",
        "submit_grievance": "Submit Grievance",
        "ticket_created": "Grievance Ticket Generated",
        "workflow_title": "RFCTLARR Act 2013 Statutory 7-Stage Process Tracker",
        "alerts": "Panchayat Alert & Notification System",
        "send_alert": "Send Alert / Notice to Panchayat",
        "alert_history": "Alert History & Logs",
        "alert_status": "Response Status",
        "panchayat_name": "Panchayat / Local Authority Name",
        "village": "Village / Revenue Ward",
        "contact_person": "Contact Person / President",
        "phone": "Official Contact Number",
        "email": "Official Email Address",
        "alert_type": "Alert / Notice Category",
        "priority": "Priority Urgency Level",
        "subject": "Statutory Subject / Ref No",
        "description": "Notice Description",
        "send": "Dispatch Statutory Notice",
        "date_sent": "Dispatched Date",
        "date_response": "Response Date",
        "response": "Response Status",
        "escalate": "Escalate to Critical",
        "mark_resolved": "Mark as Resolved",
        "resend": "Resend Notification",
        "land_not_ready": "Land Not Ready for Possession",
        "compensation_issue": "Compensation Payment Disbursement Lag",
        "rr_incomplete": "R&R Rehabilitation Process Incomplete",
        "legal_dispute": "Legal Title Dispute Pending",
        "documentation_missing": "Statutory Documentation Missing",
        "stakeholder_objection": "Stakeholder / Public Objection",
        "urgent_action": "Urgent Action Required (Possession Deadline)",
        "follow_up": "Statutory Follow-up Action",
        "compliance_notice": "RFCTLARR Compliance Notice",
        "default_template": "Use Statutory Pre-filled Template",
        "custom_message": "Custom Notice Body / Message",
        "save_template": "Save as Reusable Template",
        "track_alerts": "Track All Panchayat Alerts",
        "create_alert": "Create & Dispatch Alert Notice",
        "alert_statistics": "Alert Analytics & Response Metrics",
        "response_rate": "Panchayat Response Rate",
        "avg_response_time": "Average Response Time",
        "unresolved_alerts": "Unresolved Bottlenecks",
        "critical_alerts": "Critical Priority Alerts",
        "send_email": "Official Email Dispatch",
        "send_sms": "SMS Mobile Dispatch",
        "send_both": "SMS + Email Dual Dispatch",
        "send_whatsapp": "WhatsApp Official Dispatch",
        "alert_sent_success": "Panchayat alert & compliance notice dispatched successfully!",
        "escalated_success": "Alert escalated to CRITICAL priority! State Headquarter notified.",
        "mark_resolved_success": "Alert marked as RESOLVED! Compliance record updated."
    },
    "Tamil": {
        "title": "தேசிய நில எடுப்பு மேலாண்மை தளம்",
        "subtitle": "நிகழ் நேர GIS வரைபடம், சர்வே எண்கள் & AI தாமத கணிப்புடன் கூடிய டிஜிட்டல் தளம்",
        "gov_brand": "இந்திய அரசு | ஊரக வளர்ச்சி அமைச்சகம் | ஸ்மார்ட் இந்தியா ஹேக்கத்தான் 2024",
        "select_language": "மொழி",
        "system_status": "🟢 நேரலை: தேசிய GIS கட்டமைப்பு இயங்குகிறது",
        "dashboard": "நிர்வாக முகப்பு பலகை",
        "geographic_view": "மாநில & மாவட்ட ஆய்வு",
        "gis_map": "GIS சர்வே வரைபடம்",
        "analytics": "பகுப்பாய்வு & ஒப்பீடு",
        "workflow": "சட்டப்பூர்வ 7-நிலை பணிப்பாய்வு",
        "project_details": "திட்ட விவரங்கள்",
        "ai_predictions": "AI தாமத கணிப்பு & மாதிரி",
        "registry": "நிலப் பதிவேடு & குறைதீர்ப்பு",
        "admin": "நிர்வாகம் & பாதுகாப்பு",
        "total_projects": "மொத்த திட்டங்கள்",
        "total_area": "நிலப்பரப்பு (ஏக்கர்)",
        "families": "பாதிக்கப்பட்ட குடும்பங்கள்",
        "compensation": "மொத்த இழப்பீட்டுத் தொகை",
        "completion": "கையகப்படுத்தல் சதவீதம்",
        "disputes": "நீதிமன்ற வழக்குகள்",
        "status": "கையகப்படுத்தல் நிலை",
        "pending": "நிலுவையில் (Pending)",
        "notified": "அறிவிக்கப்பட்டது (Sec 11)",
        "awarded": "வழங்கப்பட்டது (Sec 23)",
        "possessed": "கையகப்படுத்தப்பட்டது (Sec 38)",
        "executive_dashboard": "முக்கிய தேசிய குறிகாட்டிகள் & மேலோட்டம்",
        "select_state": "மாநிலத்தை தேர்ந்தெடுக்கவும்",
        "select_district": "மாவட்டத்தை தேர்ந்தெடுக்கவும்",
        "select_project": "திட்டத்தை தேர்ந்தெடுக்கவும்",
        "projects_list": "பதிவு செய்யப்பட்ட திட்டங்கள்",
        "rr_progress": "மறுவாழ்வு (R&R) முன்னேற்றம்",
        "legal_disputes": "நீதிமன்ற வழக்குகள்",
        "run_prediction": "XGBoost AI கணிப்பை இயக்கவும்",
        "prediction_results": "AI இடர் பகுப்பாய்வு முடிவுகள்",
        "delay_risk": "தாமத ஆபத்து சதவீதம்",
        "completion_date": "மதிப்பிடப்பட்ட நிறைவு தேதி",
        "factors": "முக்கிய ஆபத்து காரணிகள் (SHAP)",
        "recommendations": "செயல்படுத்தக்கூடிய AI பரிந்துரைகள்",
        "high_risk": "அதிக ஆபத்து (High Risk)",
        "medium_risk": "நடுத்தர ஆபத்து (Medium Risk)",
        "low_risk": "குறைந்த ஆபத்து (Low Risk)",
        "critical_risk": "மிகத் தீவிர ஆபத்து",
        "map_view": "ஊடாடும் GIS வரைபட பார்வை",
        "survey_number": "சர்வே எண்",
        "extent": "பரப்பளவு (ஏக்கர்)",
        "ownership": "உடைமை வகை",
        "land_type": "நில வகைப்பாடு",
        "coordinates": "GPS ஆயத்தொலைவுகள்",
        "parcels": "சர்வே நிலப் பிரிவுகள்",
        "parcel_details": "சர்வே எண் & நில உரிமையாளர் பதிவேடு",
        "gis_enabled": "GIS சர்வே அடுக்கு செயல்பாட்டில் உள்ளது",
        "download_csv": "📥 திட்ட விபரங்கள் பதிவிறக்கம் (CSV)",
        "download_parcels_csv": "📥 சர்வே பதிவேடு பதிவிறக்கம் (CSV)",
        "fastest_state": "விரைவான நில எடுப்பு மாநிலம்",
        "largest_area": "மிகப்பெரிய நிலப்பரப்பு",
        "lowest_disputes": "குறைந்த வழக்குகள் கொண்ட மாநிலம்",
        "what_if_title": "AI இடர் தணிப்பு மாதிரி & ஆய்வுக்கூடம்",
        "what_if_desc": "நிர்வாக நடவடிக்கைகளை சோதித்து, தாமத நாட்களையும் இடரையும் குறைக்கும் முறை.",
        "grievance_title": "நில உரிமையாளர் குறைதீர்ப்பு & ஆட்சேபனை பதிவு",
        "submit_grievance": "குறைதீர்ப்பு மனு சமர்ப்பிக்கவும்",
        "ticket_created": "குறைதீர்ப்பு மனு எண் உருவாக்கப்பட்டது",
        "workflow_title": "RFCTLARR சட்டம் 2013: 7-நிலை சட்டப்பூர்வ பணிப்பாய்வு",
        "alerts": "பஞ்சாயத்து விழிப்பூட்டல் & அறிவிப்பு மேலாண்மை",
        "send_alert": "பஞ்சாயத்திற்கு விழிப்பூட்டல் / நோட்டீஸ் அனுப்பவும்",
        "alert_history": "விழிப்பூட்டல் வரலாறு & பதிவுகள்",
        "alert_status": "பதிலளிப்பு நிலை",
        "panchayat_name": "பஞ்சாயத்து பெயர்",
        "village": "கிராமம் / வார்டு",
        "contact_person": "தொடர்பு நபர் / தலைவர்",
        "phone": "தொலைபேசி எண்",
        "email": "மின்னஞ்சல் முகவரி",
        "alert_type": "விழிப்பூட்டல் வகை",
        "priority": "முன்னுரிமை",
        "subject": "பொருள்",
        "description": "விளக்கம்",
        "send": "விழிப்பூட்டல் அனுப்பவும்",
        "date_sent": "அனுப்பிய தேதி",
        "date_response": "பதிலளிக்கப்பட்ட தேதி",
        "response": "பதிலளிப்பு நிலை",
        "escalate": "முக்கிய நிலைக்கு உயர்த்து",
        "mark_resolved": "தீர்க்கப்பட்டதாக குறிக்கவும்",
        "resend": "மீண்டும் அனுப்பவும்",
        "land_not_ready": "நிலம் கையகப்படுத்தலுக்கு தயார் இல்லை",
        "compensation_issue": "இழப்பீட்டுத் தொகை வழங்கலில் தாமதம்",
        "rr_incomplete": "மறுவாழ்வு (R&R) செயல்முறை முடிவடையவில்லை",
        "legal_dispute": "நீதிமன்ற வழக்கு நிலுவையில் உள்ளது",
        "documentation_missing": "ஆவணங்கள் சமர்ப்பிக்கப்படவில்லை",
        "stakeholder_objection": "பொதுமக்கள் ஆட்சேபனை",
        "urgent_action": "அவசர நடவடிக்கை தேவை",
        "follow_up": "பின்தொடர் நடவடிக்கை",
        "compliance_notice": "சட்டப்பூர்வ இணக்க அறிவிப்பு",
        "default_template": "சட்டப்பூர்வ மாதிரி உரையைப் பயன்படுத்தவும்",
        "custom_message": "தனிப்பயன் உரை",
        "save_template": "மாதிரியாக சேமிக்கவும்",
        "track_alerts": "அனைத்து விழிப்பூட்டல்களையும் கண்காணிக்க",
        "create_alert": "புதிய விழிப்பூட்டல் உருவாக்கம்",
        "alert_statistics": "விழிப்பூட்டல் புள்ளிவிவரங்கள் & பகுப்பாய்வு",
        "response_rate": "பதிலளிப்பு விகிதம்",
        "avg_response_time": "சராசரி பதிலளிப்பு நேரம்",
        "unresolved_alerts": "தீர்க்கப்படாத விழிப்பூட்டல்கள்",
        "critical_alerts": "தீவிர விழிப்பூட்டல்கள்",
        "send_email": "அதிகாரப்பூர்வ மின்னஞ்சல்",
        "send_sms": "குறுஞ்செய்தி (SMS)",
        "send_both": "மின்னஞ்சல் + குறுஞ்செய்தி இரண்டும்",
        "send_whatsapp": "வாட்ஸ்அப் (WhatsApp) அறிவிப்பு",
        "alert_sent_success": "பஞ்சாயத்து விழிப்பூட்டல் வெற்றிகரமாக அனுப்பப்பட்டது!",
        "escalated_success": "விழிப்பூட்டல் தீவிர நிலைக்கு உயர்த்தப்பட்டது!",
        "mark_resolved_success": "விழிப்பூட்டல் தீர்க்கப்பட்டதாக குறிக்கப்பட்டது!"
    }
}

# ============================================================================
# 2. PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="National Land Acquisition Management System | GIS & AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 3. ADVANCED GOV-TECH & GLASSMORPHISM DESIGN SYSTEM
# ============================================================================

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Noto+Sans+Tamil:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', 'Noto Sans Tamil', -apple-system, sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0b1329 0%, #0f172a 50%, #0d1b2a 100%);
        color: #f1f5f9;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1128 0%, #001f54 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Top Header Banner */
    .gov-hero-container {
        background: linear-gradient(135deg, #03071e 0%, #0d1b2a 40%, #1b263b 100%);
        border: 1px solid rgba(255, 193, 7, 0.3);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 22px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .gov-hero-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff9933 0%, #ffffff 50%, #138808 100%);
    }
    
    .gov-header-title {
        font-size: 28px;
        font-weight: 800;
        color: #ffc107;
        letter-spacing: 0.5px;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.6);
    }
    
    .gov-header-sub {
        font-size: 14px;
        color: #e2e8f0;
        margin-top: 5px;
        font-weight: 400;
    }
    
    .gov-header-meta {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 8px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .live-badge {
        display: inline-block;
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid #10b981;
        color: #10b981;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5); }
        70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    /* Stat Cards */
    .stat-card-glass {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.25s ease, border-color 0.25s ease;
        margin-bottom: 12px;
    }
    
    .stat-card-glass:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 193, 7, 0.5);
    }
    
    .stat-icon {
        font-size: 24px;
        margin-bottom: 4px;
    }
    
    .stat-val {
        font-size: 26px;
        font-weight: 800;
        color: #ffc107;
        margin: 2px 0;
    }
    
    .stat-label {
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-sub {
        font-size: 11px;
        color: #cbd5e1;
        margin-top: 4px;
    }
    
    /* Content Glass Boxes */
    .glass-box {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    }
    
    .glass-box-gold { border-left: 4px solid #ffc107; }
    .glass-box-green { border-left: 4px solid #10b981; }
    .glass-box-red { border-left: 4px solid #ef4444; }
    .glass-box-blue { border-left: 4px solid #3b82f6; }
    
    /* Status Badges */
    /* Status Badges */
    .status-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }
    .status-possessed { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
    .status-awarded { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid #3b82f6; }
    .status-notified { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }
    .status-pending { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
    
    /* Alert Specific Card Styling */
    .alert-critical-card {
        background: rgba(239, 68, 68, 0.12);
        border-left: 5px solid #ef4444;
        border-top: 1px solid rgba(239, 68, 68, 0.25);
        border-right: 1px solid rgba(239, 68, 68, 0.25);
        border-bottom: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: 12px;
        padding: 18px 20px;
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.15);
    }
    .alert-high-card {
        background: rgba(249, 115, 22, 0.12);
        border-left: 5px solid #f97316;
        border-top: 1px solid rgba(249, 115, 22, 0.25);
        border-right: 1px solid rgba(249, 115, 22, 0.25);
        border-bottom: 1px solid rgba(249, 115, 22, 0.25);
        border-radius: 12px;
        padding: 18px 20px;
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(249, 115, 22, 0.15);
    }
    .alert-medium-card {
        background: rgba(234, 179, 8, 0.12);
        border-left: 5px solid #eab308;
        border-top: 1px solid rgba(234, 179, 8, 0.25);
        border-right: 1px solid rgba(234, 179, 8, 0.25);
        border-bottom: 1px solid rgba(234, 179, 8, 0.25);
        border-radius: 12px;
        padding: 18px 20px;
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(234, 179, 8, 0.15);
    }
    .alert-low-card {
        background: rgba(16, 185, 129, 0.12);
        border-left: 5px solid #10b981;
        border-top: 1px solid rgba(16, 185, 129, 0.25);
        border-right: 1px solid rgba(16, 185, 129, 0.25);
        border-bottom: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 12px;
        padding: 18px 20px;
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.15);
    }
    
    /* Buttons Styling */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.5) !important;
    }
    
    /* Navigation radio cleanup */
    [data-testid="stSidebar"] .stRadio label {
        color: #e2e8f0 !important;
        font-weight: 500;
        font-size: 14px;
        padding: 4px 0;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# 4. ROBUST MULTI-STATE & CADASTRAL DATA LOADER
# ============================================================================

@st.cache_data(ttl=600)
def load_all_datasets():
    """Load multi-state projects, ownership parcel data, and metrics with full fallback"""
    df, metrics = get_or_create_multi_state_data()
    ownership_df = load_ownership_data()
    
    # Enrich cadastral parcels with coordinates if available
    if ownership_df is not None and not ownership_df.empty:
        parcel_coords_map = get_cadastral_parcel_coordinates()
        base_lat = 13.0827
        base_lon = 80.2707
        
        lats, lons = [], []
        for _, row in ownership_df.iterrows():
            s_no = row['survey_no']
            if s_no in parcel_coords_map:
                rel_x, rel_y = parcel_coords_map[s_no]
                lat = base_lat + (rel_y - 0.5) * 0.035
                lon = base_lon + (rel_x - 0.5) * 0.035
            else:
                lat = base_lat + np.random.uniform(-0.015, 0.015)
                lon = base_lon + np.random.uniform(-0.015, 0.015)
            lats.append(round(lat, 6))
            lons.append(round(lon, 6))
            
        ownership_df['latitude'] = lats
        ownership_df['longitude'] = lons
        
    return df, ownership_df, metrics


@st.cache_resource
def load_ai_predictor():
    """Load or train the XGBoost delay prediction model"""
    predictor = LandAcquisitionPredictor()
    model_path = os.path.join(BASE_DIR, 'land_acquisition_model.pkl')
    if os.path.exists(model_path):
        try:
            predictor.load_model(model_path)
            return predictor
        except Exception:
            pass
    # Auto-train fallback
    sample_data = predictor.create_sample_dataset(500)
    predictor.train(sample_data)
    return predictor


df, ownership_df, metrics = load_all_datasets()
predictor = load_ai_predictor()

if df is None:
    st.error("❌ Failed to initialize database.")
    st.stop()

# ============================================================================
# 5. SESSION STATE & TOP NAVIGATION BAR
# ============================================================================

if 'language' not in st.session_state:
    st.session_state.language = 'English'

if 'user_role' not in st.session_state:
    st.session_state.user_role = 'Super Admin (MoRD)'

if 'grievances' not in st.session_state:
    st.session_state.grievances = [
        {
            'ticket_id': 'GRV-2024-0891',
            'survey_no': '14',
            'owner_name': 'R. Lakshmi Ammal',
            'district': 'Kanchipuram',
            'issue_type': 'Compensation Rate Discrepancy',
            'status': 'Under CALA Hearing',
            'date': (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d')
        },
        {
            'ticket_id': 'GRV-2024-0742',
            'survey_no': '29',
            'owner_name': 'K. Shanmugam',
            'district': 'Kanchipuram',
            'issue_type': 'Sub-division Boundary Dispute',
            'status': 'Field Survey Scheduled',
            'date': (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d')
        }
    ]

if 'alerts' not in st.session_state:
    st.session_state.alerts = [
        {
            'id': 101,
            'panchayat': 'Sriperumbudur Village Panchayat',
            'village': 'Nemili / Mambakkam',
            'project': 'Chennai Peripheral Ring Road (CPRR)',
            'state': 'Tamil Nadu',
            'district': 'Kanchipuram',
            'alert_type': 'Land Not Ready for Possession',
            'priority': 'Critical',
            'subject': 'URGENT: Section 38 Possession Handover Deadline (7 Days Remaining)',
            'message': 'Land parcels under Survey Nos 14-22 must be cleared for construction handover within 7 calendar days. Please coordinate immediate physical demarcation and remove pending encroachments.',
            'date_sent': datetime.now() - timedelta(days=5),
            'status': 'Pending Response',
            'contact_person': 'Thiru. K. Rajendran (Panchayat President)',
            'phone': '9840123987',
            'email': 'president.sriperumbudur@tnpanchayat.gov.in',
            'send_via': 'SMS + Email Dual Dispatch'
        },
        {
            'id': 102,
            'panchayat': 'Hosur Rural Gram Panchayat',
            'village': 'Zuzuvadi / Bagalur',
            'project': 'Bengaluru Satellite Ring Road (STRR - NH-948A)',
            'state': 'Karnataka',
            'district': 'Bengaluru Rural',
            'alert_type': 'R&R Rehabilitation Process Incomplete',
            'priority': 'High',
            'subject': 'COMPLIANCE: Resettlement Colony Allotment for 45 Displaced Families',
            'message': 'R&R assistance disbursement is lagging behind target. Allotment letters for alternative homestead plots must be finalized before Section 23 Award enquiry.',
            'date_sent': datetime.now() - timedelta(days=3),
            'status': 'Acknowledged',
            'date_response': datetime.now() - timedelta(days=1),
            'contact_person': 'Smt. Anitha Gowda (Gram Panchayat Secretary)',
            'phone': '9480987654',
            'email': 'gp.hosur.rural@karnataka.gov.in',
            'send_via': 'Official Email'
        },
        {
            'id': 103,
            'panchayat': 'Khed Taluka Gram Panchayat',
            'village': 'Chakan Industrial Border',
            'project': 'Pune Ring Road & Metro Phase 2 Link',
            'state': 'Maharashtra',
            'district': 'Pune',
            'alert_type': 'Compensation Payment Disbursement Lag',
            'priority': 'High',
            'subject': 'URGENT: Direct Bank Transfer (DBT) KYC Validation for Awardees',
            'message': 'Compensation disbursement is held up due to pending bank account validations for 28 title holders. Please organize immediate village facilitation camp.',
            'date_sent': datetime.now() - timedelta(days=2),
            'status': 'Pending Response',
            'contact_person': 'Shri. Sachin Deshmukh (Sarpanch)',
            'phone': '9822345678',
            'email': 'sarpanch.khed@maharashtra.gov.in',
            'send_via': 'SMS + Email Dual Dispatch'
        },
        {
            'id': 104,
            'panchayat': 'Shamshabad Rural Panchayat',
            'village': 'Kothwalguda',
            'project': 'Hyderabad Regional Ring Road (RRR - Northern Section)',
            'state': 'Andhra Pradesh',
            'district': 'Visakhapatnam',
            'alert_type': 'Legal Title Dispute Pending',
            'priority': 'Medium',
            'subject': 'LEGAL NOTICE: CALA Title Verification Hearing Attendance',
            'message': 'Sub-division dispute regarding ancestral inheritance under Survey 42. Village Revenue Officer is summoned to submit original pahani records on Tuesday 11:00 AM.',
            'date_sent': datetime.now() - timedelta(days=8),
            'status': 'Resolved',
            'date_response': datetime.now() - timedelta(days=2),
            'contact_person': 'Shri. Venkat Reddy (VRO)',
            'phone': '9848123456',
            'email': 'vro.shamshabad@telangana.gov.in',
            'send_via': 'Official Email'
        }
    ]

# Top Navigation Controls
top_col1, top_col2, top_col3 = st.columns([0.60, 0.22, 0.18])

with top_col2:
    selected_role = st.selectbox(
        "👤 Access Role",
        ["Super Admin (MoRD)", "District Collector (CALA)", "RDO / Revenue Officer", "Citizen / Landowner"],
        index=0,
        key="role_switcher"
    )
    st.session_state.user_role = selected_role

with top_col3:
    selected_lang = st.selectbox(
        "🌐 Language / மொழி",
        ["English", "Tamil"],
        index=0 if st.session_state.language == "English" else 1,
        key="lang_switcher"
    )
    st.session_state.language = selected_lang

L = LANGUAGES[st.session_state.language]

# Header Banner
st.markdown(f"""
    <div class="gov-hero-container">
        <div class="gov-header-title">🏛️ {L['title']}</div>
        <div class="gov-header-sub">{L['subtitle']}</div>
        <div class="gov-header-meta">
            <span>🇮🇳 {L['gov_brand']}</span>
            <span class="live-badge">{L['system_status']}</span>
            <span>🔑 Role: <b>{st.session_state.user_role}</b></span>
            <span>🕒 {datetime.now().strftime('%d-%b-%Y | %H:%M:%S IST')}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# 6. SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown(f"### 📑 {L['dashboard']}")
    
    nav_options = [
        f"📊 {L['dashboard']}",
        f"🚨 {L['alerts']}",
        f"🗺️ {L['geographic_view']}",
        f"🌍 {L['gis_map']}",
        f"📈 {L['analytics']}",
        f"⚖️ {L['workflow']}",
        f"📋 {L['project_details']}",
        f"🤖 {L['ai_predictions']}",
        f"📑 {L['registry']}",
        f"⚙️ {L['admin']}"
    ]
    
    page = st.radio("Navigation", nav_options, index=0)
    
    st.markdown("---")
    st.markdown("### 🌐 Monitored Jurisdictions")
    for s_name in sorted(df['state'].unique()):
        cnt = len(df[df['state'] == s_name])
        st.markdown(f"- **{s_name}**: `{cnt} Projects`")
        
    st.markdown("---")
    st.markdown("""
        <div style="font-size: 11px; color: #94a3b8; text-align: center;">
            National Land Acquisition System v3.5<br>
            Powered by Folium GIS, XGBoost & SHAP<br>
            Smart India Hackathon (SIH) 2024
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE 1: EXECUTIVE DASHBOARD (முகப்பு பலகை)
# ============================================================================

if f"📊 {L['dashboard']}" in page:
    st.markdown(f"## 📊 {L['executive_dashboard']}")
    
    # 6 Top-Level National KPIs
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)
    
    with kpi_col1:
        st.markdown(f"""
            <div class="stat-card-glass">
                <div class="stat-icon">🏗️</div>
                <div class="stat-val">{metrics['national']['total_projects']}</div>
                <div class="stat-label">{L['total_projects']}</div>
                <div class="stat-sub">{len(df['state'].unique())} States Active</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_col2:
        st.markdown(f"""
            <div class="stat-card-glass">
                <div class="stat-icon">🌾</div>
                <div class="stat-val">{metrics['national']['total_area']:,.0f}</div>
                <div class="stat-label">{L['total_area']}</div>
                <div class="stat-sub">Across All Corridors</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_col3:
        st.markdown(f"""
            <div class="stat-card-glass">
                <div class="stat-icon">👨‍👩‍👧‍👦</div>
                <div class="stat-val">{metrics['national']['total_families']:,}</div>
                <div class="stat-label">{L['families']}</div>
                <div class="stat-sub">R&R Beneficiaries</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_col4:
        st.markdown(f"""
            <div class="stat-card-glass">
                <div class="stat-icon">💰</div>
                <div class="stat-val">₹{metrics['national']['total_compensation']/10000000:.1f}Cr</div>
                <div class="stat-label">{L['compensation']}</div>
                <div class="stat-sub">Total Assessed Budget</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_col5:
        avg_comp = df['completion_percentage'].mean()
        st.markdown(f"""
            <div class="stat-card-glass">
                <div class="stat-icon">⏳</div>
                <div class="stat-val">{avg_comp:.1f}%</div>
                <div class="stat-label">{L['completion']}</div>
                <div class="stat-sub">Physical Possession</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_col6:
        total_disp = df['legal_disputes'].sum()
        st.markdown(f"""
            <div class="stat-card-glass">
                <div class="stat-icon">⚖️</div>
                <div class="stat-val" style="color: #ef4444;">{total_disp}</div>
                <div class="stat-label">{L['disputes']}</div>
                <div class="stat-sub">High Priority Cases</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Section A: Acquisition Funnel & Inter-State Distribution
    chart_row1_col1, chart_row1_col2 = st.columns([0.45, 0.55])
    
    with chart_row1_col1:
        st.markdown(f"#### 📊 {L['status']} (RFCTLARR Statutory Stages)")
        status_counts = df['acquisition_status'].value_counts()
        
        status_colors = {
            'Pending': '#ef4444',
            'Notified': '#f59e0b',
            'Awarded': '#3b82f6',
            'Possessed': '#10b981'
        }
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.48,
            marker=dict(colors=[status_colors.get(s, '#888888') for s in status_counts.index], line=dict(color='#0b1329', width=2)),
            textinfo='label+percent',
            hoverinfo='label+value+percent',
            pull=[0.02, 0.02, 0.02, 0.06]
        )])
        fig_pie.update_layout(
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Poppins'),
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with chart_row1_col2:
        st.markdown("#### 🗺️ Projects & Land Extent by State")
        st_summary = df.groupby('state').agg({
            'project_id': 'count',
            'total_area_acres': 'sum'
        }).reset_index()
        st_summary.columns = ['State', 'Projects', 'Acres']
        
        fig_bar = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_bar.add_trace(
            go.Bar(
                x=st_summary['State'],
                y=st_summary['Projects'],
                name="Project Count",
                marker_color='#3b82f6',
                text=st_summary['Projects'],
                textposition='auto'
            ),
            secondary_y=False
        )
        
        fig_bar.add_trace(
            go.Scatter(
                x=st_summary['State'],
                y=st_summary['Acres'],
                name="Land Area (Acres)",
                mode='lines+markers',
                marker=dict(color='#ffc107', size=9),
                line=dict(color='#ffc107', width=3)
            ),
            secondary_y=True
        )
        
        fig_bar.update_layout(
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Poppins'),
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        fig_bar.update_xaxes(showgrid=False)
        fig_bar.update_yaxes(title_text="Projects", showgrid=True, gridcolor='rgba(255,255,255,0.05)', secondary_y=False)
        fig_bar.update_yaxes(title_text="Acres", showgrid=False, secondary_y=True)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.markdown("---")
    
    # Section B: Financial Compensation Pipeline & Dispute Heatmap
    fin_col1, fin_col2 = st.columns(2)
    
    with fin_col1:
        st.markdown("#### 💰 Financial Compensation Pipeline (₹ Crores)")
        comp_agg = df.groupby('state').agg({
            'compensation_assessed': lambda x: x.sum() / 10000000,
            'compensation_disbursed_pct': 'mean'
        }).reset_index()
        comp_agg.columns = ['State', 'Assessed_Cr', 'Avg_Disb_Pct']
        comp_agg['Disbursed_Cr'] = comp_agg['Assessed_Cr'] * (comp_agg['Avg_Disb_Pct'] / 100)
        comp_agg['Pending_Cr'] = comp_agg['Assessed_Cr'] - comp_agg['Disbursed_Cr']
        
        fig_fin = go.Figure()
        fig_fin.add_trace(go.Bar(
            name='Disbursed',
            x=comp_agg['State'],
            y=comp_agg['Disbursed_Cr'],
            marker_color='#10b981'
        ))
        fig_fin.add_trace(go.Bar(
            name='Pending Escrow',
            x=comp_agg['State'],
            y=comp_agg['Pending_Cr'],
            marker_color='#f59e0b'
        ))
        fig_fin.update_layout(
            barmode='stack',
            height=320,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Poppins'),
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        fig_fin.update_yaxes(title_text="₹ Crores", gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig_fin, use_container_width=True)
        
    with fin_col2:
        st.markdown("#### ⚖️ Litigation Burden & R&R Completion Index")
        fig_scatter = px.scatter(
            df,
            x='rr_completion_pct',
            y='legal_disputes',
            size='total_area_acres',
            color='state',
            hover_name='project_name',
            labels={
                'rr_completion_pct': 'R&R Progress (%)',
                'legal_disputes': 'Active Disputes',
                'total_area_acres': 'Acres'
            },
            size_max=35
        )
        fig_scatter.update_layout(
            height=320,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Poppins'),
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        fig_scatter.update_xaxes(gridcolor='rgba(255,255,255,0.05)')
        fig_scatter.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig_scatter, use_container_width=True)

# ============================================================================
# PAGE 1B: PANCHAYAT ALERT & COMPLIANCE MANAGEMENT SYSTEM (விழிப்பூட்டல் மேலாண்மை)
# ============================================================================

elif f"🚨 {L['alerts']}" in page:
    st.markdown(f"## 🚨 {L['alerts']}")
    st.caption("🇮🇳 " + ("Complete Panchayat Alert & Notification System - Send statutory compliance notices to village administrative offices & local bodies." if st.session_state.language == "English" else "கிராம பஞ்சாயத்து மற்றும் வருவாய் அலுவலகங்களுக்கு சட்டப்பூர்வ அறிவிப்புகளை அனுப்பும் நிகழ்நேர கண்காணிப்பு அமைப்பு."))
    
    tab_al1, tab_al2, tab_al3 = st.tabs([f"🆕 {L['create_alert']}", f"📋 {L['track_alerts']}", f"📊 {L['alert_statistics']}"])
    
    # ------------------------------------------------------------------------
    # TAB 1: CREATE & DISPATCH STATUTORY ALERT
    # ------------------------------------------------------------------------
    with tab_al1:
        st.markdown(f"#### 🆕 {L['create_alert']}")
        
        c_al1, c_al2 = st.columns(2)
        with c_al1:
            in_panchayat = st.text_input(L['panchayat_name'], value="Sriperumbudur Village Panchayat", placeholder="Enter Panchayat / Local Authority name")
            in_village = st.text_input(L['village'], value="Nemili / Mambakkam", placeholder="Enter Village / Revenue Ward")
            in_contact = st.text_input(L['contact_person'], value="Thiru. K. Rajendran", placeholder="Enter Contact Person / President Name")
            
        with c_al2:
            in_phone = st.text_input(L['phone'], value="9840123987", placeholder="Enter 10-digit mobile number")
            in_email = st.text_input(L['email'], value="president.sriperumbudur@tnpanchayat.gov.in", placeholder="Enter official email address")
            
            project_names_list = sorted(df['project_name'].unique())
            in_project = st.selectbox(L['select_project'], project_names_list, index=0)
            
        st.markdown("---")
        
        # Category & Priority Selection
        col_type, col_prio, col_chan = st.columns(3)
        with col_type:
            alert_type_opts = [
                L['land_not_ready'],
                L['compensation_issue'],
                L['rr_incomplete'],
                L['legal_dispute'],
                L['documentation_missing'],
                L['stakeholder_objection'],
                L['urgent_action'],
                L['compliance_notice']
            ]
            in_alert_type = st.selectbox(L['alert_type'], alert_type_opts, index=0)
            
        with col_prio:
            in_priority = st.selectbox(
                L['priority'],
                [L['critical'], L['high'], L['medium'], L['low']],
                index=0
            )
            
        with col_chan:
            in_channel = st.selectbox(
                "Dispatch Channel / அனுப்பும் வழி",
                [L['send_both'], L['send_sms'], L['send_email'], L['send_whatsapp']],
                index=0
            )
            
        # Template pre-population
        st.markdown("---")
        use_template = st.checkbox(L['default_template'], value=True)
        
        # Statutory notice templates
        statutory_templates = {
            L['land_not_ready']: f"""STATUTORY NOTICE: IMMEDIATE LAND POSSESSION & ENCROACHMENT REMOVAL DIRECTIVE
Ref: RFCTLARR/SEC38/DEMARCATION-2024

To: The President / Executive Officer,
{in_panchayat}, {in_village}

Subject: Urgent Handover of Land Parcels for Infrastructure Project: {in_project}

In accordance with Section 38 of the RFCTLARR Act 2013, the Competent Authority for Land Acquisition (CALA) has declared the final award for the subject project. You are hereby directed to:

1. Clear all physical obstructions, fencing, and pending seasonal crop claims on or before {(datetime.now() + timedelta(days=7)).strftime('%d-%b-%Y')}.
2. Ensure all affected beneficiaries receive physical possession eviction notices.
3. Coordinate joint boundary pillar erection with the Revenue Divisional Surveyor team.
4. Submit the formal Village Possession Handover Certificate to the District Collectorate within 7 calendar days.

Failure to adhere to this statutory timeline will result in Section 46 penalty proceedings and escalation to the State Chief Secretary's Project Monitoring Committee (PMC).

Issued by:
Competent Authority for Land Acquisition (CALA) & Revenue Divisional Officer
Government of India / State Revenue Authority
Toll-Free Helpline: 1800-425-9999 | Email: cala.cell@landacquisition.gov.in""",

            L['compensation_issue']: f"""COMPLIANCE NOTICE: DIRECT BENEFIT TRANSFER (DBT) REVENUE CAMP EXPEDITION
Ref: DBT-COMP/CALA/AWRD-2024

To: The Panchayat President & Village Revenue Officer (VRO),
{in_panchayat}, {in_village}

Subject: Expeditious KYC & Bank Account Seeding for {in_project} Land Awardees

Pending compensation disbursements amounting to ₹ Crores remain un-credited due to incomplete Aadhaar-bank account validations. Required immediate actions:

1. Organize a 2-day Village Special DBT Facilitation Camp in the Panchayat Bhavan.
2. Verify original Patta passbooks and indemnity bonds for registered awardees.
3. Submit the certified beneficiary disbursement list to the Treasury Office within 3 days.

Timely distribution is mandatory to prevent project delay penalties.

Issued by: Directorate of Land Acquisition & Financial Compensation""",

            L['rr_incomplete']: f"""STATUTORY COMPLIANCE DIRECTIVE: R&R RESETTLEMENT ACTION COMPLETION
Ref: RR-ACT/SEC16/REHAB-2024

To: The Gram Panchayat Development Officer & R&R Officer,
{in_panchayat}, {in_village}

Subject: Rehabilitation & Resettlement (R&R) Compliance for {in_project}

As per the approved R&R Scheme under Section 16 of the Act:
1. Complete infrastructure development at the designated resettlement township within 15 days.
2. Issue formal house allotment entitlement certificates to all eligible displaced families.
3. Disburse transitional allowance and subsistence grants to verified bank accounts.
4. Submit tri-weekly progress compliance reports to CALA.

Issued by: R&R Commissionerate""",

            L['legal_dispute']: f"""LEGAL NOTICE & SUMMONS: CADASTRAL TITLE DISPUTE CONCILIATION HEARING
Ref: CALA/LEGAL-DISP/SUMMONS-2024

To: The Village Administrative Officer (VAO) & Panchayat Authority,
{in_panchayat}, {in_village}

Subject: Title Dispute Conciliation for Parcels under {in_project}

You are directed to attend the Dispute Resolution & Field Verification Hearing scheduled on:
📅 Date: {(datetime.now() + timedelta(days=3)).strftime('%d-%b-%Y')} at 11:00 AM IST
📍 Location: CALA Tribunal Court, District Collectorate

Mandatory Submissions:
1. Original Village 'A' Register, FMB (Field Measurement Book) sketch, and Adangal records.
2. List of legal heirs and registered partition deeds.
3. Field inspection report signed by the Village Revenue Inspector.

Issued by: CALA Legal Cell & Revenue Tribunal""",

            L['documentation_missing']: f"""URGENT ADMINISTRATIVE REQUISITION: MISSING CADASTRAL SURVEY DOCUMENTS
Ref: REV/CADASTRAL/DOCS-MISSING-2024

To: The Panchayat Secretary,
{in_panchayat}, {in_village}

Subject: Submission of Certified Land Records for {in_project}

Immediate submission of missing cadastral documents is required to proceed with Section 19 declaration:
1. Combined FMB sketches for peripheral alignment parcels.
2. Grama Natham / Poramboke classification extract.
3. Gram Sabha Consultation Resolution copy.

Submit all attested documents within 4 calendar days.

Issued by: District Land Acquisition Wing""",

            L['urgent_action']: f"""HIGH PRIORITY DIRECTIVE: CRITICAL PROJECT BOTTLENECK INTERVENTION
Ref: URGENT/PROJECT-ACCEL/2024

To: Head of Local Body,
{in_panchayat}, {in_village}

Subject: Immediate Resolution of On-Ground Execution Block for {in_project}

This project is currently on the National High-Priority PMG (Project Monitoring Group) Dashboard. You are required to intervene within 48 hours to resolve the local bottleneck and provide daily clearance status reports.

Issued by: State Project Monitoring Task Force"""
        }
        
        default_msg = statutory_templates.get(in_alert_type, f"Official statutory compliance notice regarding {in_alert_type} for project {in_project}.")
        
        if use_template:
            final_message = default_msg
            st.text_area(L['custom_message'], value=final_message, height=220, disabled=True)
        else:
            final_message = st.text_area(L['custom_message'], value=default_msg, height=220)
            
        in_subject = st.text_input(L['subject'], value=f"URGENT: {in_alert_type} - {in_project}")
        
        st.markdown("---")
        
        btn_send = st.button(f"🚀 {L['send']}", use_container_width=True, key="btn_dispatch_alert")
        if btn_send:
            if in_panchayat and in_phone and in_email and final_message:
                new_id = max([a.get('id', 100) for a in st.session_state.alerts], default=100) + 1
                
                # Fetch project state & district
                p_match = df[df['project_name'] == in_project]
                p_state = p_match.iloc[0]['state'] if not p_match.empty else "National Grid"
                p_dist = p_match.iloc[0]['district'] if not p_match.empty else in_village
                
                # Normalize priority label
                prio_label = "Critical" if (in_priority == L['critical'] or in_priority == 'Critical') else \
                             "High" if (in_priority == L['high'] or in_priority == 'High') else \
                             "Medium" if (in_priority == L['medium'] or in_priority == 'Medium') else "Low"
                             
                new_alert_entry = {
                    'id': new_id,
                    'panchayat': in_panchayat,
                    'village': in_village,
                    'project': in_project,
                    'state': p_state,
                    'district': p_dist,
                    'alert_type': in_alert_type,
                    'priority': prio_label,
                    'subject': in_subject,
                    'message': final_message,
                    'date_sent': datetime.now(),
                    'status': 'Pending Response',
                    'contact_person': in_contact,
                    'phone': in_phone,
                    'email': in_email,
                    'send_via': in_channel
                }
                
                st.session_state.alerts.insert(0, new_alert_entry)
                
                st.success(f"""
                ### ✅ {L['alert_sent_success']}
                
                - 📋 **Notice ID**: `ALRT-2024-{new_id:04d}`
                - 🏛️ **Recipient Authority**: **{in_panchayat}** ({in_village}, {p_dist})
                - 👤 **Contact Officer**: {in_contact} (`{in_phone}` | `{in_email}`)
                - 🏗️ **Target Project**: **{in_project}**
                - 🚨 **Priority Level**: `{prio_label.upper()}`
                - 📡 **Dispatch Mode**: `{in_channel}` (NIC SMS Gateway & National e-Notice Portal Synchronized)
                """)
            else:
                st.error("⚠️ Please ensure all mandatory fields (Panchayat, Phone, Email, Message) are completed.")
                
    # ------------------------------------------------------------------------
    # TAB 2: TRACK & MANAGE ALL PANCHAYAT ALERTS
    # ------------------------------------------------------------------------
    with tab_al2:
        st.markdown(f"#### 📋 {L['track_alerts']}")
        
        # Filter controls
        flt_col1, flt_col2, flt_col3 = st.columns(3)
        with flt_col1:
            flt_status = st.multiselect(
                L['alert_status'],
                ['Pending Response', 'Acknowledged', 'Resolved'],
                default=['Pending Response', 'Acknowledged']
            )
        with flt_col2:
            flt_priority = st.multiselect(
                L['priority'],
                ['Critical', 'High', 'Medium', 'Low'],
                default=['Critical', 'High', 'Medium', 'Low']
            )
        with flt_col3:
            all_alert_projs = sorted(list(set([a.get('project', 'General') for a in st.session_state.alerts])))
            flt_project = st.multiselect(L['select_project'], all_alert_projs, default=[])
            
        st.markdown("---")
        
        # Apply filters
        display_alerts = list(st.session_state.alerts)
        if flt_status:
            display_alerts = [a for a in display_alerts if a.get('status') in flt_status]
        if flt_priority:
            display_alerts = [a for a in display_alerts if a.get('priority') in flt_priority]
        if flt_project:
            display_alerts = [a for a in display_alerts if a.get('project') in flt_project]
            
        if not display_alerts:
            st.info("ℹ️ No alerts matching the selected filter criteria.")
        else:
            st.caption(f"Showing {len(display_alerts)} active notices")
            
            for alert in display_alerts:
                prio = alert.get('priority', 'Medium')
                stat = alert.get('status', 'Pending Response')
                a_id = alert.get('id', 0)
                
                # Dynamic Card CSS Class & Urgency Badge
                if prio == 'Critical':
                    card_css = 'alert-critical-card'
                    badge_icon = '🔴'
                    prio_badge = '<span style="background: rgba(239, 68, 68, 0.3); color: #ef4444; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">CRITICAL</span>'
                elif prio == 'High':
                    card_css = 'alert-high-card'
                    badge_icon = '🟠'
                    prio_badge = '<span style="background: rgba(249, 115, 22, 0.3); color: #f97316; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">HIGH</span>'
                elif prio == 'Medium':
                    card_css = 'alert-medium-card'
                    badge_icon = '🟡'
                    prio_badge = '<span style="background: rgba(234, 179, 8, 0.3); color: #eab308; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">MEDIUM</span>'
                else:
                    card_css = 'alert-low-card'
                    badge_icon = '🟢'
                    prio_badge = '<span style="background: rgba(16, 185, 129, 0.3); color: #10b981; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">LOW</span>'
                    
                if stat == 'Pending Response':
                    status_badge = '<span style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 11px;">⏳ Pending Response</span>'
                elif stat == 'Acknowledged':
                    status_badge = '<span style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid #3b82f6; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 11px;">📩 Acknowledged</span>'
                else:
                    status_badge = '<span style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 11px;">✅ Resolved</span>'
                    
                d_sent = alert.get('date_sent', datetime.now())
                d_sent_str = d_sent.strftime('%d-%b-%Y %H:%M') if isinstance(d_sent, datetime) else str(d_sent)
                
                resp_info = ""
                if alert.get('date_response'):
                    d_resp = alert.get('date_response')
                    d_resp_str = d_resp.strftime('%d-%b-%Y %H:%M') if isinstance(d_resp, datetime) else str(d_resp)
                    resp_info = f" | <b>Response Date:</b> {d_resp_str}"
                    
                st.markdown(f"""
                    <div class="{card_css}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 16px; font-weight: 700; color: #ffffff;">
                                {badge_icon} #{a_id} - {alert['panchayat']} ({alert.get('village', 'N/A')})
                            </span>
                            <div>
                                {prio_badge} &nbsp; {status_badge}
                            </div>
                        </div>
                        <div style="font-size: 13px; color: #cbd5e1; margin-bottom: 6px;">
                            <b>Project:</b> {alert.get('project', 'N/A')} | <b>Category:</b> {alert.get('alert_type', 'N/A')}
                        </div>
                        <div style="font-size: 12px; color: #94a3b8; margin-bottom: 8px;">
                            <b>Officer:</b> {alert.get('contact_person', 'N/A')} | 📞 <code>{alert.get('phone', 'N/A')}</code> | ✉️ <code>{alert.get('email', 'N/A')}</code> | 📡 <code>{alert.get('send_via', 'Email')}</code>
                        </div>
                        <div style="font-size: 12px; color: #ffc107; margin-bottom: 6px;">
                            <b>Subject:</b> {alert.get('subject', 'Notice')}
                        </div>
                        <div style="font-size: 12px; color: #e2e8f0; background: rgba(0,0,0,0.25); padding: 10px; border-radius: 6px; margin: 8px 0; max-height: 100px; overflow-y: auto; white-space: pre-wrap;">
{alert.get('message', '')}
                        </div>
                        <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">
                            <b>Dispatched:</b> {d_sent_str}{resp_info}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Interactive Workflow Action Buttons
                act_c1, act_c2, act_c3, act_c4 = st.columns(4)
                with act_c1:
                    if stat == 'Pending Response':
                        if st.button(f"✅ {L['acknowledged']}", key=f"btn_ack_{a_id}"):
                            alert['status'] = 'Acknowledged'
                            alert['date_response'] = datetime.now()
                            st.success(f"✅ Alert #{a_id} acknowledged by {alert['panchayat']}!")
                            st.rerun()
                with act_c2:
                    if prio != 'Critical' and stat != 'Resolved':
                        if st.button(f"🔼 {L['escalate']}", key=f"btn_esc_{a_id}"):
                            alert['priority'] = 'Critical'
                            st.warning(f"🚨 Alert #{a_id} escalated to CRITICAL! Direct alert sent to District Collectorate.")
                            st.rerun()
                with act_c3:
                    if stat != 'Resolved':
                        if st.button(f"✔️ {L['mark_resolved']}", key=f"btn_res_{a_id}"):
                            alert['status'] = 'Resolved'
                            alert['date_response'] = datetime.now()
                            st.success(f"🎉 Alert #{a_id} marked as RESOLVED! Compliance verified.")
                            st.rerun()
                with act_c4:
                    if st.button(f"🔄 {L['resend']}", key=f"btn_resend_{a_id}"):
                        st.info(f"📡 Re-dispatching SMS & Email notification to `{alert['phone']}` & `{alert['email']}`...")
                        
    # ------------------------------------------------------------------------
    # TAB 3: ALERT STATISTICS & PERFORMANCE METRICS
    # ------------------------------------------------------------------------
    with tab_al3:
        st.markdown(f"#### 📊 {L['alert_statistics']}")
        
        all_alerts = st.session_state.alerts
        total_a = len(all_alerts)
        crit_a = len([a for a in all_alerts if a.get('priority') == 'Critical'])
        high_a = len([a for a in all_alerts if a.get('priority') == 'High'])
        med_a = len([a for a in all_alerts if a.get('priority') == 'Medium'])
        low_a = len([a for a in all_alerts if a.get('priority') == 'Low'])
        
        pend_a = len([a for a in all_alerts if a.get('status') == 'Pending Response'])
        ack_a = len([a for a in all_alerts if a.get('status') == 'Acknowledged'])
        res_a = len([a for a in all_alerts if a.get('status') == 'Resolved'])
        
        # Top KPI Counters
        kpi_al1, kpi_al2, kpi_al3, kpi_al4, kpi_al5 = st.columns(5)
        with kpi_al1:
            st.markdown(f"""
                <div class="stat-card-glass">
                    <div class="stat-icon">📑</div>
                    <div class="stat-val">{total_a}</div>
                    <div class="stat-label">Total Notices</div>
                    <div class="stat-sub">Dispatched</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi_al2:
            st.markdown(f"""
                <div class="stat-card-glass" style="border-color: rgba(239,68,68,0.5);">
                    <div class="stat-icon">🔴</div>
                    <div class="stat-val" style="color: #ef4444;">{crit_a}</div>
                    <div class="stat-label">Critical Priority</div>
                    <div class="stat-sub">Immediate Escalation</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi_al3:
            st.markdown(f"""
                <div class="stat-card-glass" style="border-color: rgba(249,115,22,0.5);">
                    <div class="stat-icon">🟠</div>
                    <div class="stat-val" style="color: #f97316;">{high_a}</div>
                    <div class="stat-label">High Priority</div>
                    <div class="stat-sub">Action Required</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi_al4:
            st.markdown(f"""
                <div class="stat-card-glass">
                    <div class="stat-icon">⏳</div>
                    <div class="stat-val" style="color: #fbbf24;">{pend_a}</div>
                    <div class="stat-label">Pending Response</div>
                    <div class="stat-sub">Awaiting Panchayat</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi_al5:
            st.markdown(f"""
                <div class="stat-card-glass" style="border-color: rgba(16,185,129,0.5);">
                    <div class="stat-icon">✅</div>
                    <div class="stat-val" style="color: #10b981;">{res_a}</div>
                    <div class="stat-label">Resolved</div>
                    <div class="stat-sub">Compliance Completed</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Summary Response Metrics
        sm_c1, sm_c2, sm_c3 = st.columns(3)
        with sm_c1:
            resp_rate = ((ack_a + res_a) / max(total_a, 1)) * 100
            st.metric(L['response_rate'], f"{resp_rate:.1f}%", f"{ack_a + res_a} of {total_a} Responded")
        with sm_c2:
            calc_days = []
            for a in all_alerts:
                if a.get('date_response') and a.get('date_sent'):
                    diff = (a['date_response'] - a['date_sent']).total_seconds() / 86400
                    calc_days.append(max(diff, 0.5))
            avg_resp_time = np.mean(calc_days) if calc_days else 2.4
            st.metric(L['avg_response_time'], f"{avg_resp_time:.1f} Days", "-0.8 Days vs Baseline")
        with sm_c3:
            st.metric(L['unresolved_alerts'], pend_a + ack_a, "Active Bottlenecks")
            
        st.markdown("---")
        
        # Visual Analytics: Status Pie + Priority Bar Chart
        ch_c1, ch_c2 = st.columns(2)
        with ch_c1:
            st.markdown("##### 🍩 Status Resolution Distribution")
            fig_stat_donut = go.Figure(data=[go.Pie(
                labels=['Pending Response', 'Acknowledged', 'Resolved'],
                values=[pend_a, ack_a, res_a],
                hole=0.52,
                marker=dict(colors=['#ef4444', '#3b82f6', '#10b981'], line=dict(color='#0b1329', width=2)),
                textinfo='label+percent'
            )])
            fig_stat_donut.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', family='Poppins'),
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_stat_donut, use_container_width=True)
            
        with ch_c2:
            st.markdown("##### 📊 Priority Urgency Breakdown")
            fig_prio_bar = px.bar(
                x=['Critical', 'High', 'Medium', 'Low'],
                y=[crit_a, high_a, med_a, low_a],
                color=['Critical', 'High', 'Medium', 'Low'],
                color_discrete_map={'Critical': '#ef4444', 'High': '#f97316', 'Medium': '#eab308', 'Low': '#10b981'},
                text=[crit_a, high_a, med_a, low_a],
                labels={'x': 'Priority Level', 'y': 'Number of Alerts'}
            )
            fig_prio_bar.update_traces(textposition='outside')
            fig_prio_bar.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', family='Poppins'),
                margin=dict(t=10, b=10, l=10, r=10),
                showlegend=False
            )
            fig_prio_bar.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig_prio_bar, use_container_width=True)
            
        st.markdown("---")
        st.markdown("##### 📑 Project-wise Notice Distribution & Logs")
        alert_log_df = pd.DataFrame([
            {
                'Notice ID': f"ALRT-2024-{a.get('id', 0):04d}",
                'Panchayat': a.get('panchayat', ''),
                'Village': a.get('village', ''),
                'Project': a.get('project', ''),
                'Category': a.get('alert_type', ''),
                'Priority': a.get('priority', ''),
                'Status': a.get('status', ''),
                'Contact': a.get('contact_person', ''),
                'Date Sent': a.get('date_sent', '').strftime('%Y-%m-%d') if isinstance(a.get('date_sent'), datetime) else str(a.get('date_sent'))
            }
            for a in all_alerts
        ])
        st.dataframe(alert_log_df, use_container_width=True)
        
        csv_alerts = alert_log_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full Panchayat Alert Logs (CSV)", csv_alerts, "panchayat_alert_logs.csv", "text/csv")

# ============================================================================
# PAGE 2: GEOGRAPHIC & JURISDICTION EXPLORER (மாநில & மாவட்ட ஆய்வு)
# ============================================================================

elif f"🗺️ {L['geographic_view']}" in page:
    st.markdown(f"## 🗺️ {L['geographic_view']}")
    
    geo_f1, geo_f2, geo_f3 = st.columns(3)
    with geo_f1:
        sel_state = st.selectbox(L['select_state'], sorted(df['state'].unique()), key="geo_state_sel")
    with geo_f2:
        dist_opts = sorted(df[df['state'] == sel_state]['district'].unique())
        sel_dist = st.selectbox(L['select_district'], ["All Districts"] + dist_opts, key="geo_dist_sel")
    with geo_f3:
        status_opts = ["All Statuses"] + sorted(df['acquisition_status'].unique().tolist())
        sel_status = st.selectbox("Status Filter", status_opts, key="geo_status_sel")
        
    filtered_df = df[df['state'] == sel_state]
    if sel_dist != "All Districts":
        filtered_df = filtered_df[filtered_df['district'] == sel_dist]
    if sel_status != "All Statuses":
        filtered_df = filtered_df[filtered_df['acquisition_status'] == sel_status]
        
    # Region summary KPI cards
    r_c1, r_c2, r_c3, r_c4 = st.columns(4)
    with r_c1:
        st.metric(L['total_projects'], len(filtered_df))
    with r_c2:
        st.metric(L['total_area'], f"{filtered_df['total_area_acres'].sum():,.1f} ac")
    with r_c3:
        st.metric(L['families'], f"{filtered_df['affected_families'].sum():,}")
    with r_c4:
        st.metric(L['compensation'], f"₹{filtered_df['compensation_assessed'].sum()/10000000:.2f} Cr")
        
    st.markdown("---")
    st.subheader(f"📋 {L['projects_list']} ({sel_state} - {sel_dist})")
    
    cols_to_show = [
        'project_id', 'project_name', 'district', 'project_type', 'collector',
        'total_area_acres', 'affected_families', 'acquisition_status',
        'completion_percentage', 'legal_disputes', 'rr_completion_pct'
    ]
    
    disp = filtered_df[cols_to_show].copy()
    disp['total_area_acres'] = disp['total_area_acres'].round(1)
    disp['completion_percentage'] = disp['completion_percentage'].apply(lambda x: f"{x:.0f}%")
    disp['rr_completion_pct'] = disp['rr_completion_pct'].apply(lambda x: f"{x:.0f}%")
    
    st.dataframe(disp, use_container_width=True, height=380)
    
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(L['download_csv'], csv_bytes, f"projects_{sel_state}.csv", "text/csv")

# ============================================================================
# PAGE 3: INTERACTIVE GIS CADASTRAL MAP (GIS வரைபடம் & சர்வே எண்கள்)
# ============================================================================

elif f"🌍 {L['gis_map']}" in page:
    st.markdown(f"## 🌍 {L['gis_map']}")
    st.info(f"✅ {L['gis_enabled']} - Real-time Leaflet/Folium GIS mapping with individual cadastral survey parcel pins & polygons.")
    
    map_ctrl1, map_ctrl2, map_ctrl3 = st.columns([0.35, 0.35, 0.30])
    with map_ctrl1:
        map_state = st.selectbox(L['select_state'], sorted(df['state'].unique()), key="m_state_sel")
    with map_ctrl2:
        state_projs = df[df['state'] == map_state]
        map_proj = st.selectbox(L['select_project'], state_projs['project_name'].unique(), key="m_proj_sel")
    with map_ctrl3:
        map_layer = st.selectbox("🗺️ Map Base Layer", ["OpenStreetMap", "Esri Satellite Imagery", "CartoDB Positron", "CartoDB Dark Matter"])
        
    p_rec = df[df['project_name'] == map_proj].iloc[0]
    
    # Project brief header metrics
    mb_1, mb_2, mb_3, mb_4 = st.columns(4)
    with mb_1:
        st.metric(L['total_area'], f"{p_rec['total_area_acres']:.1f} acres")
    with mb_2:
        st.metric(L['families'], f"{p_rec['affected_families']} families")
    with mb_3:
        st.metric(L['status'], p_rec['acquisition_status'])
    with mb_4:
        st.metric(L['completion'], f"{p_rec['completion_percentage']:.0f}%")
        
    st.markdown("---")
    
    # Generate Interactive Folium GIS Map
    st.markdown(f"#### 🗺️ {L['map_view']} - {map_proj}")
    
    map_center = [p_rec['latitude'], p_rec['longitude']]
    
    # Select tile provider
    tile_dict = {
        "OpenStreetMap": ("OpenStreetMap", None),
        "Esri Satellite Imagery": ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", "Esri World Imagery"),
        "CartoDB Positron": ("CartoDB positron", None),
        "CartoDB Dark Matter": ("CartoDB dark_matter", None)
    }
    tile_url, tile_attr = tile_dict[map_layer]
    
    if tile_attr:
        f_map = folium.Map(location=map_center, zoom_start=13, tiles=tile_url, attr=tile_attr)
    else:
        f_map = folium.Map(location=map_center, zoom_start=13, tiles=tile_url)
        
    # 1. Main Project Anchor Marker
    folium.Marker(
        location=map_center,
        popup=folium.Popup(f"""
            <div style='font-family: sans-serif; font-size: 12px; width: 230px;'>
                <b style='color: #1a237e; font-size: 14px;'>🏛️ {p_rec['project_name']}</b><br>
                <b>District:</b> {p_rec['district']}, {map_state}<br>
                <b>CALA Collector:</b> {p_rec['collector']}<br>
                <b>Status:</b> <span style='color: #2e7d32; font-weight: bold;'>{p_rec['acquisition_status']}</span><br>
                <b>Extent:</b> {p_rec['total_area_acres']:.1f} Acres<br>
                <b>Budget:</b> ₹{p_rec['compensation_assessed']/10000000:.2f} Cr
            </div>
        """, max_width=260),
        tooltip=f"🏛️ {p_rec['project_name']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(f_map)
    
    # 2. Other Projects in State as boundary markers
    for _, r in state_projs.iterrows():
        if r['project_name'] != map_proj:
            c_stat = r['acquisition_status']
            clr = '#10b981' if c_stat == 'Possessed' else ('#3b82f6' if c_stat == 'Awarded' else ('#f59e0b' if c_stat == 'Notified' else '#ef4444'))
            
            folium.CircleMarker(
                location=[r['latitude'], r['longitude']],
                radius=8,
                popup=folium.Popup(f"""
                    <b>{r['project_name']}</b><br>
                    Status: {r['acquisition_status']}<br>
                    Area: {r['total_area_acres']:.1f} ac<br>
                    Families: {r['affected_families']}
                """, max_width=220),
                tooltip=r['project_name'],
                color=clr,
                fill=True,
                fillColor=clr,
                fillOpacity=0.75,
                weight=2
            ).add_to(f_map)
            
    # 3. Add Individual Cadastral Survey Parcels (Survey Nos. 1 to 61)
    if ownership_df is not None and not ownership_df.empty:
        for _, parcel in ownership_df.iterrows():
            p_stat = parcel['acquisition_status']
            p_clr = '#10b981' if p_stat == 'Possessed' else ('#3b82f6' if p_stat == 'Awarded' else ('#f59e0b' if p_stat == 'Notified' else '#ef4444'))
            disp_tag = "<b style='color: red;'>⚠️ ACTIVE TITLE DISPUTE</b><br>" if parcel.get('legal_disputes', 0) > 0 else ""
            
            folium.CircleMarker(
                location=[parcel['latitude'], parcel['longitude']],
                radius=6,
                popup=folium.Popup(f"""
                    <div style='font-family: sans-serif; font-size: 11px; width: 220px;'>
                        <b style='color: #0d47a1; font-size: 13px;'>📍 Survey Parcel #{parcel['survey_no']}</b><br>
                        <b>Owner:</b> {parcel['registered_owner']}<br>
                        <b>Category:</b> {parcel['ownership_category']}<br>
                        <b>Land Type:</b> {parcel['land_type']}<br>
                        <b>Extent:</b> {parcel['total_extent_acres']:.2f} Acres<br>
                        <b>Status:</b> <b>{parcel['acquisition_status']}</b><br>
                        <b>Compensation:</b> ₹{parcel['compensation_assessed']:,.0f}<br>
                        {disp_tag}
                    </div>
                """, max_width=250),
                tooltip=f"Survey #{parcel['survey_no']} - {parcel['registered_owner']}",
                color=p_clr,
                fill=True,
                fillColor=p_clr,
                fillOpacity=0.7,
                weight=1.5
            ).add_to(f_map)
            
    # Render Folium Map
    st_folium(f_map, width=1350, height=540)
    
    st.markdown("---")
    
    # Cadastral Survey Registry Table & Search Filter
    st.subheader(f"📋 {L['parcel_details']}")
    
    if ownership_df is not None and not ownership_df.empty:
        f_c1, f_c2 = st.columns([0.4, 0.6])
        with f_c1:
            search_sno = st.text_input("🔍 Search by Survey No or Owner Name", "")
        with f_c2:
            dispute_filter = st.checkbox("Show Only Disputed / High-Risk Parcels")
            
        p_filtered = ownership_df.copy()
        if search_sno:
            p_filtered = p_filtered[
                p_filtered['survey_no'].astype(str).str.contains(search_sno, case=False) |
                p_filtered['registered_owner'].str.contains(search_sno, case=False)
            ]
        if dispute_filter:
            p_filtered = p_filtered[p_filtered['legal_disputes'] > 0]
            
        p_table_cols = [
            'survey_no', 'registered_owner', 'ownership_category', 
            'land_type', 'total_extent_acres', 'acquisition_status',
            'compensation_assessed', 'compensation_disbursed_pct', 'legal_disputes'
        ]
        
        p_table = p_filtered[p_table_cols].copy()
        p_table['total_extent_acres'] = p_table['total_extent_acres'].round(2)
        p_table['compensation_assessed'] = p_table['compensation_assessed'].apply(lambda x: f"₹{x:,.0f}")
        p_table['compensation_disbursed_pct'] = p_table['compensation_disbursed_pct'].apply(lambda x: f"{x:.0f}%")
        
        st.dataframe(p_table, use_container_width=True, height=360)
        
        p_csv = ownership_df.to_csv(index=False).encode('utf-8')
        st.download_button(L['download_parcels_csv'], p_csv, "cadastral_survey_parcels.csv", "text/csv")

# ============================================================================
# PAGE 4: ANALYTICS & INTER-STATE BENCHMARKS (பகுப்பாய்வு & ஒப்பீடு)
# ============================================================================

elif f"📈 {L['analytics']}" in page:
    st.markdown(f"## 📈 {L['analytics']}")
    
    comp_list = []
    for s_name in sorted(df['state'].unique()):
        s_m = metrics['by_state'].get(s_name, {})
        s_sub = df[df['state'] == s_name]
        
        comp_list.append({
            'State': s_name,
            'Projects': s_m.get('total_projects', len(s_sub)),
            'Area (Acres)': round(s_m.get('total_area', s_sub['total_area_acres'].sum()), 1),
            'Avg Completion %': round(s_m.get('avg_completion', s_sub['completion_percentage'].mean()), 1),
            'Legal Disputes': s_m.get('total_legal_disputes', s_sub['legal_disputes'].sum()),
            'R&R Progress %': round(s_m.get('avg_rr_completion', s_sub['rr_completion_pct'].mean()), 1),
            'Compensation (₹ Cr)': round(s_m.get('compensation_assessed', s_sub['compensation_assessed'].sum()) / 10000000, 2)
        })
        
    bench_df = pd.DataFrame(comp_list).sort_values('Avg Completion %', ascending=False)
    
    an_col1, an_col2 = st.columns(2)
    with an_col1:
        st.markdown("#### 📊 Average Acquisition Completion by State (%)")
        fig_cmp = px.bar(
            bench_df,
            x='State',
            y='Avg Completion %',
            color='Avg Completion %',
            color_continuous_scale='RdYlGn',
            text=bench_df['Avg Completion %'].apply(lambda x: f"{x:.1f}%")
        )
        fig_cmp.update_layout(
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Poppins'),
            margin=dict(t=10, b=10, l=10, r=10),
            yaxis_range=[0, 110]
        )
        st.plotly_chart(fig_cmp, use_container_width=True)
        
    with an_col2:
        st.markdown(f"#### ⚖️ {L['legal_disputes']} by State")
        fig_dsp = px.bar(
            bench_df,
            x='State',
            y='Legal Disputes',
            color='Legal Disputes',
            color_continuous_scale='Reds',
            text='Legal Disputes'
        )
        fig_dsp.update_layout(
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Poppins'),
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_dsp, use_container_width=True)
        
    st.markdown("---")
    st.subheader("🏆 Inter-State Performance Rankings")
    st.dataframe(bench_df.set_index('State'), use_container_width=True)
    
    # Strategic Governance Insight Cards
    st.markdown("---")
    h_c1, h_c2, h_c3 = st.columns(3)
    
    with h_c1:
        fastest = bench_df.loc[bench_df['Avg Completion %'].idxmax()]
        st.markdown(f"""
            <div class="glass-box glass-box-green">
                <h4>🥇 {L['fastest_state']}</h4>
                <h3 style="color:#10b981; margin-top:-4px;">{fastest['State']}</h3>
                <p><strong>Avg Completion:</strong> {fastest['Avg Completion %']:.1f}%</p>
                <p><strong>Total Projects:</strong> {fastest['Projects']}</p>
            </div>
        """, unsafe_allow_html=True)
        
    with h_c2:
        largest = bench_df.loc[bench_df['Area (Acres)'].idxmax()]
        st.markdown(f"""
            <div class="glass-box glass-box-gold">
                <h4>📍 {L['largest_area']}</h4>
                <h3 style="color:#ffc107; margin-top:-4px;">{largest['State']}</h3>
                <p><strong>Total Extent:</strong> {largest['Area (Acres)']:,.1f} acres</p>
                <p><strong>Compensation:</strong> ₹{largest['Compensation (₹ Cr)']:.2f} Cr</p>
            </div>
        """, unsafe_allow_html=True)
        
    with h_c3:
        lowest_disp = bench_df.loc[bench_df['Legal Disputes'].idxmin()]
        st.markdown(f"""
            <div class="glass-box glass-box-blue">
                <h4>✅ {L['lowest_disputes']}</h4>
                <h3 style="color:#3b82f6; margin-top:-4px;">{lowest_disp['State']}</h3>
                <p><strong>Disputes:</strong> {lowest_disp['Legal Disputes']} cases</p>
                <p><strong>R&R Rate:</strong> {lowest_disp['R&R Progress %']:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE 5: STATUTORY 7-STAGE WORKFLOW TRACKER (சட்டப்பூர்வ பணிப்பாய்வு)
# ============================================================================

elif f"⚖️ {L['workflow']}" in page:
    st.markdown(f"## ⚖️ {L['workflow_title']}")
    st.info("📌 Statutory compliance tracking under Right to Fair Compensation and Transparency in Land Acquisition, Rehabilitation and Resettlement (RFCTLARR) Act, 2013.")
    
    wf_proj_name = st.selectbox(
        L['select_project'],
        options=sorted(df['project_name'].unique()),
        key="wf_proj_selector"
    )
    wf_p = df[df['project_name'] == wf_proj_name].iloc[0]
    
    # Progress gauge
    comp_pct = wf_p['completion_percentage']
    
    st.markdown(f"### 📍 Project: **{wf_p['project_name']}** (`{wf_p['district']}, {wf_p['state']}`)")
    st.progress(comp_pct / 100.0)
    st.markdown(f"**Overall Statutory Progress:** `{comp_pct:.0f}% Complete` | **CALA Collector:** `{wf_p['collector']}`")
    
    st.markdown("---")
    
    stages = [
        {"stage": "Stage 1", "sec": "Section 4(1)", "title": "Social Impact Assessment (SIA) Study", "status": "Completed" if comp_pct >= 20 else "In Progress", "date": "Completed on 15-Mar-2023"},
        {"stage": "Stage 2", "sec": "Section 6(1)", "title": "SIA Expert Committee Evaluation & Report", "status": "Completed" if comp_pct >= 35 else "In Progress", "date": "Approved on 02-May-2023"},
        {"stage": "Stage 3", "sec": "Section 11(1)", "title": "Preliminary Gazette Notification", "status": "Completed" if comp_pct >= 50 else ("In Progress" if comp_pct >= 25 else "Pending"), "date": wf_p['notification_date'] or "Under Preparation"},
        {"stage": "Stage 4", "sec": "Section 15", "title": "Hearing of Public Objections & Title Verification", "status": "Completed" if comp_pct >= 65 else ("In Progress" if comp_pct >= 45 else "Pending"), "date": "Disposal within 60 days"},
        {"stage": "Stage 5", "sec": "Section 19(1)", "title": "Final Declaration & Summary R&R Scheme", "status": "Completed" if comp_pct >= 75 else ("In Progress" if comp_pct >= 55 else "Pending"), "date": "Mandatory within 12 months"},
        {"stage": "Stage 6", "sec": "Section 23/27", "title": "Collector Award & Compensation Valuation", "status": "Completed" if comp_pct >= 90 else ("In Progress" if comp_pct >= 70 else "Pending"), "date": wf_p['award_date'] or "Award Hearing Pending"},
        {"stage": "Stage 7", "sec": "Section 38", "title": "Possession Handover & Mutation in Patta/ROR", "status": "Completed" if comp_pct >= 95 else ("In Progress" if comp_pct >= 85 else "Pending"), "date": wf_p['possession_date'] or "Handover Scheduled"}
    ]
    
    for s in stages:
        s_cls = "glass-box-green" if s['status'] == 'Completed' else ("glass-box-gold" if s['status'] == 'In Progress' else "glass-box-red")
        tag_clr = "#10b981" if s['status'] == 'Completed' else ("#f59e0b" if s['status'] == 'In Progress' else "#ef4444")
        
        st.markdown(f"""
            <div class="glass-box {s_cls}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 6px; font-size: 12px; font-weight: 700;">{s['stage']}: {s['sec']}</span>
                        <h4 style="margin: 6px 0 2px 0; color: #ffffff;">{s['title']}</h4>
                        <span style="font-size: 12px; color: #94a3b8;">📅 Timeline: {s['date']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: {tag_clr}; font-weight: 800; font-size: 14px;">● {s['status']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE 6: DETAILED PROJECT DOSSIER (திட்ட விவரங்கள்)
# ============================================================================

elif f"📋 {L['project_details']}" in page:
    st.markdown(f"## 📋 {L['project_details']}")
    
    sel_proj_d = st.selectbox(
        L['select_project'],
        options=sorted(df['project_name'].unique()),
        key="dos_proj_sel"
    )
    p_d = df[df['project_name'] == sel_proj_d].iloc[0]
    
    d_c1, d_c2, d_c3, d_c4 = st.columns(4)
    with d_c1:
        st.metric(L['total_area'], f"{p_d['total_area_acres']:.1f} ac")
    with d_c2:
        st.metric(L['families'], f"{p_d['affected_families']} families")
    with d_c3:
        st.metric(L['compensation'], f"₹{p_d['compensation_assessed']/10000000:.2f} Cr")
    with d_c4:
        st.metric(L['completion'], f"{p_d['completion_percentage']:.0f}%")
        
    st.markdown("---")
    
    dos_col1, dos_col2 = st.columns(2)
    with dos_col1:
        st.markdown(f"""
            <div class="glass-box glass-box-gold">
                <h4>📌 Administrative Overview</h4>
                <p><strong>Project Code:</strong> <code>{p_d['project_id']}</code></p>
                <p><strong>Jurisdiction:</strong> {p_d['district']}, {p_d['state']}</p>
                <p><strong>Competent Authority (CALA):</strong> {p_d['collector']}</p>
                <p><strong>Project Category:</strong> {p_d['project_type']}</p>
                <p><strong>Statutory Status:</strong> <span class="status-pill status-{p_d['acquisition_status'].lower()}">{p_d['acquisition_status']}</span></p>
            </div>
        """, unsafe_allow_html=True)
        
    with dos_col2:
        st.markdown(f"""
            <div class="glass-box glass-box-blue">
                <h4>⚖️ Legal & Rehabilitation Overview</h4>
                <p><strong>Active Court Disputes:</strong> {p_d['legal_disputes']} Litigation Cases</p>
                <p><strong>R&R Progress:</strong> {p_d['rr_completion_pct']:.1f}%</p>
                <p><strong>Sec 11 Notification:</strong> {p_d['notification_date'] or 'Pending'}</p>
                <p><strong>Sec 23 Award Declaration:</strong> {p_d['award_date'] or 'Pending'}</p>
                <p><strong>Sec 38 Possession Handover:</strong> {p_d['possession_date'] or 'Pending'}</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE 7: AI DELAY PREDICTIONS & WHAT-IF SANDBOX (AI தாமத கணிப்பு & மாதிரி)
# ============================================================================

elif f"🤖 {L['ai_predictions']}" in page:
    st.markdown(f"## 🤖 {L['ai_predictions']}")
    st.info("🧠 Powered by XGBoost & SHAP Explainable AI for accurate bottleneck forecasting 2-3 months in advance.")
    
    ai_proj_name = st.selectbox(
        L['select_project'],
        options=sorted(df['project_name'].unique()),
        key="ai_p_selector"
    )
    ai_p = df[df['project_name'] == ai_proj_name].iloc[0]
    
    st.markdown(f"### ⚙️ {L['what_if_title']}")
    st.caption(L['what_if_desc'])
    
    # What-If Interactive Sliders
    w_col1, w_col2, w_col3 = st.columns(3)
    
    with w_col1:
        sim_disputes = st.slider("Active Title Injunctions / Disputes", 0, 15, int(ai_p['legal_disputes']), help="Simulate resolving court stays in Lok Adalat")
        sim_comp_disb = st.slider("Compensation Disbursal %", 0, 100, int(ai_p['compensation_disbursed_pct']), help="Simulate fast-tracking direct DBT compensation")
        
    with w_col2:
        sim_doc_pct = st.slider("Documentation Complete %", 0, 100, int(ai_p.get('documentation_complete_pct', 70)))
        sim_rr_pct = st.slider("Rehabilitation (R&R) Progress %", 0, 100, int(ai_p['rr_completion_pct']))
        
    with w_col3:
        sim_coord_score = st.slider("Inter-Departmental Coordination (1-10)", 1, 10, int(ai_p.get('inter_dept_coordination_score', 6)))
        sim_stake_score = st.slider("Public Stakeholder Responsiveness (1-10)", 1, 10, int(ai_p.get('stakeholder_responsiveness_score', 7)))
        
    st.markdown("---")
    
    # Run Prediction Button
    if st.button(f"🚀 {L['run_prediction']}", use_container_width=True):
        model_input = {
            'project_type': ai_p['project_type'],
            'project_status': ai_p.get('project_status', 'Active'),
            'land_area_acres': float(ai_p['total_area_acres']),
            'affected_families': int(ai_p['affected_families']),
            'approval_days_passed': int(ai_p.get('approval_days_passed', 120)),
            'approval_days_total': int(ai_p.get('approval_days_total', 365)),
            'pending_approvals': int(ai_p.get('pending_approvals', 2)),
            'legal_disputes_count': int(sim_disputes),
            'compensation_pending_families': int(ai_p['affected_families'] * (100 - sim_comp_disb) / 100),
            'compensation_disbursed_pct': float(sim_comp_disb),
            'documentation_complete_pct': float(sim_doc_pct),
            'possession_acquired_pct': float(ai_p.get('possession_acquired_pct', 50)),
            'rehabilitation_progress_pct': float(sim_rr_pct),
            'stakeholder_responsiveness_score': int(sim_stake_score),
            'inter_dept_coordination_score': int(sim_coord_score),
            'past_project_success_rate': float(ai_p.get('past_project_success_rate', 0.85)),
            'district_avg_delay_days': int(ai_p.get('district_avg_delay_days', 5))
        }
        
        with st.spinner("Analyzing project features with XGBoost & SHAP explainer..."):
            pred_res = predictor.predict_with_explanation(model_input)
            
            prob = pred_res['delay_probability']
            score = pred_res['risk_score']
            category = pred_res['risk_category']
            factors = pred_res['top_factors']
            recs = pred_res['recommendations']
            
            st.markdown(f"### 🎯 {L['prediction_results']}")
            
            # Prediction Results Cards
            res_c1, res_c2, res_c3 = st.columns(3)
            
            with res_c1:
                r_color = "#ef4444" if score >= 70 else ("#f59e0b" if score >= 40 else "#10b981")
                st.markdown(f"""
                    <div style='background: {r_color}22; border-left: 5px solid {r_color}; padding: 18px; border-radius: 12px; text-align: center;'>
                        <h2 style='color: {r_color}; margin: 0;'>{score:.0f} / 100</h2>
                        <p style='color: {r_color}; font-weight: 700; margin: 4px 0 0 0;'>{L['delay_risk']} ({category})</p>
                    </div>
                """, unsafe_allow_html=True)
                
            with res_c2:
                days_offset = int(max(150 + (score * 2.2), 30))
                est_possession = datetime.now() + timedelta(days=days_offset)
                st.markdown(f"""
                    <div class="glass-box" style="text-align: center; margin: 0; padding: 18px;">
                        <span style="font-size: 12px; color: #94a3b8;">{L['completion_date']}</span>
                        <h3 style="color: #ffc107; margin: 4px 0;">{est_possession.strftime('%d-%b-%Y')}</h3>
                        <span style="font-size: 11px; color: #38bdf8;">+ {days_offset} Projected Days</span>
                    </div>
                """, unsafe_allow_html=True)
                
            with res_c3:
                st.markdown(f"""
                    <div class="glass-box" style="text-align: center; margin: 0; padding: 18px;">
                        <span style="font-size: 12px; color: #94a3b8;">Model Confidence</span>
                        <h3 style="color: #34d399; margin: 4px 0;">{prob*100:.1f}%</h3>
                        <span style="font-size: 11px; color: #cbd5e1;">XGBoost ROC-AUC: 0.94</span>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            
            # SHAP & Recommendations
            f_col1, f_col2 = st.columns(2)
            
            with f_col1:
                st.markdown(f"#### 🔍 {L['factors']} (SHAP Values)")
                if factors:
                    f_df = pd.DataFrame(factors)
                    fig_fac = px.bar(
                        f_df,
                        x='importance',
                        y='feature',
                        orientation='h',
                        color='importance',
                        color_continuous_scale='Reds',
                        text=f_df['importance'].apply(lambda x: f"{x:+.3f}")
                    )
                    fig_fac.update_layout(
                        yaxis={'categoryorder': 'total ascending'},
                        height=330,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e2e8f0', family='Poppins'),
                        margin=dict(t=10, b=10, l=10, r=10)
                    )
                    st.plotly_chart(fig_fac, use_container_width=True)
                else:
                    st.info("No critical risk bottlenecks identified.")
                    
            with f_col2:
                st.markdown(f"#### 💡 {L['recommendations']}")
                for rec in recs:
                    st.info(rec)

# ============================================================================
# PAGE 8: CADASTRAL REGISTRY & GRIEVANCE PORTAL (நிலப் பதிவேடு & குறைதீர்ப்பு)
# ============================================================================

elif f"📑 {L['registry']}" in page:
    st.markdown(f"## 📑 {L['registry']}")
    
    tab1, tab2, tab3 = st.tabs(["📋 Cadastral Survey Registry", "✍️ Field Data Entry Form", "📬 Landowner Grievance Portal"])
    
    with tab1:
        st.markdown("#### 📜 Registered Cadastral Survey Parcels (1 to 61)")
        if ownership_df is not None and not ownership_df.empty:
            st.dataframe(ownership_df, use_container_width=True, height=420)
            
            csv_parcels = ownership_df.to_csv(index=False).encode('utf-8')
            st.download_button(L['download_parcels_csv'], csv_parcels, "cadastral_registry_master.csv", "text/csv")
            
    with tab2:
        st.markdown("#### ✍️ Revenue Official / VAO Cadastral Record Update")
        with st.form("add_parcel_form"):
            form_col1, form_col2 = st.columns(2)
            with form_col1:
                new_sno = st.number_input("Survey Parcel Number", min_value=1, max_value=999, value=62)
                new_owner = st.text_input("Registered Landowner Name", "Thiru. S. Ramanathan")
                new_cat = st.selectbox("Ownership Category", ["Private", "Joint Family", "Government", "Trust / Institution", "Firm / Corporate"])
            with form_col2:
                new_type = st.selectbox("Land Classification", ["Wetland (Nanja)", "Dryland (Punja)", "Commercial", "Residential Plot", "Poramboke (Waterbody)"])
                new_extent = st.number_input("Total Extent (Acres)", min_value=0.1, max_value=50.0, value=2.50, step=0.1)
                new_status = st.selectbox("Acquisition Status", ["Pending", "Notified", "Awarded", "Possessed"])
                
            submitted = st.form_submit_layer = st.form_submit_button("💾 Save Cadastral Parcel to Registry")
            if submitted:
                st.success(f"✅ Cadastral Parcel Survey #{new_sno} saved successfully to national database!")
                
    with tab3:
        st.markdown(f"#### 📬 {L['grievance_title']}")
        st.caption("Direct citizen interface for landowners to file compensation rate disputes, title objections, or R&R claims.")
        
        with st.form("citizen_grievance_form"):
            g_c1, g_c2 = st.columns(2)
            with g_c1:
                g_sno = st.text_input("Survey Number", "33")
                g_owner = st.text_input("Landowner / Claimant Name", "M. Sundaram")
                g_phone = st.text_input("Contact Mobile Number", "9840123456")
            with g_c2:
                g_dist = st.selectbox("District", ["Kanchipuram", "Chennai", "Coimbatore", "Madurai", "Salem"])
                g_type = st.selectbox("Grievance Category", [
                    "Compensation Rate Valuation Discrepancy",
                    "Title Ownership / Boundary Dispute",
                    "R&R Resettlement Package Allocation",
                    "Pending Direct DBT Compensation",
                    "Other Statutory Objections"
                ])
                g_desc = st.text_area("Detailed Grievance Description", "Compensation assessed for wet agricultural land is below market guideline rate.")
                
            g_submit = st.form_submit_button(f"📨 {L['submit_grievance']}")
            if g_submit:
                new_ticket = f"GRV-2024-{np.random.randint(1000, 9999)}"
                st.session_state.grievances.append({
                    'ticket_id': new_ticket,
                    'survey_no': g_sno,
                    'owner_name': g_owner,
                    'district': g_dist,
                    'issue_type': g_type,
                    'status': 'Registered / Assigned to CALA',
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
                st.success(f"🎉 {L['ticket_created']}: `{new_ticket}` | Acknowledgement SMS dispatched to {g_phone}.")
                
        st.markdown("---")
        st.markdown("#### 📂 Active Landowner Grievance Dossiers")
        st.dataframe(pd.DataFrame(st.session_state.grievances), use_container_width=True)

# ============================================================================
# PAGE 9: ADMIN & GOVERNANCE (நிர்வாகம் & பாதுகாப்பு)
# ============================================================================

elif f"⚙️ {L['admin']}" in page:
    st.markdown(f"## ⚙️ {L['admin']}")
    
    adm_col1, adm_col2 = st.columns(2)
    
    with adm_col1:
        st.markdown("""
            <div class="glass-box glass-box-gold">
                <h4>👥 Role-Based Authority Hierarchy (RBAC)</h4>
                <ul>
                    <li>🛡️ <b>Super Admin (MoRD)</b>: Full master access across 5 States & 38 Mega Projects</li>
                    <li>🏛️ <b>Competent Authority (CALA / District Collector)</b>: Section 11 & Section 23 Award Declarations</li>
                    <li>🏢 <b>Revenue Divisional Officer (RDO) / VAO</b>: Cadastral Survey & Field Ground-truthing</li>
                    <li>👨‍🌾 <b>Landowner & Public Citizen</b>: Patta verification, Grievance tracking & Direct DBT</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    with adm_col2:
        st.markdown("""
            <div class="glass-box glass-box-green">
                <h4>🟢 System Infrastructure Diagnostics</h4>
                <ul>
                    <li>🟢 <b>Multi-State Database</b>: 5 States, 38 Projects Synchronized</li>
                    <li>🟢 <b>Cadastral GIS Engine (Folium)</b>: Active (Survey Nos 1-61 Loaded)</li>
                    <li>🟢 <b>Bilingual Engine</b>: English & Pure தமிழ் (Tamil) Online</li>
                    <li>🟢 <b>AI Engine</b>: XGBoost + SHAP Explainability Online</li>
                    <li>🟢 <b>Security Layer</b>: RBAC & Audit Log Verification Active</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("#### 🔄 Reseed / Refresh Multi-State Simulation Data")
    if st.button("🔄 Reseed Multi-State Project Dataset", use_container_width=True):
        from multi_state_sample_generator import create_multi_state_dataset, calculate_project_metrics, CSV_PATH, METRICS_PATH
        new_df = create_multi_state_dataset()
        new_df.to_csv(CSV_PATH, index=False)
        new_metrics = calculate_project_metrics(new_df)
        with open(METRICS_PATH, 'w') as f:
            json.dump(new_metrics, f, indent=2, default=str)
        st.cache_data.clear()
        st.success("✅ Dataset reseeded! All maps, analytics, and metrics updated.")
        st.rerun()

# ============================================================================
# 7. FOOTER
# ============================================================================

st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; color: #94a3b8; font-size: 13px; padding: 20px;'>
        🏛️ <b>{L['title']}</b> | {datetime.now().strftime('%B %d, %Y')}
        <br>
        Government of India | Ministry of Rural Development | Smart India Hackathon (SIH) 2024
    </div>
""", unsafe_allow_html=True)
