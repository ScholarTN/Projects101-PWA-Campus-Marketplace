import streamlit as st
from auth import login
from listings import create_listing

st.set_page_config(page_title="Campus Marketplace", layout="wide")

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "login"

st.title("Campus Marketplace")

# Navigation logic
if st.session_state.page == "login":
    login()

elif st.session_state.page == "home":
    st.success(f"Welcome! You are logged in.")
    st.button("Create Listing", on_click=lambda: set_page("create_listing"))

elif st.session_state.page == "create_listing":
    create_listing(st.session_state.user)
    st.button("Back to Home", on_click=lambda: set_page("home"))


def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()
