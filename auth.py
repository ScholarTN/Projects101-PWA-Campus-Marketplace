import streamlit as st
from supabase_client import supabase

def login():
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 30px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Logo and title - ONLY in login page
    st.markdown("<h1 style='text-align: center;'>🛒</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #232F3E;'>Campus Marketplace</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #565959;'>Login to buy and sell on campus</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Login form
    email = st.text_input("📧 Email Address")
    password = st.text_input("🔑 Password", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚪 Login", use_container_width=True):
            if email and password:
                try:
                    res = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    if res.user:
                        st.session_state.user = res.user
                        st.session_state.page = "home"
                        st.rerun()

                except Exception as e:
                    st.error("Login failed: Invalid email or password")
            else:
                st.warning("Please enter both email and password")
    
    with col2:
        if st.button("📝 Sign Up", use_container_width=True):
            if email and password:
                try:
                    supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })
                    st.success("Account created! Please check your email to verify your account.")
                except Exception as e:
                    st.error("Signup failed. Please try a different email.")
            else:
                st.warning("Please enter both email and password")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    