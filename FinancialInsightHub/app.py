import streamlit as st
import os
from dashboards import finance, hr, payments, engineering, strategy, ai_assistant, customer
from utils.auth import login, logout, check_password, USERS
from utils.data_loader import load_all_data

# Page configuration
st.set_page_config(
    page_title="Fincra Centralized Insights Hub",
    page_icon="assets/fincra_logo.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open(".streamlit/styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session states
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = None

# Load all data once at startup
data = load_all_data()

# Fincra color palette based on fincra.com
FINCRA_COLORS = {
    "primary": "#2563eb",  # Primary Blue
    "secondary": "#004db3",  # Darker Blue
    "accent": "#ff9700",  # Accent Orange
    "light_blue": "#e5f0ff",
    "dark_blue": "#1e3a8a",
    "light_gray": "#f1f5f9",
    "dark_gray": "#334155",
    "white": "#FFFFFF",
    "black": "#0f172a"
}

def main():
    # Load custom CSS
    load_css()
    
    # Login screen if not authenticated
    if not st.session_state.authenticated:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Fincra logo/header for login screen
            # Display the SVG logo
            st.image("assets/fincra_logo.svg", width=120)
            
            st.markdown(f"""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h1 style='color: {FINCRA_COLORS["primary"]}; font-size: 2.5rem;'>Fincra</h1>
                <h3 style='color: {FINCRA_COLORS["dark_gray"]}; font-weight: 400;'>Centralized Insights Hub</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.image("https://images.unsplash.com/photo-1563013544-824ae1b704d3?q=80", 
                    width=450, 
                    caption="Secure payment solutions for Africa and beyond")
        
        with col2:
            st.markdown(f"""
            <div style='background-color: {FINCRA_COLORS["light_gray"]}; padding: 1.5rem; border-radius: 10px; margin-top: 2rem;'>
                <h2 style='color: {FINCRA_COLORS["primary"]}; margin-bottom: 1rem;'>Login</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Login form
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                
                if submit:
                    if login(username, password):
                        st.success(f"Welcome, {username}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
            
            # Demo accounts info
            with st.expander("Available Demo Accounts"):
                st.write("You can use the following accounts to test different roles:")
                for user, details in USERS.items():
                    st.markdown(f"""
                    <div style='margin-bottom: 0.5rem; padding: 0.5rem; background-color: {FINCRA_COLORS["white"]}; 
                    border-left: 3px solid {FINCRA_COLORS["primary"]}; border-radius: 3px;'>
                        Username: <b>{user}</b> | Password: <b>{user}</b> | Role: <b>{details['role']}</b>
                    </div>
                    """, unsafe_allow_html=True)
        
        return
    
    # Main application after authentication
    st.sidebar.title(f"Welcome, {st.session_state.user}")
    
    # Show role badge
    role_style = f"""
    <div style='background-color: {FINCRA_COLORS["primary"]}; color: white; padding: 0.5rem; 
    border-radius: 5px; text-align: center; margin-bottom: 1.5rem;'>
        <b>Role:</b> {st.session_state.role.capitalize()}
    </div>
    """
    st.sidebar.markdown(role_style, unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.markdown("<h3>Dashboards</h3>", unsafe_allow_html=True)
    page = st.sidebar.radio(
        "",  # Empty label since we're using the markdown header above
        ["Home"] + 
        (["Finance"] if st.session_state.role in ["admin", "finance"] else []) +
        (["HR"] if st.session_state.role in ["admin", "hr"] else []) +
        (["Payments/Ops"] if st.session_state.role in ["admin", "payments"] else []) +
        (["Engineering"] if st.session_state.role in ["admin", "engineering"] else []) +
        (["Strategy"] if st.session_state.role in ["admin", "strategy"] else []) +
        (["Customer Dashboard"] if st.session_state.role in ["admin", "customer"] else []) +
        ["AI Assistant"]
    )
    
    # Logout button
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()
    
    # Footer in sidebar
    st.sidebar.markdown("""---""")
    st.sidebar.markdown("""
    <div style='position: fixed; bottom: 0; padding: 1rem; text-align: center; width: 100%; font-size: 0.8rem;'>
        © 2025 Fincra • Secure Payments
    </div>
    """, unsafe_allow_html=True)
    
    # Display selected dashboard
    if page == "Home":
        display_home()
    elif page == "Finance":
        finance.show_dashboard(data['finance'])
    elif page == "HR":
        hr.show_dashboard(data['hr'])
    elif page == "Payments/Ops":
        payments.show_dashboard(data['payments'])
    elif page == "Engineering":
        engineering.show_dashboard(data['engineering'])
    elif page == "Strategy":
        strategy.show_dashboard(data)
    elif page == "Customer Dashboard":
        customer.show_dashboard(data)
    elif page == "AI Assistant":
        ai_assistant.show_assistant(data)

def display_home():
    # Header with subtitle
    st.markdown("""
    <h1>Fincra Centralized Insights Hub</h1>
    <p style='font-size: 1.2rem; color: #3D3935; margin-bottom: 2rem;'>
        Unified analytics platform for real-time business intelligence
    </p>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div style='background-color: #e5f0ff; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;'>
        <p style='margin: 0; font-size: 1.1rem;'>
            Welcome to the Fincra Centralized Insights Hub (FCIH) - a unified platform providing real-time 
            analytics and insights across all departments. Use the sidebar to navigate to department-specific 
            dashboards or try the AI Assistant to query your data.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a 3-column layout for the dashboard features
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div style='text-align: center;'>
            <h3 style='color: #2563eb;'>Financial Analytics</h3>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1638913662380-9799def8ffb1?q=80", 
                 caption="Real-time FX and cash flow monitoring")
        
        st.markdown("""
        <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 8px; 
        border-left: 4px solid #2563eb; margin-top: 0.5rem;'>
            <p><strong>Finance Dashboard</strong></p>
            <ul style='margin-top: 0.5rem; padding-left: 1.2rem;'>
                <li>FX Exposure Tracking</li>
                <li>Cash Flow Analysis</li>
                <li>Geographic Distribution</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <h3 style='color: #2563eb;'>Operational Insights</h3>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1563986768609-322da13575f3?q=80", 
                 caption="Transaction monitoring and system performance")
        
        st.markdown("""
        <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 8px; 
        border-left: 4px solid #2563eb; margin-top: 0.5rem;'>
            <p><strong>Payments & Engineering</strong></p>
            <ul style='margin-top: 0.5rem; padding-left: 1.2rem;'>
                <li>Transaction Success Rates</li>
                <li>API Performance Metrics</li>
                <li>Error Rate Monitoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center;'>
            <h3 style='color: #2563eb;'>Strategic & HR</h3>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80", 
                 caption="Team performance and company growth")
        
        st.markdown("""
        <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 8px; 
        border-left: 4px solid #2563eb; margin-top: 0.5rem;'>
            <p><strong>Strategy & HR Dashboards</strong></p>
            <ul style='margin-top: 0.5rem; padding-left: 1.2rem;'>
                <li>KPI Tracking & Target Achievement</li>
                <li>Headcount & Turnover Analysis</li>
                <li>Department Performance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Assistant promotion
    st.markdown("""
    <div style='background-color: {FINCRA_COLORS["primary"]}; color: white; padding: 1.5rem; border-radius: 8px; margin-top: 2rem;'>
        <h2 style='color: white; margin-top: 0;'>AI-Powered Insights</h2>
        <p style='font-size: 1.1rem;'>
            Ask questions about your data in natural language and get instant answers.
        </p>
        <div style='display: flex; margin-top: 1rem;'>
            <div style='background-color: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 5px; margin-right: 0.5rem;'>
                "What's our FX exposure today?"
            </div>
            <div style='background-color: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 5px; margin-right: 0.5rem;'>
                "Which country has the most failed transactions?"
            </div>
            <div style='background-color: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 5px;'>
                "What's the onboarding time trend over the last 3 months?"
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
