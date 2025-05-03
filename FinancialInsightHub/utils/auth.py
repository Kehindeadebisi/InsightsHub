import streamlit as st

# Define users with roles
USERS = {
    "admin": {"password": "admin", "role": "admin"},
    "finance": {"password": "finance", "role": "finance"},
    "hr": {"password": "hr", "role": "hr"},
    "payments": {"password": "payments", "role": "payments"},
    "engineering": {"password": "engineering", "role": "engineering"},
    "strategy": {"password": "strategy", "role": "strategy"},
    "customer": {"password": "customer", "role": "customer"} # Customer-facing portal access
}

def check_password(username, password):
    """Check if username and password are valid"""
    if username in USERS and USERS[username]["password"] == password:
        return True
    return False

def login(username, password):
    """Log in a user with given username and password"""
    if check_password(username, password):
        st.session_state.authenticated = True
        st.session_state.user = username
        st.session_state.role = USERS[username]["role"]
        return True
    return False

def logout():
    """Log out the current user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    return True

def get_user_role():
    """Get the role of the current user"""
    return st.session_state.role if st.session_state.authenticated else None

def has_access(required_role):
    """Check if the current user has access to a feature requiring the given role"""
    if not st.session_state.authenticated:
        return False
    
    # Admin has access to everything
    if st.session_state.role == "admin":
        return True
    
    # Check if user's role matches required role
    if st.session_state.role == required_role:
        return True
    
    return False
