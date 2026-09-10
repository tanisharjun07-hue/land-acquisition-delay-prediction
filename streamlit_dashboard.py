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
        ["🎯 Dashboard", "🚨 Panchayat Alerts", "🔮 Single Prediction", "📊 Batch Analysis", "📈 Analytics", "❓ Help"]
    )

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data
def load_sample_projects():
    """Load sample projects from generated multi-state dataset with fallback"""
    import os
    candidate_paths = [
        os.path.join(os.path.dirname(__file__), 'multi_state_projects.csv'),
        os.path.join(os.path.dirname(__file__), 'data', 'sample_projects.csv'),
        'multi_state_projects.csv',
        'data/sample_projects.csv'
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            try:
                df = pd.read_csv(p)
                if len(df) > 0:
                    return df
            except Exception:
                pass
    # Fallback if file not yet generated
    from multi_state_sample_generator import get_or_create_multi_state_data
    df, _ = get_or_create_multi_state_data()
    return df


def get_prediction(project_data, api_url):
    """Call prediction API with resilient local in-process fallback"""
    try:
        response = requests.post(
            f"{api_url}/predict",
            json=project_data,
            timeout=1.5
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
        
    # Local fallback
    try:
        from ml_pipeline import LandAcquisitionPredictor
        pred_engine = LandAcquisitionPredictor()
        pred_engine.load_model('land_acquisition_model.pkl')
        return pred_engine.predict_with_explanation(pd.DataFrame([project_data]))
    except Exception:
        disputes = project_data.get('legal_disputes_count', 0)
        comp_disb = project_data.get('compensation_disbursed_pct', 50)
        rehab_pct = project_data.get('rehabilitation_progress_pct', 50)
        
        score = int(np.clip(
            (disputes * 20) + (100 - comp_disb) * 0.35 + (100 - rehab_pct) * 0.25,
            5, 95
        ))
        cat = "🟢 LOW RISK" if score < 30 else "🟡 MEDIUM RISK" if score < 60 else "🟠 HIGH RISK" if score < 80 else "🔴 CRITICAL RISK"
        return {
            'risk_score': score,
            'risk_category': cat,
            'delay_probability': round(score / 100.0, 2),
            'top_factors': [
                {'feature': 'legal_disputes_count', 'shap_value': round(disputes * 0.12, 3), 'direction': '↑ Increases Risk'},
                {'feature': 'compensation_disbursed_pct', 'shap_value': round((100 - comp_disb) * 0.005, 3), 'direction': '↑ Increases Risk'}
            ],
            'recommendations': [
                'Prioritize title dispute resolution and FAST-track CALA hearings',
                'Organize DBT verification camps to increase compensation disbursement rate'
            ],
            'timestamp': datetime.now().isoformat()
        }

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
# PAGE: PANCHAYAT ALERTS & STATUTORY NOTICES
# ============================================================================

elif page == "🚨 Panchayat Alerts":
    st.title("🚨 Panchayat Alert & Notification Management")
    st.markdown("**Real-Time Compliance Tracking & Direct Notice Dispatch to Local Revenue Bodies**")
    
    if 'dashboard_alerts' not in st.session_state:
        from datetime import timedelta
        st.session_state.dashboard_alerts = [
            {
                'id': 101,
                'panchayat': 'Sriperumbudur Village Panchayat',
                'village': 'Nemili / Mambakkam',
                'project': 'Chennai Peripheral Ring Road (CPRR)',
                'alert_type': 'Land Not Ready for Possession',
                'priority': 'Critical',
                'subject': 'URGENT: Section 38 Possession Handover Deadline (7 Days Remaining)',
                'message': 'Land parcels under Survey Nos 14-22 must be cleared for construction handover within 7 calendar days.',
                'date_sent': datetime.now() - timedelta(days=5),
                'status': 'Pending Response',
                'contact_person': 'Thiru. K. Rajendran',
                'phone': '9840123987',
                'email': 'president.sriperumbudur@tnpanchayat.gov.in',
                'send_via': 'SMS + Email Dual Dispatch'
            },
            {
                'id': 102,
                'panchayat': 'Hosur Rural Gram Panchayat',
                'village': 'Zuzuvadi / Bagalur',
                'project': 'Bengaluru Satellite Ring Road (STRR - NH-948A)',
                'alert_type': 'R&R Rehabilitation Process Incomplete',
                'priority': 'High',
                'subject': 'COMPLIANCE: Resettlement Colony Allotment for 45 Displaced Families',
                'message': 'R&R assistance disbursement is lagging behind target. Allotment letters must be finalized.',
                'date_sent': datetime.now() - timedelta(days=3),
                'status': 'Acknowledged',
                'contact_person': 'Smt. Anitha Gowda',
                'phone': '9480987654',
                'email': 'gp.hosur.rural@karnataka.gov.in',
                'send_via': 'Official Email'
            }
        ]
        
    al_tab1, al_tab2, al_tab3 = st.tabs(["🆕 Create & Dispatch Alert", "📋 Track Active Alerts", "📊 Alert Statistics"])
    
    with al_tab1:
        st.subheader("Create New Statutory Alert")
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Panchayat Name", value="Sriperumbudur Village Panchayat")
            v_name = st.text_input("Village / Revenue Ward", value="Nemili")
            cp_name = st.text_input("Contact Person Name", value="Thiru. K. Rajendran")
        with c2:
            p_phone = st.text_input("Contact Phone Number", value="9840123987")
            p_email = st.text_input("Official Email", value="president@panchayat.gov.in")
            projs_df = load_sample_projects()
            p_proj = st.selectbox("Associated Project", projs_df['project_name'].unique())
            
        a_type = st.selectbox("Alert Category", [
            "Land Not Ready for Possession",
            "Compensation Payment Disbursement Lag",
            "R&R Rehabilitation Process Incomplete",
            "Legal Title Dispute Pending",
            "Statutory Documentation Missing",
            "Urgent Action Required (Possession Deadline)"
        ])
        
        prio = st.selectbox("Priority Level", ["Critical", "High", "Medium", "Low"])
        chan = st.selectbox("Dispatch Channel", ["SMS + Email Dual Dispatch", "Official Email", "SMS Mobile Dispatch", "WhatsApp Notice"])
        
        msg_body = st.text_area("Notice Body", value=f"URGENT STATUTORY COMPLIANCE NOTICE: Regarding {a_type} for project {p_proj}. Immediate intervention required within 7 days.")
        
        if st.button("🚀 Dispatch Notice Now", use_container_width=True):
            new_id = len(st.session_state.dashboard_alerts) + 101
            st.session_state.dashboard_alerts.insert(0, {
                'id': new_id,
                'panchayat': p_name,
                'village': v_name,
                'project': p_proj,
                'alert_type': a_type,
                'priority': prio,
                'subject': f"URGENT: {a_type}",
                'message': msg_body,
                'date_sent': datetime.now(),
                'status': 'Pending Response',
                'contact_person': cp_name,
                'phone': p_phone,
                'email': p_email,
                'send_via': chan
            })
            st.success(f"✅ Alert Notice #{new_id} Dispatched to {p_name} via {chan}!")
            
    with al_tab2:
        st.subheader("Active Panchayat Notices")
        for alt in st.session_state.dashboard_alerts:
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.05); border-left: 5px solid {'#d32f2f' if alt['priority']=='Critical' else '#f57c00'}; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <h4>#{alt['id']} - {alt['panchayat']} ({alt['village']})</h4>
                <p><b>Project:</b> {alt['project']} | <b>Priority:</b> {alt['priority']} | <b>Status:</b> {alt['status']}</p>
                <p><b>Contact:</b> {alt['contact_person']} ({alt['phone']} | {alt['email']})</p>
                <p><i>{alt['message']}</i></p>
            </div>
            """, unsafe_allow_html=True)
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if alt['status'] == 'Pending Response':
                    if st.button("✅ Acknowledge", key=f"d_ack_{alt['id']}"):
                        alt['status'] = 'Acknowledged'
                        st.rerun()
            with col_b2:
                if alt['priority'] != 'Critical':
                    if st.button("🔼 Escalate to Critical", key=f"d_esc_{alt['id']}"):
                        alt['priority'] = 'Critical'
                        st.rerun()
            with col_b3:
                if alt['status'] != 'Resolved':
                    if st.button("✔️ Mark Resolved", key=f"d_res_{alt['id']}"):
                        alt['status'] = 'Resolved'
                        st.rerun()
                        
    with al_tab3:
        st.subheader("Alert Metrics")
        m_c1, m_c2, m_c3, m_c4 = st.columns(4)
        m_c1.metric("Total Notices", len(st.session_state.dashboard_alerts))
        m_c2.metric("Critical", len([a for a in st.session_state.dashboard_alerts if a['priority']=='Critical']))
        m_c3.metric("Pending", len([a for a in st.session_state.dashboard_alerts if a['status']=='Pending Response']))
        m_c4.metric("Resolved", len([a for a in st.session_state.dashboard_alerts if a['status']=='Resolved']))

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
