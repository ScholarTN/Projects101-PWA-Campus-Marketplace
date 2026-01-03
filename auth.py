import streamlit as st
from supabase_client import supabase
from cookies_manager import CookiesManager

def inject_login_css():
    #moved to auth.css
    pass

def checkCookies():
    """Checks for existing session in browser cookies"""
    cookie_data = CookiesManager.get_session_cookie()
    
    if cookie_data:
        try:
            # Restore Supabase session
            response = supabase.auth.set_session(
                cookie_data['access_token'], 
                cookie_data['refresh_token']
            )
            if response.user:
                st.session_state.user = response.user
                st.session_state.page = "home"
                st.rerun()
            else:
                CookiesManager.clear_session_cookie()
        except Exception:
            CookiesManager.clear_session_cookie()
            
    # If no valid cookie, stay on login
    return

def login():
    inject_login_css()
    
    # Centering Layout using Columns
    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    
    with col_center:
        # --- CARD START ---
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Header Section
        st.markdown("""
            <div class="brand-header">
                <div class="brand-icon">🛒</div> <!-- or: 🛍️ -->
                <h1 class="brand-title">Campus Marketplace</h1>
                <p class="brand-subtitle">Welcome back! Please login to continue.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Input Section
        email = st.text_input("Email Address", placeholder="name@university.edu", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
        
        st.write("") # Spacer
        
        # --- LOGIN ACTION ---
        if st.button("Log In", type="primary", use_container_width=True):
            if email and password:
                with st.spinner("Authenticating..."):
                    try:
                        res = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        
                        if res.user and res.session:
                            # SAVE COOKIES (Vital for persistence)
                            CookiesManager.set_session_cookie(
                                user_id=res.user.id,
                                email=res.user.email,
                                access_token=res.session.access_token,
                                refresh_token=res.session.refresh_token
                            )

                            st.session_state.user = res.user
                            st.session_state.page = "home"
                            st.rerun()
                    except Exception as e:
                        st.error("Incorrect email or password.")
            else:
                st.warning("Please enter your credentials.")

        # --- SIGN UP ACTION ---
        st.markdown("""
            <div style="text-align: center; margin: 20px 0 10px 0; color: #999; font-size: 0.8rem;">
                ━━━━━━━━━ OR ━━━━━━━━━
            </div>
        """, unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            if st.button("Create New Account", use_container_width=True): #
                st.session_state.page = "signup" # Redirects to the registration logic
                st.rerun()
            
        with col2:
            if st.button("Forgot Password ❓", use_container_width=True): #
                st.session_state.page = "reset_password" # Redirects to the registration logic
                st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        # --- CARD END ---