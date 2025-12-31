import streamlit as st
from auth import login
from listings import create_listing, view_listings

st.set_page_config(
    page_title="Campus Marketplace",
    layout="wide"
)

# ----------------------------
# Session state initialization
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

st.title("Campus Marketplace")

# ----------------------------
# Page router
# ----------------------------
if st.session_state.page == "login":
    login()

elif st.session_state.page == "home":
    st.success("Welcome to Campus Marketplace")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Create Listing"):
            st.session_state.page = "create_listing"
            st.rerun()

    with col2:
        if st.button("🔄 Refresh Listings"):
            st.rerun()

    st.divider()

    # Amazon-style listings feed
    view_listings()

elif st.session_state.page == "create_listing":
    create_listing(st.session_state.user)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()
