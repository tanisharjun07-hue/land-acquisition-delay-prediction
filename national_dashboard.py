"""
National Land Acquisition Management System
Multi-State Dashboard (Sample Data Version for SIH Hackathon)
Comprehensive 5-State Monitoring, Comparative Benchmarking & Digital Workflows
"""

import os
import sys
import json
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Import generator helper for automatic data availability
from multi_state_sample_generator import (
    get_or_create_multi_state_data,
    BASE_DIR, CSV_PATH, METRICS_PATH
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

# Government theme & Rich CSS Styling
st.markdown("""
    <style>
    .gov-header {
        background: linear-gradient(135deg, #0a192f 0%, #1a237e 50%, #283593 100%);
        color: white;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        border-bottom: 4px solid #ffc107;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    .gov-title {
        font-size: 32px;
        font-weight: 800;
        color: #ffc107;
        letter-spacing: 0.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    .gov-subtitle {
        font-size: 16px;
        color: #e0e0e0;
        margin-top: 5px;
    }
    .gov-badge {
        font-size: 12px;
        color: #b0bec5;
        margin-top: 8px;
        letter-spacing: 0.5px;
    }
    .state-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.12);
    }
    .metric-box {
        background: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #1a237e;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .insight-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 18px;
        border: 1px solid #e0e0e0;
        border-top: 4px solid #1a237e;
        margin-bottom: 15px;
    }
    .insight-card-gold {
        border-top: 4px solid #f57f17;
    }
    .insight-card-green {
        border-top: 4px solid #2e7d32;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA WITH CACHE
# ============================================================================

@st.cache_data(ttl=600)
def load_data():
    """Load multi-state sample dataset with fallback generator"""
    return get_or_create_multi_state_data()

try:
    df, metrics = load_data()
except Exception as e:
    st.error(f"❌ Data loading error: {e}. Regenerating...")
    from multi_state_sample_generator import create_multi_state_dataset, calculate_project_metrics
    df = create_multi_state_dataset()
    metrics = calculate_project_metrics(df)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
    <div class="gov-header">
        <div class="gov-title">🏛️ National Land Acquisition Management System</div>
        <div class="gov-subtitle">Real-Time Multi-State Infrastructure Monitoring, Cadastral Tracking & Digital Governance</div>
        <div class="gov-badge">
            Government of India | Ministry of Rural Development & Revenue Departments | Smart India Hackathon (SIH) 2024
        </div>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("### 📑 Navigation Modules")
    page = st.radio(
        "Select Module",
        [
            "📊 National Dashboard",
            "🗺️ State-wise View",
            "📈 Comparative Analytics",
            "🔄 Workflow Tracking",
            "📋 Project Details",
            "⚙️ Data Generator / Refresh"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 🌐 Monitored States")
    for s in sorted(df['state'].unique()):
        cnt = len(df[df['state'] == s])
        st.markdown(f"- **{s}**: `{cnt} Projects`")
        
    st.markdown("---")
    st.caption("🚀 SIH National Hackathon Platform v2.4")

# ============================================================================
# PAGE 1: NATIONAL DASHBOARD
# ============================================================================

if page == "📊 National Dashboard":
    st.header("📊 National Executive Dashboard")
    
    # National KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🏗️ Total Projects",
            f"{metrics['national']['total_projects']}",
            f"{len(df['state'].unique())} States Active"
        )
    with col2:
        st.metric(
            "🌾 Total Area",
            f"{metrics['national']['total_area']:,.0f} ac",
            "Acquisition Target"
        )
    with col3:
        st.metric(
            "👨‍👩‍👧‍👦 Affected Families",
            f"{metrics['national']['total_families']:,}",
            "R&R Monitored"
        )
    with col4:
        st.metric(
            "💰 Compensation",
            f"₹{metrics['national']['total_compensation']/10000000:.2f} Cr",
            "Total Assessed Value"
        )
    with col5:
        avg_comp = df['completion_percentage'].mean()
        st.metric(
            "⏳ Avg Completion",
            f"{avg_comp:.1f}%",
            "Nationwide Average"
        )
    
    st.markdown("---")
    
    # Status breakdown nationally
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Acquisition Status Breakdown (All States)")
        status_counts = df['acquisition_status'].value_counts()
        
        status_colors = {
            'Pending': '#ff9800',
            'Notified': '#ff5722',
            'Awarded': '#3f51b5',
            'Possessed': '#2e7d32'
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.42,
            marker=dict(colors=[status_colors.get(s, '#888888') for s in status_counts.index]),
            textposition='inside',
            textinfo='label+percent+value',
            pull=[0.03, 0.03, 0.03, 0.06]
        )])
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            height=380,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🗺️ Infrastructure Projects by State")
        state_counts = df['state'].value_counts().reset_index()
        state_counts.columns = ['State', 'Projects']
        
        fig = px.bar(
            state_counts,
            x='State',
            y='Projects',
            color='Projects',
            color_continuous_scale='Blues',
            text='Projects'
        )
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            height=380,
            xaxis_title="State Jurisdiction",
            yaxis_title="Project Count"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Compensation and Area analysis
    st.markdown("---")
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("💰 Total Compensation Assessed by State (₹ Crores)")
        comp_by_state = (df.groupby('state')['compensation_assessed'].sum() / 10000000).reset_index()
        comp_by_state.columns = ['State', 'Compensation_Cr']
        comp_by_state = comp_by_state.sort_values('Compensation_Cr', ascending=False)
        
        fig_comp = px.bar(
            comp_by_state,
            x='State',
            y='Compensation_Cr',
            color='Compensation_Cr',
            color_continuous_scale='Tealgrn',
            text=comp_by_state['Compensation_Cr'].apply(lambda x: f"₹{x:.2f} Cr")
        )
        fig_comp.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            height=380,
            xaxis_title="",
            yaxis_title="Amount (₹ Crores)"
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        
    with col_c2:
        st.subheader("🌾 Total Land Area Under Acquisition (Acres)")
        area_by_state = df.groupby('state')['total_area_acres'].sum().reset_index()
        area_by_state.columns = ['State', 'Total_Acres']
        area_by_state = area_by_state.sort_values('Total_Acres', ascending=False)
        
        fig_area = px.bar(
            area_by_state,
            x='State',
            y='Total_Acres',
            color='Total_Acres',
            color_continuous_scale='Viridis',
            text=area_by_state['Total_Acres'].apply(lambda x: f"{x:,.0f} ac")
        )
        fig_area.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            height=380,
            xaxis_title="",
            yaxis_title="Total Land Extent (Acres)"
        )
        st.plotly_chart(fig_area, use_container_width=True)


# ============================================================================
# PAGE 2: STATE-WISE VIEW
# ============================================================================

elif page == "🗺️ State-wise View":
    st.header("🗺️ State-wise Detailed Analysis")
    
    # State selector
    selected_state = st.selectbox(
        "Select State to Inspect",
        sorted(df['state'].unique()),
        key="state_selector"
    )
    
    state_data = df[df['state'] == selected_state]
    state_metrics = metrics['by_state'].get(selected_state, {})
    
    if not state_metrics:
        state_metrics = {
            'total_projects': len(state_data),
            'total_area': state_data['total_area_acres'].sum(),
            'affected_families': state_data['affected_families'].sum(),
            'compensation_assessed': state_data['compensation_assessed'].sum(),
            'avg_completion': state_data['completion_percentage'].mean(),
            'projects_pending': len(state_data[state_data['acquisition_status'] == 'Pending']),
            'projects_notified': len(state_data[state_data['acquisition_status'] == 'Notified']),
            'projects_awarded': len(state_data[state_data['acquisition_status'] == 'Awarded']),
            'projects_possessed': len(state_data[state_data['acquisition_status'] == 'Possessed']),
            'total_legal_disputes': state_data['legal_disputes'].sum(),
            'avg_rr_completion': state_data['rr_completion_pct'].mean(),
        }
    
    # State KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🏗️ Projects", state_metrics['total_projects'])
    with col2:
        st.metric("🌾 Total Extent", f"{state_metrics['total_area']:,.1f} ac")
    with col3:
        st.metric("👨‍👩‍👧‍👦 Families", f"{state_metrics['affected_families']:,}")
    with col4:
        st.metric("💰 Compensation", f"₹{state_metrics['compensation_assessed']/10000000:.2f} Cr")
    with col5:
        st.metric("⚖️ Court Disputes", f"{state_metrics['total_legal_disputes']} Active")
    
    st.markdown("---")
    
    # State status breakdown and R&R Gauge
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📊 Acquisition Status Breakdown: {selected_state}")
        status_data = {
            'Pending': state_metrics['projects_pending'],
            'Notified': state_metrics['projects_notified'],
            'Awarded': state_metrics['projects_awarded'],
            'Possessed': state_metrics['projects_possessed']
        }
        
        fig = go.Figure(data=[go.Bar(
            x=list(status_data.keys()),
            y=list(status_data.values()),
            marker=dict(color=['#ff9800', '#ff5722', '#3f51b5', '#2e7d32']),
            text=list(status_data.values()),
            textposition='outside'
        )])
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            height=360,
            yaxis=dict(title="Number of Projects")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(f"🔧 Rehabilitation & Resettlement (R&R) Progress: {selected_state}")
        
        fig_gauge = go.Figure(data=[go.Indicator(
            mode="gauge+number",
            value=state_metrics['avg_rr_completion'],
            number={'suffix': "%"},
            title={'text': "Average R&R Milestone Completion"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1a237e"},
                'steps': [
                    {'range': [0, 40], 'color': "#ffebee"},
                    {'range': [40, 70], 'color': "#fff8e1"},
                    {'range': [70, 100], 'color': "#e8f5e9"}
                ],
                'threshold': {
                    'line': {'color': "#2e7d32", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        )])
        fig_gauge.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=360)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Projects table for this state
    st.markdown("---")
    st.subheader(f"📋 Registered Land Acquisition Projects in {selected_state}")
    
    display_cols = [
        'project_id', 'project_name', 'district', 'project_type', 'collector',
        'total_area_acres', 'affected_families', 'acquisition_status',
        'completion_percentage', 'legal_disputes', 'rr_completion_pct'
    ]
    
    display_df = state_data[display_cols].copy()
    display_df['total_area_acres'] = display_df['total_area_acres'].round(1)
    display_df['completion_percentage'] = display_df['completion_percentage'].apply(lambda x: f"{x:.0f}%")
    display_df['rr_completion_pct'] = display_df['rr_completion_pct'].apply(lambda x: f"{x:.0f}%")
    
    st.dataframe(display_df, use_container_width=True, height=350)


# ============================================================================
# PAGE 3: COMPARATIVE ANALYTICS
# ============================================================================

elif page == "📈 Comparative Analytics":
    st.header("📈 Multi-State Benchmarking & Performance Analytics")
    
    # Create comparison dataframe
    comp_data = []
    for state in sorted(df['state'].unique()):
        s_m = metrics['by_state'].get(state, {})
        if not s_m:
            s_data = df[df['state'] == state]
            s_m = {
                'total_projects': len(s_data),
                'total_area': s_data['total_area_acres'].sum(),
                'avg_completion': s_data['completion_percentage'].mean(),
                'total_legal_disputes': s_data['legal_disputes'].sum(),
                'avg_rr_completion': s_data['rr_completion_pct'].mean(),
                'compensation_assessed': s_data['compensation_assessed'].sum(),
            }
        comp_data.append({
            'State': state,
            'Projects': s_m['total_projects'],
            'Area (Acres)': round(s_m['total_area'], 1),
            'Avg Completion %': round(s_m['avg_completion'], 1),
            'Disputes': s_m['total_legal_disputes'],
            'R&R Completion %': round(s_m['avg_rr_completion'], 1),
            'Compensation (₹ Cr)': round(s_m['compensation_assessed'] / 10000000, 2)
        })
    
    comp_df = pd.DataFrame(comp_data).sort_values('Area (Acres)', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Average Project Completion Rate by State (%)")
        fig = px.bar(
            comp_df,
            x='State',
            y='Avg Completion %',
            color='Avg Completion %',
            color_continuous_scale='RdYlGn',
            text=comp_df['Avg Completion %'].apply(lambda x: f"{x:.1f}%")
        )
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=360, yaxis_range=[0, 110])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚖️ Total Active Legal & Land Title Disputes")
        fig = px.bar(
            comp_df,
            x='State',
            y='Disputes',
            color='Disputes',
            color_continuous_scale='Reds',
            text='Disputes'
        )
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=360)
        st.plotly_chart(fig, use_container_width=True)
    
    # Comparison table
    st.markdown("---")
    st.subheader("🏆 Inter-State Performance Rankings")
    
    st.dataframe(
        comp_df.set_index('State'),
        use_container_width=True
    )
    
    # Performance insights cards
    st.markdown("---")
    st.subheader("💡 Strategic Insights & Governance Highlights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fastest = comp_df.loc[comp_df['Avg Completion %'].idxmax()]
        st.markdown(f"""
        <div class="insight-card insight-card-green">
            <h4>🥇 Fastest Execution State</h4>
            <h3 style="color:#2e7d32; margin-top: -8px;">{fastest['State']}</h3>
            <p><strong>Avg Completion:</strong> {fastest['Avg Completion %']:.1f}%</p>
            <p><strong>Projects Active:</strong> {fastest['Projects']}</p>
            <p><strong>R&R Progress:</strong> {fastest['R&R Completion %']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        most_area = comp_df.loc[comp_df['Area (Acres)'].idxmax()]
        st.markdown(f"""
        <div class="insight-card insight-card-gold">
            <h4>📍 Largest Land Acquisition Extent</h4>
            <h3 style="color:#f57f17; margin-top: -8px;">{most_area['State']}</h3>
            <p><strong>Total Extent:</strong> {most_area['Area (Acres)']:,.1f} acres</p>
            <p><strong>Projects:</strong> {most_area['Projects']}</p>
            <p><strong>Compensation:</strong> ₹{most_area['Compensation (₹ Cr)']:.2f} Cr</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        least_disputes = comp_df.loc[comp_df['Disputes'].idxmin()]
        st.markdown(f"""
        <div class="insight-card">
            <h4>✅ Lowest Litigation Risk</h4>
            <h3 style="color:#1a237e; margin-top: -8px;">{least_disputes['State']}</h3>
            <p><strong>Disputes:</strong> {least_disputes['Disputes']} cases</p>
            <p><strong>Completion:</strong> {least_disputes['Avg Completion %']:.1f}%</p>
            <p><strong>R&R Rate:</strong> {least_disputes['R&R Completion %']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# PAGE 4: WORKFLOW TRACKING
# ============================================================================

elif page == "🔄 Workflow Tracking":
    st.header("🔄 Multi-State Statutory Workflow Stages")
    
    st.markdown("""
    Tracking the complete statutory acquisition lifecycle adhering to the **RFCTLARR Act 2013** across all 5 participating states.
    """)
    
    total_projects = len(df)
    
    stages_data = {
        '1. Proposal (SIA)': {'count': total_projects, 'percentage': 100.0},
        '2. Joint Scrutiny': {'count': int(total_projects * 0.92), 'percentage': 92.0},
        '3. Sec 11 Notification': {'count': len(df[df['acquisition_status'].isin(['Notified', 'Awarded', 'Possessed'])]), 'percentage': (len(df[df['acquisition_status'].isin(['Notified', 'Awarded', 'Possessed'])]) / total_projects * 100)},
        '4. Award Determination': {'count': len(df[df['acquisition_status'].isin(['Awarded', 'Possessed'])]), 'percentage': (len(df[df['acquisition_status'].isin(['Awarded', 'Possessed'])]) / total_projects * 100)},
        '5. Land Possession': {'count': len(df[df['acquisition_status'] == 'Possessed']), 'percentage': (len(df[df['acquisition_status'] == 'Possessed']) / total_projects * 100)},
        '6. R&R & Closure': {'count': int(len(df[df['rr_completion_pct'] >= 75])), 'percentage': (len(df[df['rr_completion_pct'] >= 75]) / total_projects * 100)}
    }
    
    # Workflow progress chart
    fig = go.Figure(data=[
        go.Bar(
            x=list(stages_data.keys()),
            y=[v['percentage'] for v in stages_data.values()],
            marker=dict(color=['#2e7d32', '#43a047', '#ff9800', '#3f51b5', '#00897b', '#7b1fa2']),
            text=[f"{v['percentage']:.1f}% ({v['count']}/{total_projects})" for v in stages_data.values()],
            textposition='outside'
        )
    ])
    fig.update_layout(
        title="National Workflow Stage Clearance Progress",
        xaxis_title="Statutory Workflow Stages",
        yaxis_title="Stage Clearance Rate (%)",
        yaxis=dict(range=[0, 115]),
        height=400,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # State-wise workflow comparison
    st.markdown("---")
    st.subheader("📊 State-wise Acquisition Status Distribution")
    
    workflow_by_state = pd.crosstab(df['state'], df['acquisition_status'])
    
    status_order = [s for s in ['Pending', 'Notified', 'Awarded', 'Possessed'] if s in workflow_by_state.columns]
    
    fig_w = px.bar(
        workflow_by_state.reset_index(),
        x='state',
        y=status_order,
        title="Project Counts by Current Acquisition Stage",
        barmode='stack',
        color_discrete_map={
            'Pending': '#ff9800',
            'Notified': '#ff5722',
            'Awarded': '#3f51b5',
            'Possessed': '#2e7d32'
        }
    )
    fig_w.update_layout(xaxis_title="State", yaxis_title="Number of Projects", height=420)
    st.plotly_chart(fig_w, use_container_width=True)


# ============================================================================
# PAGE 5: PROJECT DETAILS
# ============================================================================

elif page == "📋 Project Details":
    st.header("📋 Detailed Multi-State Project Database")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_states = st.multiselect(
            "Filter by State",
            sorted(df['state'].unique()),
            default=sorted(df['state'].unique())
        )
    
    with col2:
        selected_status = st.multiselect(
            "Filter by Acquisition Status",
            sorted(df['acquisition_status'].unique()),
            default=sorted(df['acquisition_status'].unique())
        )
    
    with col3:
        min_families = st.slider(
            "Min Affected Families Threshold",
            int(df['affected_families'].min()),
            int(df['affected_families'].max()),
            int(df['affected_families'].min())
        )
    
    # Apply filters
    filtered_df = df[
        (df['state'].isin(selected_states)) &
        (df['acquisition_status'].isin(selected_status)) &
        (df['affected_families'] >= min_families)
    ]
    
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} projects** matching selected criteria:")
    
    # Display table
    display_cols = [
        'project_id', 'project_name', 'state', 'district', 'project_type',
        'total_area_acres', 'affected_families', 'acquisition_status',
        'completion_percentage', 'compensation_assessed', 'legal_disputes',
        'rr_completion_pct'
    ]
    
    display_df = filtered_df[display_cols].copy()
    display_df['total_area_acres'] = display_df['total_area_acres'].round(1)
    display_df['completion_percentage'] = display_df['completion_percentage'].apply(lambda x: f"{x:.0f}%")
    display_df['compensation_assessed'] = display_df['compensation_assessed'].apply(lambda x: f"₹{x/10000000:.2f} Cr")
    display_df['rr_completion_pct'] = display_df['rr_completion_pct'].apply(lambda x: f"{x:.0f}%")
    
    st.dataframe(display_df, use_container_width=True, height=520)
    
    # Export option
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Filtered Projects Dataset (CSV)",
        csv_bytes,
        "multi_state_projects_export.csv",
        "text/csv",
        use_container_width=True
    )


# ============================================================================
# PAGE 6: DATA GENERATOR / REFRESH
# ============================================================================

elif page == "⚙️ Data Generator / Refresh":
    st.header("⚙️ Multi-State Sample Dataset Generator & Simulation")
    
    st.markdown("""
    This utility dynamically regenerates realistic simulated data across **Tamil Nadu, Andhra Pradesh, Maharashtra, Karnataka, and Rajasthan** for live SIH demonstration purposes.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📁 Current Dataset Information")
        st.info(f"""
        - **CSV File**: `{CSV_PATH}`
        - **JSON Metrics**: `{METRICS_PATH}`
        - **Total Records**: {len(df)} projects
        - **States Covered**: {', '.join(sorted(df['state'].unique()))}
        """)
        
        if st.button("🔄 Regenerate & Reseed Dataset", type="primary", use_container_width=True):
            with st.spinner("Generating fresh multi-state dataset..."):
                from multi_state_sample_generator import create_multi_state_dataset, calculate_project_metrics
                new_df = create_multi_state_dataset()
                new_df.to_csv(CSV_PATH, index=False)
                new_metrics = calculate_project_metrics(new_df)
                with open(METRICS_PATH, 'w') as f:
                    json.dump(new_metrics, f, indent=2, default=str)
                st.cache_data.clear()
                st.success("✅ Dataset successfully regenerated and cache cleared! Switch to any tab to see updated figures.")
                st.rerun()
                
    with col2:
        st.markdown("#### 📊 National Summary Snapshot")
        st.json(metrics.get('national', {}))

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #78909c; font-size: 13px; padding: 15px;">
        🏛️ Government of India | Ministry of Rural Development | National Land Acquisition Management System
        <br>
        Smart India Hackathon (SIH) 2024 Solution | Multi-State Enterprise Portal
    </div>
""", unsafe_allow_html=True)
