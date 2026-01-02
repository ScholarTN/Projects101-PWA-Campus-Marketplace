import streamlit as st
from supabase_client import supabase

#user_data = supabase.table("users").select("full_name", "email", "phone_number", "password", "role", "is_student", "student_id", "picture", "is_verified", "online_status", "last_login").eq("email", st.session_state.user["email"]).execute().data[0]

user_data = {"full_name":'FULL NAME', 
            "email": 'EMAIL', 
            "phone_number": 'PHONE NUMBER', 
            "password": 'PASSWORD', 
            "role": 'ROLE', 
            "is_student": True, 
            "student_id": 'STUDENT ID', 
            "picture": 'img/cm_pholder.png', 
            "is_verified": True, 
            "online_status": 'ONLINE STATUS', 
            "last_login": 'LAST LOGIN'} 


def profile():
    st.markdown("<div class='profile-container'>", unsafe_allow_html=True)

    st.markdown("<div class='row'>", unsafe_allow_html=True)
    st.markdown("<div class='col-md-6'>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-body'>", unsafe_allow_html=True)

    
    
    st.markdown(f"<p class='card-text'>{user_data['password']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>{user_data['role']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>{user_data['is_student']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>{user_data['student_id']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>{user_data['picture']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>{user_data['is_verified']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>{user_data['online_status']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>{user_data['last_login']}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='col-md-6'>", unsafe_allow_html=True)
    st.markdown(f"<h5 class='card-title'>{user_data['full_name']}</h5>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>{user_data['role']}</p>", unsafe_allow_html=True)

    st.markdown(f"<div class='d-flex justify-content-center'>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>Email: {user_data['email']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='card-text'>Phone: {user_data['phone_number']}</p>", unsafe_allow_html=True)
    st.markdown(f"</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='account-status'>", unsafe_allow_html=True)
    st.markdow(f"<div class='account-status-icon'>", unsafe_allow_html=True)
    st.markdown(f"<i class='bi bi-circle'></i>", unsafe_allow_html=True)
    st.markdown(f"</div>", unsafe_allow_html=True)

    #end of column
    st.markdown("</div>", unsafe_allow_html=True)

    #end of row
    st.markdown("</div>", unsafe_allow_html=True)