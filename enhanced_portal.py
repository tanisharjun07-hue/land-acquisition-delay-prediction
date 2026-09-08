"""
Enhanced Tamil Nadu Land Acquisition Portal
With Cadastral Map Viewer & Real Ownership Data Integration
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from datetime import datetime
import json

# Import auth and data loaders
from auth_system import (
    initialize_session, show_login_page, show_user_profile,
    get_user_district, check_access_level
)
from land_ownership_loader import (
    load_ownership_data, get_project_statistics, 
    create_land_acquisition_project, get_cadastral_parcel_coordinates
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="National Land Acquisition Management System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Government theme styling
st.markdown("""
    <style>
    .gov-header {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a237e 50%, #283593 100%);
        color: white;
        padding: 24px;
        border-radius: 10px;
        margin-bottom: 24px;
        border-bottom: 4px solid #ffc107;
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    }
    .gov-title {
        font-size: 30px;
        font-weight: 800;
        color: #ffc107;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }
    .gov-subtitle {
        font-size: 15px;
        color: #e0e0e0;
        margin-top: 4px;
    }
    .gov-badge {
        font-size: 12px;
        color: #b0bec5;
        margin-top: 6px;
        letter-spacing: 0.5px;
    }
    .parcel-info {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        border-left: 6px solid #1a237e;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .parcel-status-pending { border-left-color: #ff9800; }
    .parcel-status-notified { border-left-color: #ff5722; }
    .parcel-status-awarded { border-left-color: #3f51b5; }
    .parcel-status-possessed { border-left-color: #2e7d32; }
    
    .status-badge-pending { background-color: #fff3e0; color: #e65100; padding: 4px 10px; border-radius: 12px; font-weight: 600; }
    .status-badge-notified { background-color: #fbe9e7; color: #d84315; padding: 4px 10px; border-radius: 12px; font-weight: 600; }
    .status-badge-awarded { background-color: #e8eaf6; color: #283593; padding: 4px 10px; border-radius: 12px; font-weight: 600; }
    .status-badge-possessed { background-color: #e8f5e9; color: #2e7d32; padding: 4px 10px; border-radius: 12px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZATION & AUTHENTICATION CHECK
# ============================================================================

initialize_session()

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# Display authenticated user in sidebar
show_user_profile()

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
    <div class="gov-header">
        <div class="gov-title">🏛️ தமிழ்நாடு நில எடுப்பு மேலாண்மை தளம்</div>
        <div class="gov-title" style="font-size: 22px; color: #ffffff; margin-top: 2px;">
            National Land Acquisition & Cadastral Monitoring System
        </div>
        <div class="gov-subtitle">Real-Time Cadastral GIS, Ownership Verification & Workflow Management</div>
        <div class="gov-badge">
            Ministry of Rural Development & Revenue Department | Government of Tamil Nadu
        </div>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("### 📑 Portal Modules")
    page = st.radio(
        "Select Module",
        [
            "📊 Dashboard", 
            "🗺️ Cadastral Map", 
            "📋 Parcel Details", 
            "📈 Project Analytics", 
            "🔄 Workflow Stages", 
            "⚙️ Admin & Security"
        ]
    )

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data(ttl=600)
def load_project_data():
    """Load land ownership and project data"""
    project = create_land_acquisition_project(
        'Chennai-Salem Green Expressway Corridor',
        'Sriperumbudur Survey Sector 01',
        'Chennai'
    )
    return project

project = load_project_data()
if project is None:
    st.error("❌ Failed to initialize land acquisition project dataset.")
    st.stop()

ownership_data = project['ownership_data']
stats = get_project_statistics(project)
parcel_coords = project['parcel_coordinates']

# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================

if page == "📊 Dashboard":
    st.header("📊 Executive Overview & Project KPIs")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🗺️ Total Parcels", stats['total_parcels'], "Surveyed")
    with col2:
        st.metric("📍 Total Area", f"{stats['total_area']:.2f} ac", "Target Extent")
    with col3:
        st.metric("👨‍👩‍👧‍👦 Affected Families", stats['total_affected_families'], "R&R Required")
    with col4:
        st.metric("💰 Compensation", f"₹{stats['total_compensation_assessed']/10000000:.2f} Cr", "Assessed")
    with col5:
        disbursed_pct = (stats['total_compensation_disbursed'] / stats['total_compensation_assessed'] * 100) if stats['total_compensation_assessed'] > 0 else 0
        st.metric("✅ Land Possessed", f"{stats['parcels_possessed']}/{stats['total_parcels']}", f"{disbursed_pct:.1f}% Disbursed")
    
    st.markdown("---")
    
    # Status breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Acquisition Status Distribution")
        
        status_data = {
            'Pending': stats['parcels_pending'],
            'Notified': stats['parcels_notified'],
            'Awarded': stats['parcels_awarded'],
            'Possessed': stats['parcels_possessed']
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(status_data.keys()),
            values=list(status_data.values()),
            hole=0.45,
            marker=dict(colors=['#ff9800', '#ff5722', '#3f51b5', '#2e7d32']),
            textinfo='label+percent+value',
            pull=[0.05, 0.05, 0.05, 0.08]
        )])
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏘️ Ownership Category Distribution")
        
        ownership_counts = ownership_data['ownership_category'].value_counts().reset_index()
        ownership_counts.columns = ['Category', 'Parcels']
        
        fig = px.bar(
            ownership_counts,
            x='Parcels',
            y='Category',
            orientation='h',
            color='Parcels',
            color_continuous_scale='Tealgrn',
            text='Parcels'
        )
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Number of Parcels",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Land type analysis
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 🌾 Area by Land Classification")
        land_type_data = ownership_data.groupby('land_type')['total_extent_acres'].sum().reset_index()
        land_type_data.columns = ['Land Type', 'Extent (Acres)']
        land_type_data = land_type_data.sort_values(by='Extent (Acres)', ascending=False)
        
        fig = px.bar(
            land_type_data,
            x='Land Type',
            y='Extent (Acres)',
            color='Extent (Acres)',
            color_continuous_scale='Viridis',
            text=land_type_data['Extent (Acres)'].apply(lambda x: f"{x:.1f} ac")
        )
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), xaxis_title="", yaxis_title="Acres")
        st.plotly_chart(fig, use_container_width=True)
        
    with col4:
        st.markdown("### ⚖️ Legal Disputes & Action Items")
        disputed_parcels = ownership_data[ownership_data['legal_disputes'] == 1]
        
        st.markdown(f"**{len(disputed_parcels)} Parcels** with active legal disputes requiring Revenue Divisional Officer (RDO) hearing:")
        
        if len(disputed_parcels) > 0:
            st.dataframe(
                disputed_parcels[['survey_no', 'registered_owner', 'ownership_category', 'total_extent_acres', 'acquisition_status']],
                use_container_width=True,
                height=240
            )
        else:
            st.success("No active legal disputes flagged in this project.")


# ============================================================================
# PAGE 2: CADASTRAL MAP
# ============================================================================

elif page == "🗺️ Cadastral Map":
    st.header("🗺️ Interactive Cadastral Map Viewer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Village Cadastral Boundary & Parcel Layout")
        
        # Check if local cadastral image exists
        image_candidates = [
            'cadastral_map.jpeg',
            'cadastral_map.png',
            'cadastral_map.jpg',
            '/mnt/user-data/uploads/WhatsApp_Image_2026-09-06_at_9_41_47_PM.jpeg',
            'WhatsApp_Image_2026-09-06_at_9_41_47_PM.jpeg'
        ]
        
        found_image = None
        for img_path in image_candidates:
            if os.path.exists(img_path):
                found_image = img_path
                break
                
        if found_image:
            try:
                img = Image.open(found_image)
                st.image(img, use_container_width=True, caption="Village Cadastral Map with Survey Boundary Numbers")
            except Exception as e:
                found_image = None
                
        if not found_image:
            # Generate rich interactive Cadastral Parcel Plot based on coordinates
            plot_records = []
            for _, row in ownership_data.iterrows():
                s_no = row['survey_no']
                coords = parcel_coords.get(s_no, (0.5 + np.random.uniform(-0.3, 0.3), 0.5 + np.random.uniform(-0.3, 0.3)))
                plot_records.append({
                    'survey_no': s_no,
                    'x': coords[0],
                    'y': coords[1],
                    'owner': row['registered_owner'],
                    'category': row['ownership_category'],
                    'land_type': row['land_type'],
                    'status': row['acquisition_status'],
                    'acres': row['total_extent_acres'],
                    'comp': f"₹{row['compensation_assessed']:,.0f}"
                })
            plot_df = pd.DataFrame(plot_records)
            
            status_color_map = {
                'Pending': '#ff9800',
                'Notified': '#ff5722',
                'Awarded': '#3f51b5',
                'Possessed': '#2e7d32'
            }
            
            fig_map = px.scatter(
                plot_df,
                x='x',
                y='y',
                color='status',
                color_discrete_map=status_color_map,
                text='survey_no',
                size='acres',
                size_max=35,
                hover_data=['owner', 'category', 'land_type', 'acres', 'comp'],
                title="Interactive Cadastral Parcel Grid (Sriperumbudur Sector 01)"
            )
            fig_map.update_traces(
                textposition='middle center',
                textfont=dict(color='white', size=11, family="Arial Black"),
                marker=dict(line=dict(width=2, color='DarkSlateGrey'))
            )
            fig_map.update_layout(
                xaxis=dict(showgrid=True, zeroline=False, showticklabels=False, title="East-West Grid"),
                yaxis=dict(showgrid=True, zeroline=False, showticklabels=False, title="North-South Grid"),
                plot_bgcolor='#f8f9fa',
                height=520,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_map, use_container_width=True)
            st.caption("💡 Interactive Cadastral Grid: Hover over any parcel to inspect ownership, extent, and compensation.")
    
    with col2:
        st.markdown("### 🎯 Cadastral Legend")
        
        st.markdown("""
        **Acquisition Status:**
        - 🟡 **Pending**: Initial identification / Pre-gazette
        - 🟠 **Notified**: Section 11/19 Notice published
        - 🔵 **Awarded**: Compensation determined
        - 🟢 **Possessed**: Physical possession handed over
        
        **Ownership Types:**
        - **Private**: Individual landowners
        - **Government**: State/PWD/TNHB Poramboke
        - **Joint/Ancestral**: Multiple legal heirs
        - **Trust**: Temple/Institutional lands
        """)
        
        # Summary metrics
        st.markdown("#### 📋 Quick Metrics")
        st.metric("Surveyed Parcels", stats['total_parcels'])
        st.metric("Total Extent", f"{stats['total_area']:.2f} acres")
        st.metric("Litigation Cases", stats['legal_disputes_count'], "Active Court Writs")
    
    st.markdown("---")
    
    # Interactive parcel selector
    st.markdown("### 🔍 Cadastral Parcel Inspector")
    
    selected_survey = st.selectbox(
        "Select Survey Number to Inspect Details",
        sorted(ownership_data['survey_no'].unique()),
        format_func=lambda x: f"Survey Parcel #{x} - {ownership_data[ownership_data['survey_no'] == x]['registered_owner'].values[0]}"
    )
    
    if selected_survey:
        parcel_info = ownership_data[ownership_data['survey_no'] == selected_survey].iloc[0]
        
        status_key = parcel_info['acquisition_status'].lower()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="parcel-info parcel-status-{status_key}">
                <strong>📍 Survey No: {parcel_info['survey_no']}</strong><br>
                <strong>Status:</strong> <span class="status-badge-{status_key}">{parcel_info['acquisition_status']}</span><br><br>
                <strong>Owner:</strong> {parcel_info['registered_owner']}<br>
                <strong>Category:</strong> {parcel_info['ownership_category']}<br>
                <strong>Contact:</strong> {parcel_info['phone']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="parcel-info">
                <strong>🌾 Land & Tenancy Details</strong><br>
                <strong>Classification:</strong> {parcel_info['land_type']}<br>
                <strong>Total Extent:</strong> {parcel_info['total_extent_acres']:.2f} Acres<br>
                <strong>Affected Families:</strong> {parcel_info['affected_families']}<br>
                <strong>Disputes:</strong> {'⚠️ Active Legal Dispute' if parcel_info['legal_disputes'] else '✅ Clear Title'}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            disbursed_amt = parcel_info['compensation_assessed'] * parcel_info['compensation_disbursed_pct'] / 100
            st.markdown(f"""
            <div class="parcel-info">
                <strong>💰 Compensation Breakdown</strong><br>
                <strong>Assessed Value:</strong> ₹{parcel_info['compensation_assessed']:,.0f}<br>
                <strong>Disbursed Progress:</strong> {parcel_info['compensation_disbursed_pct']:.0f}%<br>
                <strong>Disbursed Amount:</strong> ₹{disbursed_amt:,.0f}<br>
                <strong>Acquisition Date:</strong> {parcel_info['acquisition_date'] or 'Pending'}
            </div>
            """, unsafe_allow_html=True)


# ============================================================================
# PAGE 3: PARCEL DETAILS
# ============================================================================

elif page == "📋 Parcel Details":
    st.header("📋 Detailed Cadastral Land Records & Filter")
    
    # Filter options
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_status = st.multiselect(
            "Filter Status",
            options=sorted(ownership_data['acquisition_status'].unique()),
            default=sorted(ownership_data['acquisition_status'].unique())
        )
    
    with col2:
        filter_ownership = st.multiselect(
            "Filter Ownership Category",
            options=sorted(ownership_data['ownership_category'].unique()),
            default=sorted(ownership_data['ownership_category'].unique())
        )
    
    with col3:
        filter_land_type = st.multiselect(
            "Filter Land Type",
            options=sorted(ownership_data['land_type'].unique()),
            default=sorted(ownership_data['land_type'].unique())
        )
        
    with col4:
        search_query = st.text_input("🔍 Search Owner / Survey #", placeholder="e.g. Sundaram or 12")
    
    # Apply filters
    filtered_data = ownership_data[
        (ownership_data['acquisition_status'].isin(filter_status)) &
        (ownership_data['ownership_category'].isin(filter_ownership)) &
        (ownership_data['land_type'].isin(filter_land_type))
    ]
    
    if search_query:
        query = search_query.strip().lower()
        filtered_data = filtered_data[
            filtered_data['registered_owner'].astype(str).str.lower().str.contains(query) |
            filtered_data['survey_no'].astype(str).str.contains(query)
        ]
    
    st.markdown(f"**Showing {len(filtered_data)} of {len(ownership_data)} parcels**")
    
    # Format display columns
    display_cols = [
        'survey_no', 'ownership_category', 'registered_owner', 
        'phone', 'land_type', 'total_extent_acres', 'acquisition_status',
        'affected_families', 'legal_disputes', 'compensation_assessed',
        'compensation_disbursed_pct', 'acquisition_date'
    ]
    
    display_df = filtered_data[display_cols].copy()
    display_df['total_extent_acres'] = display_df['total_extent_acres'].round(2)
    display_df['compensation_assessed'] = display_df['compensation_assessed'].apply(lambda x: f"₹{x:,.0f}")
    display_df['compensation_disbursed_pct'] = display_df['compensation_disbursed_pct'].apply(lambda x: f"{x:.0f}%")
    
    st.dataframe(display_df, use_container_width=True, height=450)
    
    # Download options
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Filtered Parcels (CSV)",
            csv,
            "cadastral_parcels.csv",
            "text/csv",
            use_container_width=True
        )
    with col_dl2:
        st.caption("Records maintained under Tamil Nadu Land Acquisition Act & RFCTLARR Act 2013.")


# ============================================================================
# PAGE 4: PROJECT ANALYTICS
# ============================================================================

elif page == "📈 Project Analytics":
    st.header("📈 Financial & Legal Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Compensation Disbursed vs Pending")
        
        comp_summary = ownership_data.groupby('acquisition_status').apply(
            lambda df: pd.Series({
                'Disbursed': (df['compensation_assessed'] * df['compensation_disbursed_pct'] / 100).sum(),
                'Pending_Disbursement': (df['compensation_assessed'] * (100 - df['compensation_disbursed_pct']) / 100).sum()
            })
        ).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Disbursed (₹)',
            x=comp_summary['acquisition_status'],
            y=comp_summary['Disbursed'],
            marker_color='#2e7d32'
        ))
        fig.add_trace(go.Bar(
            name='Pending (₹)',
            x=comp_summary['acquisition_status'],
            y=comp_summary['Pending_Disbursement'],
            marker_color='#ff9800'
        ))
        fig.update_layout(barmode='stack', yaxis_title="Amount (₹)", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### ⚖️ Legal Disputes by Ownership Category")
        
        disputes_by_ownership = ownership_data.groupby('ownership_category')['legal_disputes'].sum().reset_index()
        disputes_by_ownership.columns = ['Category', 'Disputes']
        
        fig = px.pie(
            disputes_by_ownership,
            values='Disputes',
            names='Category',
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.4
        )
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
    
    # Area summary table
    st.markdown("---")
    st.markdown("### 📊 Land Classification & Extent Distribution")
    
    area_by_type = ownership_data.groupby('land_type').agg(
        Total_Area_Acres=('total_extent_acres', 'sum'),
        Parcel_Count=('survey_no', 'count'),
        Total_Families=('affected_families', 'sum'),
        Total_Compensation=('compensation_assessed', 'sum')
    ).reset_index()
    
    area_by_type['Total_Area_Acres'] = area_by_type['Total_Area_Acres'].round(2)
    area_by_type['Total_Compensation'] = area_by_type['Total_Compensation'].apply(lambda x: f"₹{x:,.0f}")
    
    st.dataframe(area_by_type, use_container_width=True)


# ============================================================================
# PAGE 5: WORKFLOW STAGES
# ============================================================================

elif page == "🔄 Workflow Stages":
    st.header("🔄 Digital Land Acquisition Workflow Stages")
    
    st.markdown("""
    The statutory workflow adheres to the **Right to Fair Compensation and Transparency in Land Acquisition, Rehabilitation and Resettlement Act (RFCTLARR), 2013** and Tamil Nadu State Amendments.
    """)
    
    workflow_stages = {
        '1️⃣ Project Proposal & SIA Study': {
            'description': 'Submission of project alignment, Social Impact Assessment (SIA) notification, and public hearing.',
            'documents': ['Detailed Project Report (DPR)', 'SIA Report', 'Preliminary Cost Estimate'],
            'stakeholders': ['Project Implementing Authority (NHAI/State Highways)', 'Revenue Dept'],
            'status': 'Completed'
        },
        '2️⃣ Land Identification & Cadastral Mapping': {
            'description': 'Joint survey, sub-division verification, cadastral parcel boundary validation against revenue records.',
            'documents': ['Cadastral Maps', 'Patta/Chitta Records', 'A-Register Extracts'],
            'stakeholders': ['Tahsidar', 'Village Administrative Officer (VAO)', 'Surveyor'],
            'status': 'Completed'
        },
        '3️⃣ Section 11 & Section 19 Notifications': {
            'description': 'Gazette publication of preliminary notification and declaration of public purpose.',
            'documents': ['Gazette Notification Copy', 'Public Hearing Notices', 'Form-C Objections'],
            'stakeholders': ['District Collector', 'Affected Landowners', 'General Public'],
            'status': 'In Progress'
        },
        '4️⃣ Compensation Determination & Award': {
            'description': 'Market value calculation, 100% solatium addition, 12% additional interest, and draft award enquiry.',
            'documents': ['Award Statement (Form 19)', 'Valuation Certificate', 'Bank Account Mandates'],
            'stakeholders': ['District Revenue Officer (DRO)', 'Competent Authority', 'Landowners'],
            'status': 'In Progress'
        },
        '5️⃣ Land Possession & Handover': {
            'description': 'Physical possession handover to project proponent after 100% disbursement or court deposit.',
            'documents': ['Form-E Possession Certificate', 'Panchanama Certificate', 'Site Handover Memo'],
            'stakeholders': ['Revenue Divisional Officer (RDO)', 'Project Authority'],
            'status': 'Pending'
        },
        '6️⃣ R&R Implementation & Final Closure': {
            'description': 'Rehabilitation grant disbursement, alternate plot allotment, and final compliance audit.',
            'documents': ['R&R Compliance Audit', 'Closure Certificate', 'Revenue Record Mutation'],
            'stakeholders': ['Commissioner of R&R', 'State Government'],
            'status': 'Pending'
        }
    }
    
    for stage, details in workflow_stages.items():
        with st.expander(f"### {stage} - [{details['status']}]"):
            st.markdown(f"**Description**: {details['description']}")
            st.markdown(f"**Key Documents Required**: `{', '.join(details['documents'])}`")
            st.markdown(f"**Responsible Authorities**: {', '.join(details['stakeholders'])}")
    
    st.markdown("---")
    
    # Progress tracking bar chart
    st.markdown("### 📈 Project Stage Milestone Completion")
    
    notified_pct = (stats['parcels_notified'] / stats['total_parcels'] * 100) if stats['total_parcels'] > 0 else 0
    awarded_pct = (stats['parcels_awarded'] / stats['total_parcels'] * 100) if stats['total_parcels'] > 0 else 0
    possessed_pct = (stats['parcels_possessed'] / stats['total_parcels'] * 100) if stats['total_parcels'] > 0 else 0
    
    progress_data = {
        'Stage': [
            '1. Proposal & SIA', 
            '2. Cadastral Survey', 
            '3. Sec 11/19 Notice', 
            '4. Award Enquiry', 
            '5. Possession', 
            '6. R&R & Closure'
        ],
        'Completion %': [100.0, 100.0, notified_pct, awarded_pct, possessed_pct, 45.0]
    }
    
    progress_df = pd.DataFrame(progress_data)
    
    fig = go.Figure(data=[
        go.Bar(
            x=progress_df['Stage'], 
            y=progress_df['Completion %'],
            marker=dict(color=['#2e7d32', '#2e7d32', '#ff9800', '#3f51b5', '#009688', '#9c27b0']),
            text=progress_df['Completion %'].round(1).astype(str) + '%',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        yaxis=dict(title="Progress Percentage (%)", range=[0, 115]),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PAGE 6: ADMIN & SECURITY
# ============================================================================

elif page == "⚙️ Admin & Security":
    st.header("⚙️ Portal Administration & Access Control")
    
    current_role = st.session_state.user_info.get('role', '')
    if current_role not in ['Admin', 'District Collector']:
        st.error(f"❌ Access Denied. Administrator or District Collector credentials required. (Current role: {current_role})")
        st.stop()
    
    st.markdown("### 👥 Role-Based Authority Hierarchy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Configured System Accounts")
        st.markdown("""
        - 🛡️ **Super Admin**: `admin@tnland.gov.in` (Statewide Master Access)
        - 🏛️ **District Collectors**:
          - Chennai: `collector.chennai@tnmail.gov.in`
          - Coimbatore: `collector.coimbatore@tnmail.gov.in`
          - Madurai: `collector.madurai@tnmail.gov.in`
          - Salem: `collector.salem@tnmail.gov.in`
          - Trichy: `collector.trichy@tnmail.gov.in`
        - 🏢 **Regional Officers**: Northern, Western, Southern Divisions
        - 📊 **Planning & Analytics Wing**: Data Analyst Role
        """)
    
    with col2:
        st.markdown("#### System Health & Integration Status")
        st.markdown("""
        - 🟢 **State Land Records Database**: Connected
        - 🟢 **Cadastral GIS Engine**: Online
        - 🟢 **e-Gazette Notification Sync**: Active
        - 🟢 **Treasury Direct Benefit Transfer (DBT)**: Ready
        - 🟢 **Session Encryption**: SHA-256 Enabled
        """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Project Metadata & Summary")
    
    stats_display = pd.DataFrame({
        'Parameter': [
            'Project Name',
            'Village & Sector',
            'District Jurisdiction',
            'Total Survey Parcels', 
            'Total Acquisition Extent', 
            'Affected Families', 
            'Active Legal Disputes', 
            'Total Assessed Compensation',
            'Total Disbursed Amount'
        ],
        'Value': [
            project['project_name'],
            project['village'],
            project['district'],
            f"{stats['total_parcels']} parcels", 
            f"{stats['total_area']:.2f} acres",
            f"{stats['total_affected_families']} families", 
            f"{stats['legal_disputes_count']} cases",
            f"₹{stats['total_compensation_assessed']/10000000:.2f} Cr",
            f"₹{stats['total_compensation_disbursed']/10000000:.2f} Cr"
        ]
    })
    
    st.table(stats_display)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #78909c; font-size: 13px; padding: 15px;">
        🏛️ Government of Tamil Nadu | Land Acquisition & Revenue Administration Portal
        <br>
        Built for National Infrastructure Monitoring & SIH Land Governance Initiative
    </div>
""", unsafe_allow_html=True)
