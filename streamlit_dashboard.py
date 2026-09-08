"""
Streamlit Dashboard - Land Acquisition Delay Prediction System
Interactive analytics and prediction interface for government stakeholders
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime
import folium
from streamlit_folium import st_folium

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Land Acquisition Delay Prediction",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .risk-critical { color: #d32f2f; font-weight: bold; }
    .risk-high { color: #f57c00; font-weight: bold; }
    .risk-medium { color: #fbc02d; font-weight: bold; }
    .risk-low { color: #388e3c; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_url = st.text_input(
        "API Base URL",
        value="http://localhost:8000",
        help="FastAPI server URL"
    )
    
    page = st.radio(
        "Navigation",
        ["🎯 Dashboard", "🔮 Single Prediction", "📊 Batch Analysis", "📈 Analytics", "❓ Help"]
    )

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data
def load_sample_projects():
    """Load sample projects for demo"""
    return pd.DataFrame([
        {
            "project_name": "TN Highway Expansion Phase-1",
            "district": "Chennai",
            "state": "Tamil Nadu",
            "project_type": "Highway",
            "land_area_acres": 250,
            "affected_families": 120,
            "approval_days_passed": 90,
            "approval_days_total": 180,
            "pending_approvals": 2,
            "legal_disputes_count": 1,
            "compensation_pending_families": 20,
            "compensation_disbursed_pct": 70,
            "documentation_complete_pct": 85,
            "possession_acquired_pct": 80,
            "rehabilitation_progress_pct": 60,
            "stakeholder_responsiveness_score": 8,
            "inter_dept_coordination_score": 8,
            "past_project_success_rate": 0.85,
            "district_avg_delay_days": -10,
            "project_status": "Active",
            "latitude": 13.0827,
            "longitude": 80.2707
        },
        {
            "project_name": "Railway Station Development",
            "district": "Coimbatore",
            "state": "Tamil Nadu",
            "project_type": "Railway",
            "land_area_acres": 180,
            "affected_families": 95,
            "approval_days_passed": 150,
            "approval_days_total": 360,
            "pending_approvals": 4,
            "legal_disputes_count": 3,
            "compensation_pending_families": 60,
            "compensation_disbursed_pct": 40,
            "documentation_complete_pct": 65,
            "possession_acquired_pct": 45,
            "rehabilitation_progress_pct": 30,
            "stakeholder_responsiveness_score": 3,
            "inter_dept_coordination_score": 2,
            "past_project_success_rate": 0.60,
            "district_avg_delay_days": 150,
            "project_status": "Pending",
            "latitude": 11.0066,
            "longitude": 76.9499
        },
        {
            "project_name": "Water Supply Project",
            "district": "Madurai",
            "state": "Tamil Nadu",
            "project_type": "Water",
            "land_area_acres": 150,
            "affected_families": 80,
            "approval_days_passed": 200,
            "approval_days_total": 365,
            "pending_approvals": 1,
            "legal_disputes_count": 0,
            "compensation_pending_families": 10,
            "compensation_disbursed_pct": 90,
            "documentation_complete_pct": 95,
            "possession_acquired_pct": 95,
            "rehabilitation_progress_pct": 85,
            "stakeholder_responsiveness_score": 9,
            "inter_dept_coordination_score": 9,
            "past_project_success_rate": 0.95,
            "district_avg_delay_days": 5,
            "project_status": "Active",
            "latitude": 9.9252,
            "longitude": 78.1198
        }
    ])

def get_prediction(project_data, api_url):
    """Call prediction API"""
    try:
        response = requests.post(
            f"{api_url}/predict",
            json=project_data,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

def get_risk_color(risk_score):
    """Get color based on risk score"""
    if risk_score < 30:
        return "#388e3c"  # Green
    elif risk_score < 60:
        return "#fbc02d"  # Yellow
    elif risk_score < 80:
        return "#f57c00"  # Orange
    else:
        return "#d32f2f"  # Red

def get_risk_category_emoji(risk_score):
    """Get emoji based on risk score"""
    if risk_score < 30:
        return "🟢"
    elif risk_score < 60:
        return "🟡"
    elif risk_score < 80:
        return "🟠"
    else:
        return "🔴"

# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================

if page == "🎯 Dashboard":
    st.title("🏗️ Land Acquisition Delay Prediction - Dashboard")
    st.markdown("**Smart monitoring for India's infrastructure projects**")
    
    # Load sample data
    projects_df = load_sample_projects()
    
    # Get predictions for all projects
    st.info("📊 Analyzing projects... Please wait.")
    
    predictions = []
    progress_bar = st.progress(0)
    
    for idx, (_, project) in enumerate(projects_df.iterrows()):
        # Create input dict (exclude non-model features)
        model_features = {k: v for k, v in project.items() 
                         if k not in ['project_name', 'district', 'state', 'latitude', 'longitude']}
        
        pred = get_prediction(model_features, api_url)
        if pred:
            pred['project_name'] = project['project_name']
            pred['district'] = project['district']
            pred['state'] = project['state']
            predictions.append(pred)
        
        progress_bar.progress((idx + 1) / len(projects_df))
    
    # Summary metrics
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📍 Total Projects",
            len(predictions),
            "Monitored"
        )
    
    with col2:
        critical = len([p for p in predictions if p['risk_score'] >= 80])
        st.metric(
            "🔴 Critical Risk",
            critical,
            "Immediate Action"
        )
    
    with col3:
        high_risk = len([p for p in predictions if 60 <= p['risk_score'] < 80])
        st.metric(
            "🟠 High Risk",
            high_risk,
            "Attention Needed"
        )
    
    with col4:
        avg_risk = np.mean([p['risk_score'] for p in predictions])
        st.metric(
            "📊 Average Risk Score",
            f"{avg_risk:.0f}",
            "Out of 100"
        )
    
    st.markdown("---")
    
    # Risk distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        risk_scores = [p['risk_score'] for p in predictions]
        
        fig = go.Figure(data=[
            go.Histogram(
                x=risk_scores,
                nbinsx=20,
                marker=dict(color='rgba(55, 83, 109, 0.5)'),
                name='Risk Score Distribution'
            )
        ])
        
        fig.add_vline(x=30, line_dash="dash", line_color="green", annotation_text="Low/Med Threshold")
        fig.add_vline(x=60, line_dash="dash", line_color="orange", annotation_text="Med/High Threshold")
        fig.add_vline(x=80, line_dash="dash", line_color="red", annotation_text="High/Critical Threshold")
        
        fig.update_layout(
            title="Risk Score Distribution",
            xaxis_title="Risk Score (0-100)",
            yaxis_title="Number of Projects",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk category pie chart
        categories = {
            "🟢 Low Risk": len([p for p in predictions if p['risk_score'] < 30]),
            "🟡 Medium Risk": len([p for p in predictions if 30 <= p['risk_score'] < 60]),
            "🟠 High Risk": len([p for p in predictions if 60 <= p['risk_score'] < 80]),
            "🔴 Critical": len([p for p in predictions if p['risk_score'] >= 80])
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(categories.keys()),
            values=list(categories.values()),
            marker=dict(colors=['#388e3c', '#fbc02d', '#f57c00', '#d32f2f'])
        )])
        
        fig.update_layout(title="Risk Category Breakdown", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Projects table
    st.markdown("### 📋 Projects Overview")
    
    projects_table = pd.DataFrame([
        {
            "Project": p['project_name'],
            "Risk": f"{get_risk_category_emoji(p['risk_score'])} {p['risk_score']}/100",
            "Probability": f"{p['delay_probability']:.1%}",
            "Category": p['risk_category'].replace('🟢 ', '').replace('🟡 ', '').replace('🟠 ', '').replace('🔴 ', ''),
            "Status": "⚠️ URGENT" if p['risk_score'] >= 80 else ("⏰ WATCH" if p['risk_score'] >= 60 else "✅ OK")
        }
        for p in sorted(predictions, key=lambda x: x['risk_score'], reverse=True)
    ])
    
    st.dataframe(projects_table, use_container_width=True)
    
    # GIS Map
    st.markdown("### 🗺️ Geographic Distribution")
    
    m = folium.Map(location=[11.1271, 78.6569], zoom_start=7)
    
    for _, project in projects_df.iterrows():
        pred = next((p for p in predictions if p['project_name'] == project['project_name']), None)
        if pred:
            risk_score = pred['risk_score']
            color = get_risk_color(risk_score)
            
            folium.CircleMarker(
                location=[project['latitude'], project['longitude']],
                radius=10,
                popup=f"<b>{project['project_name']}</b><br>Risk: {risk_score}/100",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(m)
    
    st_folium(m, width=700, height=500)

# ============================================================================
# PAGE 2: SINGLE PREDICTION
# ============================================================================

elif page == "🔮 Single Prediction":
    st.title("🔮 Single Project Prediction")
    st.markdown("Enter project details to get delay risk assessment")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_type = st.selectbox("Project Type", ["Highway", "Railway", "Port", "Water", "Power"])
            land_area = st.number_input("Land Area (acres)", min_value=10, value=150)
            affected_families = st.number_input("Affected Families", min_value=0, value=80)
            approval_days_passed = st.slider("Approval Days Passed", 0, 500, 120)
            approval_days_total = st.slider("Total Approval Days", 100, 730, 365)
            pending_approvals = st.slider("Pending Approvals", 0, 10, 2)
        
        with col2:
            legal_disputes = st.slider("Legal Disputes", 0, 10, 1)
            compensation_pending = st.slider("Compensation Pending (families)", 0, 500, 30)
            compensation_pct = st.slider("Compensation Disbursed (%)", 0, 100, 60)
            documentation_pct = st.slider("Documentation Complete (%)", 0, 100, 75)
            possession_pct = st.slider("Land Possession Acquired (%)", 0, 100, 65)
            rehabilitation_pct = st.slider("Rehabilitation Progress (%)", 0, 100, 50)
        
        col3, col4 = st.columns(2)
        
        with col3:
            stakeholder_score = st.slider("Stakeholder Responsiveness (1-10)", 1, 10, 6)
            coordination_score = st.slider("Inter-Dept Coordination (1-10)", 1, 10, 6)
        
        with col4:
            success_rate = st.slider("Past Project Success Rate", 0.0, 1.0, 0.75)
            district_delay = st.slider("District Avg Delay (days)", -100, 300, 50)
        
        submit = st.form_submit_button("🔮 Get Prediction", use_container_width=True)
    
    if submit:
        project_data = {
            "project_type": project_type,
            "land_area_acres": float(land_area),
            "affected_families": int(affected_families),
            "approval_days_passed": int(approval_days_passed),
            "approval_days_total": int(approval_days_total),
            "pending_approvals": int(pending_approvals),
            "legal_disputes_count": int(legal_disputes),
            "compensation_pending_families": int(compensation_pending),
            "compensation_disbursed_pct": float(compensation_pct),
            "documentation_complete_pct": float(documentation_pct),
            "possession_acquired_pct": float(possession_pct),
            "rehabilitation_progress_pct": float(rehabilitation_pct),
            "stakeholder_responsiveness_score": int(stakeholder_score),
            "inter_dept_coordination_score": int(coordination_score),
            "past_project_success_rate": float(success_rate),
            "district_avg_delay_days": int(district_delay),
            "project_status": "Active"
        }
        
        prediction = get_prediction(project_data, api_url)
        
        if prediction:
            # Results display
            col1, col2, col3 = st.columns(3)
            
            with col1:
                risk_emoji = get_risk_category_emoji(prediction['risk_score'])
                st.metric(
                    "Risk Score",
                    f"{risk_emoji} {prediction['risk_score']}/100",
                    prediction['risk_category']
                )
            
            with col2:
                st.metric(
                    "Delay Probability",
                    f"{prediction['delay_probability']:.1%}",
                    "Likelihood of delay"
                )
            
            with col3:
                status = "⚠️ CRITICAL" if prediction['risk_score'] >= 80 else ("⏰ WATCH" if prediction['risk_score'] >= 60 else "✅ ON TRACK")
                st.metric("Status", status)
            
            # Top factors
            st.markdown("### 🔍 Top Contributing Factors")
            
            for i, factor in enumerate(prediction['top_factors'], 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{i}. {factor['feature']}** - {factor['direction']}")
                with col2:
                    st.write(f"Impact: {factor['shap_value']:.3f}")
            
            # Recommendations
            st.markdown("### 💡 Recommended Actions")
            
            for rec in prediction['recommendations']:
                st.info(rec)

# ============================================================================
# PAGE 3: BATCH ANALYSIS
# ============================================================================

elif page == "📊 Batch Analysis":
    st.title("📊 Batch Analysis")
    st.markdown("Analyze multiple projects at once")
    
    # Upload CSV or use sample
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} projects")
        
        st.dataframe(df.head())
    else:
        df = load_sample_projects()
        st.info("📌 Using sample dataset. Upload a CSV file to analyze your own data.")
    
    if st.button("🚀 Analyze All Projects"):
        predictions = []
        progress_bar = st.progress(0)
        
        for idx, (_, project) in enumerate(df.iterrows()):
            model_features = {k: v for k, v in project.items() 
                             if k not in ['project_name', 'district', 'state', 'latitude', 'longitude']}
            
            pred = get_prediction(model_features, api_url)
            if pred:
                pred['project_name'] = project.get('project_name', f"Project {idx+1}")
                predictions.append(pred)
            
            progress_bar.progress((idx + 1) / len(df))
        
        # Download results
        results_df = pd.DataFrame([
            {
                "Project": p['project_name'],
                "Risk Score": p['risk_score'],
                "Category": p['risk_category'],
                "Delay Probability": f"{p['delay_probability']:.1%}"
            }
            for p in predictions
        ])
        
        st.dataframe(results_df, use_container_width=True)
        
        csv = results_df.to_csv(index=False)
        st.download_button(
            "📥 Download Results (CSV)",
            csv,
            "predictions.csv",
            "text/csv"
        )

# ============================================================================
# PAGE 4: ANALYTICS
# ============================================================================

elif page == "📈 Analytics":
    st.title("📈 Advanced Analytics")
    
    st.markdown("### Feature Importance")
    st.info("Shows which factors most influence delay predictions")
    
    try:
        response = requests.get(f"{api_url}/feature_importance?top_n=10")
        if response.status_code == 200:
            features = response.json()['top_features']
            
            importance_df = pd.DataFrame(features)
            
            fig = px.bar(
                importance_df,
                x='importance',
                y='feature',
                orientation='h',
                title="Feature Importance for Delay Prediction",
                labels={'importance': 'Importance Score', 'feature': 'Feature'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.warning("Could not fetch feature importance from API")

# ============================================================================
# PAGE 5: HELP
# ============================================================================

elif page == "❓ Help":
    st.title("❓ Help & Documentation")
    
    st.markdown("""
    ## About This System
    
    The **Land Acquisition Delay Prediction System** uses machine learning to:
    - 🔮 Predict delays in infrastructure projects
    - 🎯 Identify risk factors causing delays
    - 💡 Recommend mitigation strategies
    
    ## How It Works
    
    1. **Data Input**: Enter project details (legal status, compensation, etc.)
    2. **ML Analysis**: XGBoost model analyzes 15+ factors
    3. **Risk Scoring**: Projects ranked 0-100 (100 = highest delay risk)
    4. **Explainability**: SHAP shows which factors drive each prediction
    5. **Recommendations**: Actionable steps to reduce delay probability
    
    ## Risk Categories
    
    - 🟢 **Low Risk (0-30)**: Project on track
    - 🟡 **Medium Risk (30-60)**: Monitor closely
    - 🟠 **High Risk (60-80)**: Intervention recommended
    - 🔴 **Critical (80-100)**: Urgent action required
    
    ## Key Metrics
    
    | Metric | Impact | What to Do |
    |--------|--------|-----------|
    | Legal Disputes | High | Expedite legal clearance |
    | Compensation Pending | High | Prioritize disbursement |
    | Stakeholder Engagement | Medium | Increase coordination |
    | Documentation | Medium | Complete all records |
    | Land Possession | Medium | Resolve ownership disputes |
    
    ## Support
    
    For issues or questions:
    - Check API status: Dashboard → Configuration
    - Verify sample data loads correctly
    - Contact: team@sih-landacquisition.gov.in
    """)

st.markdown("---")
st.markdown("Made with ❤️ for SIH 2024 | Land Acquisition Delay Prediction System")
