import streamlit as st
from auth import login
from listings import create_listing

st.title("Campus Marketplace")

if "user" not in st.session_state:
    login()
else:
    create_listing(st.session_state.user)
