import streamlit as st
from supabase_client import supabase

def login():
    st.subheader("Login / Signup")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if res.user:
            st.session_state.user = res.user
            st.success("Logged in")

    if st.button("Sign Up"):
        supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        st.success("Account created")
