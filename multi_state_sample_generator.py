"""
Multi-State Land Acquisition Sample Dataset Generator
For SIH Hackathon Demo - September 14
Generates realistic land acquisition data across 5 major Indian states:
Tamil Nadu, Andhra Pradesh, Maharashtra, Karnataka, and Rajasthan.
Includes comprehensive features for both National Monitoring and AI Delay Prediction.
"""

import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Base directory for storing dataset files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

CSV_PATH = os.path.join(BASE_DIR, 'multi_state_projects.csv')
DATA_CSV_PATH = os.path.join(DATA_DIR, 'sample_projects.csv')
DATA_MS_CSV_PATH = os.path.join(DATA_DIR, 'multi_state_projects.csv')
METRICS_PATH = os.path.join(BASE_DIR, 'multi_state_metrics.json')


def _build_project_record(state, state_code, district_name, collector, lat, lon, proj_id, p_name, p_type,
                          area_min, area_max, fam_min, fam_max, comp_min, comp_max, status_probs):
    status = np.random.choice(['Pending', 'Notified', 'Awarded', 'Possessed'], p=status_probs)
    
    total_area = float(round(np.random.uniform(area_min, area_max), 2))
    affected_fam = int(np.random.randint(fam_min, fam_max))
    total_parcels = int(np.random.randint(12, 45))
    
    if status == 'Pending':
        completion = float(round(np.random.uniform(10, 35), 1))
        comp_disb_pct = float(round(np.random.uniform(0, 15), 1))
        possession_pct = float(round(np.random.uniform(0, 20), 1))
        doc_pct = float(round(np.random.uniform(30, 65), 1))
        p_status = 'Pending'
        notif_date = (datetime.now() - timedelta(days=int(np.random.randint(20, 90)))).strftime('%Y-%m-%d')
        award_date = None
        possession_date = None
        pending_appr = int(np.random.randint(3, 7))
        appr_days_passed = int(np.random.randint(45, 150))
        appr_days_total = int(np.random.randint(200, 400))
    elif status == 'Notified':
        completion = float(round(np.random.uniform(35, 65), 1))
        comp_disb_pct = float(round(np.random.uniform(20, 50), 1))
        possession_pct = float(round(np.random.uniform(20, 55), 1))
        doc_pct = float(round(np.random.uniform(65, 85), 1))
        p_status = 'Active'
        notif_date = (datetime.now() - timedelta(days=int(np.random.randint(90, 240)))).strftime('%Y-%m-%d')
        award_date = None
        possession_date = None
        pending_appr = int(np.random.randint(1, 4))
        appr_days_passed = int(np.random.randint(120, 260))
        appr_days_total = int(np.random.randint(250, 450))
    elif status == 'Awarded':
        completion = float(round(np.random.uniform(65, 90), 1))
        comp_disb_pct = float(round(np.random.uniform(55, 90), 1))
        possession_pct = float(round(np.random.uniform(60, 85), 1))
        doc_pct = float(round(np.random.uniform(85, 98), 1))
        p_status = 'Active'
        notif_date = (datetime.now() - timedelta(days=int(np.random.randint(180, 360)))).strftime('%Y-%m-%d')
        award_date = (datetime.now() - timedelta(days=int(np.random.randint(30, 120)))).strftime('%Y-%m-%d')
        possession_date = None
        pending_appr = int(np.random.randint(0, 2))
        appr_days_passed = int(np.random.randint(200, 380))
        appr_days_total = int(np.random.randint(300, 500))
    else: # Possessed
        completion = float(round(np.random.uniform(90, 100), 1))
        comp_disb_pct = float(round(np.random.uniform(90, 100), 1))
        possession_pct = 100.0
        doc_pct = 100.0
        p_status = 'Active'
        notif_date = (datetime.now() - timedelta(days=int(np.random.randint(250, 450)))).strftime('%Y-%m-%d')
        award_date = (datetime.now() - timedelta(days=int(np.random.randint(90, 180)))).strftime('%Y-%m-%d')
        possession_date = (datetime.now() - timedelta(days=int(np.random.randint(10, 80)))).strftime('%Y-%m-%d')
        pending_appr = 0
        appr_days_passed = int(np.random.randint(280, 450))
        appr_days_total = appr_days_passed

    comp_assessed = float(round(np.random.uniform(comp_min, comp_max), 2))
    comp_pending_fam = int(round(affected_fam * (100.0 - comp_disb_pct) / 100.0))
    legal_disputes = int(np.random.randint(0, 5 if status == 'Possessed' else 7))
    
    rr_affected = int(round(affected_fam * np.random.uniform(0.85, 1.0)))
    rr_pct = float(round(np.random.uniform(15, 95) if status != 'Possessed' else np.random.uniform(80, 100), 1))
    rr_completed = int(round(rr_affected * rr_pct / 100.0))
    
    stakeholder_score = int(np.random.randint(3, 9) if status != 'Pending' else np.random.randint(2, 7))
    coord_score = int(np.random.randint(3, 9) if status != 'Pending' else np.random.randint(2, 7))
    success_rate = float(round(np.random.uniform(0.70, 0.96), 2))
    dist_delay = int(np.random.randint(-15, 45))

    return {
        'state': state,
        'state_code': state_code,
        'district': district_name,
        'collector': collector,
        'latitude': float(lat + np.random.uniform(-0.15, 0.15)),
        'longitude': float(lon + np.random.uniform(-0.15, 0.15)),
        
        'project_id': proj_id,
        'project_name': p_name,
        'project_type': p_type,
        
        'total_parcels': total_parcels,
        'total_area_acres': total_area,
        'land_area_acres': total_area,
        'affected_families': affected_fam,
        
        'acquisition_status': status,
        'project_status': p_status,
        'completion_percentage': completion,
        'possession_acquired_pct': possession_pct,
        
        'compensation_assessed': comp_assessed,
        'compensation_disbursed_pct': comp_disb_pct,
        'compensation_pending_families': comp_pending_fam,
        
        'legal_disputes': legal_disputes,
        'legal_disputes_count': legal_disputes,
        
        'approval_days_passed': appr_days_passed,
        'approval_days_total': appr_days_total,
        'pending_approvals': pending_appr,
        
        'documentation_complete_pct': doc_pct,
        'rehabilitation_progress_pct': rr_pct,
        'rr_affected_families': rr_affected,
        'rr_completed_families': rr_completed,
        'rr_completion_pct': rr_pct,
        
        'stakeholder_responsiveness_score': stakeholder_score,
        'inter_dept_coordination_score': coord_score,
        'past_project_success_rate': success_rate,
        'district_avg_delay_days': dist_delay,
        
        'notification_date': notif_date,
        'award_date': award_date,
        'possession_date': possession_date,
    }


def create_tamil_nadu_projects():
    """Tamil Nadu - 8 projects"""
    projects = []
    tn_districts = [
        {'name': 'Chennai', 'lat': 13.0827, 'lon': 80.2707, 'collector': 'Dr. Supradeep Elangeni'},
        {'name': 'Coimbatore', 'lat': 11.0066, 'lon': 76.9499, 'collector': 'Dr. Sudha Sadasivam'},
        {'name': 'Madurai', 'lat': 9.9252, 'lon': 78.1198, 'collector': 'V. Anbuchezhiyan'},
        {'name': 'Salem', 'lat': 11.6643, 'lon': 78.1460, 'collector': 'Suki Eswaran'},
    ]
    project_types = ['Highway', 'Railway', 'Water Supply', 'Power Plant', 'Industrial Corridor']
    
    for i, district in enumerate(tn_districts):
        for j in range(2):
            p_type = np.random.choice(project_types)
            rec = _build_project_record(
                state='Tamil Nadu',
                state_code='TN',
                district_name=district['name'],
                collector=district['collector'],
                lat=district['lat'],
                lon=district['lon'],
                proj_id=f"TN-{i+1:02d}-{j+1:02d}",
                p_name=f"{district['name']} {p_type} Phase {j+1}",
                p_type=p_type,
                area_min=50, area_max=220,
                fam_min=30, fam_max=160,
                comp_min=15000000, comp_max=75000000,
                status_probs=[0.25, 0.30, 0.30, 0.15]
            )
            projects.append(rec)
    return projects


def create_andhra_pradesh_projects():
    """Andhra Pradesh - 9 projects"""
    projects = []
    ap_districts = [
        {'name': 'Visakhapatnam', 'lat': 17.6869, 'lon': 83.2185, 'collector': 'V. Vinay Chand'},
        {'name': 'Vijayawada', 'lat': 16.5062, 'lon': 80.6480, 'collector': 'Md. Imtiaz'},
        {'name': 'Tirupati', 'lat': 13.1939, 'lon': 79.8581, 'collector': 'S. Venkateswar'},
    ]
    project_types = ['Expressway', 'Railway', 'Port Expansion', 'Industrial Corridor', 'SEZ Hub']
    
    for i, district in enumerate(ap_districts):
        for j in range(3):
            p_type = np.random.choice(project_types)
            rec = _build_project_record(
                state='Andhra Pradesh',
                state_code='AP',
                district_name=district['name'],
                collector=district['collector'],
                lat=district['lat'],
                lon=district['lon'],
                proj_id=f"AP-{i+1:02d}-{j+1:02d}",
                p_name=f"{district['name']} {p_type} Sector {j+1}",
                p_type=p_type,
                area_min=90, area_max=310,
                fam_min=45, fam_max=260,
                comp_min=20000000, comp_max=95000000,
                status_probs=[0.25, 0.35, 0.25, 0.15]
            )
            projects.append(rec)
    return projects


def create_maharashtra_projects():
    """Maharashtra - 8 projects"""
    projects = []
    mh_districts = [
        {'name': 'Mumbai Suburban', 'lat': 19.0760, 'lon': 72.8777, 'collector': 'Rajendra Keshari'},
        {'name': 'Pune', 'lat': 18.5204, 'lon': 73.8567, 'collector': 'Rajesh Deshmukh'},
        {'name': 'Nagpur', 'lat': 21.1458, 'lon': 79.0882, 'collector': 'Sandip Chakraborty'},
        {'name': 'Thane', 'lat': 19.2183, 'lon': 72.9781, 'collector': 'Ashok Shingare'},
    ]
    project_types = ['Metro Rail Line', 'Samruddhi Mahamarg Link', 'Cargo Terminal', 'Port Terminal']
    
    for i, district in enumerate(mh_districts):
        for j in range(2):
            p_type = np.random.choice(project_types)
            rec = _build_project_record(
                state='Maharashtra',
                state_code='MH',
                district_name=district['name'],
                collector=district['collector'],
                lat=district['lat'],
                lon=district['lon'],
                proj_id=f"MH-{i+1:02d}-{j+1:02d}",
                p_name=f"{district['name']} {p_type} Sec-{j+1}",
                p_type=p_type,
                area_min=80, area_max=270,
                fam_min=60, fam_max=220,
                comp_min=30000000, comp_max=120000000,
                status_probs=[0.20, 0.30, 0.30, 0.20]
            )
            projects.append(rec)
    return projects


def create_karnataka_projects():
    """Karnataka - 7 projects"""
    projects = []
    ka_districts = [
        {'name': 'Bangalore Urban', 'lat': 12.9716, 'lon': 77.5946, 'collector': 'K. Dayananda'},
        {'name': 'Mysore', 'lat': 12.2958, 'lon': 76.6394, 'collector': 'Dr. K.V. Rajendra'},
        {'name': 'Hubli-Dharwad', 'lat': 15.3647, 'lon': 75.1240, 'collector': 'Divya Prabhu'},
    ]
    project_types = ['Tech Park Corridor', 'Highway Bypass', 'Namma Metro Extension', 'KIADB Industrial Zone']
    
    count = 0
    for i, district in enumerate(ka_districts):
        num_projects = 3 if i == 0 else 2
        for j in range(num_projects):
            p_type = np.random.choice(project_types)
            rec = _build_project_record(
                state='Karnataka',
                state_code='KA',
                district_name=district['name'],
                collector=district['collector'],
                lat=district['lat'],
                lon=district['lon'],
                proj_id=f"KA-{i+1:02d}-{j+1:02d}",
                p_name=f"{district['name']} {p_type} Stage {j+1}",
                p_type=p_type,
                area_min=60, area_max=240,
                fam_min=40, fam_max=190,
                comp_min=18000000, comp_max=85000000,
                status_probs=[0.25, 0.35, 0.25, 0.15]
            )
            projects.append(rec)
            count += 1
    return projects


def create_rajasthan_projects():
    """Rajasthan - 6 projects"""
    projects = []
    rj_districts = [
        {'name': 'Jaipur', 'lat': 26.9124, 'lon': 75.7873, 'collector': 'Prakash Rajpurohit'},
        {'name': 'Udaipur', 'lat': 24.5854, 'lon': 73.7125, 'collector': 'Arvind Poswal'},
        {'name': 'Jodhpur', 'lat': 26.2389, 'lon': 73.0243, 'collector': 'Gaurav Agrawal'},
    ]
    project_types = ['Desert Highway Corridor', 'Mega Solar Ultra Park', 'Canal Water Project', 'RIICO Industrial Zone']
    
    for i, district in enumerate(rj_districts):
        for j in range(2):
            p_type = np.random.choice(project_types)
            rec = _build_project_record(
                state='Rajasthan',
                state_code='RJ',
                district_name=district['name'],
                collector=district['collector'],
                lat=district['lat'],
                lon=district['lon'],
                proj_id=f"RJ-{i+1:02d}-{j+1:02d}",
                p_name=f"{district['name']} {p_type} Ph-{j+1}",
                p_type=p_type,
                area_min=120, area_max=320,
                fam_min=70, fam_max=230,
                comp_min=15000000, comp_max=80000000,
                status_probs=[0.30, 0.30, 0.25, 0.15]
            )
            projects.append(rec)
    return projects


def create_multi_state_dataset():
    """
    Create realistic sample data for 5 major states
    35-50 projects total across states
    """
    np.random.seed(42)
    all_projects = []
    
    all_projects.extend(create_tamil_nadu_projects())
    all_projects.extend(create_andhra_pradesh_projects())
    all_projects.extend(create_maharashtra_projects())
    all_projects.extend(create_karnataka_projects())
    all_projects.extend(create_rajasthan_projects())
    
    df = pd.DataFrame(all_projects)
    return df


def calculate_project_metrics(df):
    """Calculate state-wise and national metrics"""
    
    metrics = {
        'national': {
            'total_projects': int(len(df)),
            'total_area': float(round(df['total_area_acres'].sum(), 2)),
            'total_families': int(df['affected_families'].sum()),
            'total_compensation': float(round(df['compensation_assessed'].sum(), 2)),
            'avg_completion': float(round(df['completion_percentage'].mean(), 1)),
            'avg_days_to_notification': 60,
            'avg_days_to_possession': 240,
        },
        'by_state': {}
    }
    
    for state in sorted(df['state'].unique()):
        state_data = df[df['state'] == state]
        
        metrics['by_state'][state] = {
            'total_projects': int(len(state_data)),
            'total_area': float(round(state_data['total_area_acres'].sum(), 2)),
            'affected_families': int(state_data['affected_families'].sum()),
            'compensation_assessed': float(round(state_data['compensation_assessed'].sum(), 2)),
            'avg_completion': float(round(state_data['completion_percentage'].mean(), 1)),
            'projects_pending': int(len(state_data[state_data['acquisition_status'] == 'Pending'])),
            'projects_notified': int(len(state_data[state_data['acquisition_status'] == 'Notified'])),
            'projects_awarded': int(len(state_data[state_data['acquisition_status'] == 'Awarded'])),
            'projects_possessed': int(len(state_data[state_data['acquisition_status'] == 'Possessed'])),
            'total_legal_disputes': int(state_data['legal_disputes'].sum()),
            'avg_rr_completion': float(round(state_data['rr_completion_pct'].mean(), 1)),
        }
    
    return metrics


def get_or_create_multi_state_data():
    """Load existing dataset or generate new dataset if files are missing"""
    if os.path.exists(CSV_PATH) and os.path.exists(METRICS_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            with open(METRICS_PATH, 'r') as f:
                metrics = json.load(f)
            # Also ensure data/ directories are populated
            if not os.path.exists(DATA_CSV_PATH):
                df.to_csv(DATA_CSV_PATH, index=False)
            if not os.path.exists(DATA_MS_CSV_PATH):
                df.to_csv(DATA_MS_CSV_PATH, index=False)
            return df, metrics
        except Exception as e:
            print(f"Error loading existing files: {e}. Regenerating...")

    df = create_multi_state_dataset()
    df.to_csv(CSV_PATH, index=False)
    df.to_csv(DATA_CSV_PATH, index=False)
    df.to_csv(DATA_MS_CSV_PATH, index=False)
    
    metrics = calculate_project_metrics(df)
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=2, default=str)
    
    return df, metrics


if __name__ == "__main__":
    print("=" * 70)
    print("🏛️ MULTI-STATE LAND ACQUISITION SAMPLE DATASET GENERATOR")
    print("=" * 70)
    
    df, metrics = get_or_create_multi_state_data()
    
    print(f"\n✅ Generated {len(df)} projects across {len(df['state'].unique())} states:")
    print(f"  - CSV File: {CSV_PATH}")
    print(f"  - Data Dir CSV: {DATA_CSV_PATH}")
    print(f"  - JSON File: {METRICS_PATH}")
    
    print(f"\n📊 NATIONAL SUMMARY:")
    print(f"  Total Projects: {metrics['national']['total_projects']}")
    print(f"  Total Area: {metrics['national']['total_area']:.1f} acres")
    print(f"  Total Families: {metrics['national']['total_families']:,}")
    print(f"  Total Compensation: ₹{metrics['national']['total_compensation']/10000000:.2f} Crores")
    print(f"  Average Completion: {metrics['national']['avg_completion']:.1f}%")
