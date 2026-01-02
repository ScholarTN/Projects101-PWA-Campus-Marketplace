import streamlit as st
from supabase_client import supabase



def login():
    # Wrap everything in a Streamlit container
    with st.container(key="login-container"):
        st.write('<div class="login-wrapper"><div class="login-card">', unsafe_allow_html=True)

        # Logo and title
        st.write("<h1 style='text-align: center;'>🛒</h1>", unsafe_allow_html=True)
        st.write("<h2 class='login-title'>Campus Marketplace</h2>", unsafe_allow_html=True)
        st.write("<p class='login-subtitle'>Login to buy and sell on campus</p>", unsafe_allow_html=True)

        st.divider()

        # Login form
        email = st.text_input("📧 Email Address", key="user_l_email")
        password = st.text_input("🔑 Password", type="password")

        # Buttons in columns
        col1, col2 = st.columns(2)

        with col1:
            if st.button(" Login", use_container_width=True):
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
                    except Exception:
                        st.error("Login failed: Invalid email or password")
                else:
                    st.warning("Please enter both email and password")

        with col2:
            if st.button(" Sign Up", use_container_width=True):
                if email and password:
                    try:
                        supabase.auth.sign_up({
                            "email": email,
                            "password": password
                        })
                        st.success("Account created! Please check your email to verify your account.")
                    except Exception:
                        st.error("Signup failed. Please try a different email.")
                else:
                    st.warning("Please enter both email and password")

        st.markdown('</div></div>', unsafe_allow_html=True)
        
    