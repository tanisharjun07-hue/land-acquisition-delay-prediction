"""
Authentication & Role Management System
For Tamil Nadu Land Acquisition Portal
"""

import streamlit as st
from datetime import datetime, timedelta
import hashlib
import json

# ============================================================================
# DEMO CREDENTIALS & USER DATABASE
# ============================================================================

# Demo users for authorities (For Demo Purpose Only - Replace in Production)
DEMO_CREDENTIALS = {
    # Admin - Super user
    'admin@tnland.gov.in': {
        'password': 'Admin@123',
        'name': 'Admin User',
        'role': 'Admin',
        'district': 'All Districts',
        'department': 'Land Acquisition Authority',
        'access_level': 'Full Access'
    },
    
    # District Collectors
    'collector.chennai@tnmail.gov.in': {
        'password': 'Chennai@123',
        'name': 'Dr. Supradeep Elangeni',
        'role': 'District Collector',
        'district': 'Chennai',
        'department': 'Revenue Department',
        'access_level': 'District Level'
    },
    
    'collector.coimbatore@tnmail.gov.in': {
        'password': 'Coimbatore@123',
        'name': 'Dr. Sudha Sadasivam',
        'role': 'District Collector',
        'district': 'Coimbatore',
        'department': 'Revenue Department',
        'access_level': 'District Level'
    },
    
    'collector.madurai@tnmail.gov.in': {
        'password': 'Madurai@123',
        'name': 'V. Anbuchezhiyan',
        'role': 'District Collector',
        'district': 'Madurai',
        'department': 'Revenue Department',
        'access_level': 'District Level'
    },
    
    'collector.salem@tnmail.gov.in': {
        'password': 'Salem@123',
        'name': 'Suki Eswaran',
        'role': 'District Collector',
        'district': 'Salem',
        'department': 'Revenue Department',
        'access_level': 'District Level'
    },
    
    'collector.trichy@tnmail.gov.in': {
        'password': 'Trichy@123',
        'name': 'Pradeep Kumar Ramakrishnan',
        'role': 'District Collector',
        'district': 'Trichy',
        'department': 'Revenue Department',
        'access_level': 'District Level'
    },
    
    # Regional Officers
    'officer.northern@tnmail.gov.in': {
        'password': 'Officer@123',
        'name': 'K. Ramakrishnan',
        'role': 'Regional Officer',
        'district': 'Chennai, Villupuram',
        'department': 'Land Acquisition Wing',
        'access_level': 'Regional Level'
    },
    
    'officer.western@tnmail.gov.in': {
        'password': 'Officer@123',
        'name': 'S. Anand Kumar',
        'role': 'Regional Officer',
        'district': 'Coimbatore, Tiruppur, Erode, Salem',
        'department': 'Land Acquisition Wing',
        'access_level': 'Regional Level'
    },
    
    'officer.southern@tnmail.gov.in': {
        'password': 'Officer@123',
        'name': 'R. Murugesan',
        'role': 'Regional Officer',
        'district': 'Madurai, Tirunelveli, Kanyakumari',
        'department': 'Land Acquisition Wing',
        'access_level': 'Regional Level'
    },
    
    # Analysts
    'analyst.tn@tnmail.gov.in': {
        'password': 'Analyst@123',
        'name': 'Dr. Priya Sharma',
        'role': 'Data Analyst',
        'district': 'All Districts',
        'department': 'Planning & Analytics',
        'access_level': 'View Only'
    }
}


# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def hash_password(password):
    """Hash password for verification"""
    return hashlib.sha256(password.encode()).hexdigest()


def initialize_session():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'login_timestamp' not in st.session_state:
        st.session_state.login_timestamp = None


def login_user(email, password):
    """Authenticate user with email and password"""
    
    if email not in DEMO_CREDENTIALS:
        return False, "❌ User not found. Check email and try again."
    
    user = DEMO_CREDENTIALS[email]
    
    if user['password'] != password:
        return False, "❌ Invalid password. Try again."
    
    # Login successful
    st.session_state.logged_in = True
    st.session_state.user_email = email
    st.session_state.user_info = user
    st.session_state.login_timestamp = datetime.now()
    
    return True, f"✅ Welcome, {user['name']}!"


def logout_user():
    """Logout current user"""
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_info = None
    st.session_state.login_timestamp = None


def get_user_district():
    """Get district(s) accessible by current user"""
    if not st.session_state.logged_in:
        return None
    
    user_info = st.session_state.user_info
    role = user_info.get('role', '')
    
    if role == 'Admin':
        return 'All Districts'
    else:
        return user_info.get('district', 'All Districts')


def check_access_level(required_level):
    """Check if user has required access level"""
    if not st.session_state.logged_in:
        return False
    
    access_levels = {
        'Full Access': 3,
        'Regional Level': 2,
        'District Level': 2,
        'View Only': 1
    }
    
    user_level = access_levels.get(st.session_state.user_info.get('access_level'), 0)
    required = access_levels.get(required_level, 0)
    
    return user_level >= required


# ============================================================================
# LOGIN PAGE UI
# ============================================================================

def show_login_page():
    """Display login page with government branding"""
    
    # Government styling
    st.markdown("""
        <style>
        .login-container {
            background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
            margin-bottom: 25px;
        }
        .login-title {
            color: #FFD700;
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .login-subtitle {
            color: #ffffff;
            font-size: 15px;
            margin-bottom: 20px;
        }
        .demo-badge {
            background-color: #ff5722;
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 13px;
            display: inline-block;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="login-container">
                <div class="login-title">🏛️ தமிழ்நாடு நில எடுப்பு ஆணையம்</div>
                <div class="login-subtitle">Tamil Nadu Land Acquisition & Cadastral Portal</div>
                <div class="demo-badge">🔐 DEMO MODE - Authorized Personnel Portal</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form(key="login_form"):
            email = st.text_input(
                "📧 Official Email ID",
                placeholder="e.g. admin@tnland.gov.in or collector.chennai@tnmail.gov.in",
                help="Use official government credentials"
            )
            
            password = st.text_input(
                "🔐 Password",
                type="password",
                placeholder="Enter your security password"
            )
            
            submit_button = st.form_submit_button("🔓 Secure Login", use_container_width=True)
            
            if submit_button:
                if not email or not password:
                    st.warning("⚠️ Please enter both email and password")
                else:
                    success, message = login_user(email.strip(), password.strip())
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        st.markdown("---")
        
        # Demo credentials
        with st.expander("📋 Click here to view Demo Credentials"):
            st.markdown("""
            | Role | Email ID | Password | Access Level |
            | :--- | :--- | :--- | :--- |
            | **Super Admin** | `admin@tnland.gov.in` | `Admin@123` | Full Access |
            | **Collector (Chennai)** | `collector.chennai@tnmail.gov.in` | `Chennai@123` | District Level |
            | **Collector (Coimbatore)** | `collector.coimbatore@tnmail.gov.in` | `Coimbatore@123` | District Level |
            | **Collector (Madurai)** | `collector.madurai@tnmail.gov.in` | `Madurai@123` | District Level |
            | **Regional Officer (West)** | `officer.western@tnmail.gov.in` | `Officer@123` | Regional Level |
            | **Data Analyst** | `analyst.tn@tnmail.gov.in` | `Analyst@123` | View Only |
            """)
        
        st.info("ℹ️ National Land Acquisition & Monitoring Portal | SIH Solution")


# ============================================================================
# USER PROFILE & SIDEBAR
# ============================================================================

def show_user_profile():
    """Display current user profile in sidebar"""
    if not st.session_state.logged_in:
        return
    
    user = st.session_state.user_info
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 User Profile")
        
        st.markdown(f"**{user.get('name', 'Unknown')}**")
        st.caption(f"Role: {user.get('role', 'User')} | {user.get('department', 'Revenue Dept')}")
        
        st.markdown(f"""
        - 🏛️ **District**: `{user.get('district', 'N/A')}`
        - 🛡️ **Access**: `{user.get('access_level', 'N/A')}`
        """)
        
        # Login time
        if st.session_state.login_timestamp:
            login_time = st.session_state.login_timestamp.strftime("%H:%M:%S (%d-%b)")
            st.caption(f"⏱️ Logged in: {login_time}")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout_user()
            st.rerun()


# ============================================================================
# AUTHORIZATION DECORATORS
# ============================================================================

def require_login(func):
    """Decorator to require login"""
    def wrapper(*args, **kwargs):
        if not st.session_state.get('logged_in', False):
            st.error("🔐 Please login to access this page")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_role(required_role):
    """Decorator to require specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not st.session_state.get('logged_in', False):
                st.error("🔐 Please login to access this page")
                st.stop()
            
            user_role = st.session_state.user_info.get('role')
            if required_role:
                if isinstance(required_role, list) and user_role not in required_role:
                    st.error(f"❌ Access denied. This page requires role in: {required_role}")
                    st.stop()
                elif isinstance(required_role, str) and user_role != required_role:
                    st.error(f"❌ Access denied. This page requires role: {required_role}")
                    st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    initialize_session()
    show_login_page()
