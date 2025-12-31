import streamlit as st
from supabase_client import supabase

def login():
    st.subheader("Login / Signup")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
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
                st.error("Login failed. Check email or password.")

    with col2:
        if st.button("Sign Up"):
            try:
                supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                st.success("Account created. You can now login.")
            except Exception:
                st.error("Signup failed.")
