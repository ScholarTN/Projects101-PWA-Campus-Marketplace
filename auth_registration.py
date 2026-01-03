import streamlit as st
from supabase_client import supabase
import re
import time

def inject_registration_css():
    #took it to auth_registration.css
   pass

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def register_user_profile():
    """
    Renders a professional sign-up form for the 'users' table.
    Returns: True if registration was successful, False otherwise.
    """
    inject_registration_css()

    st.markdown("<h2 class='reg-header'>Create Your Profile</h2>", unsafe_allow_html=True)
    st.markdown("<p class='reg-sub'>Join the campus marketplace community</p>", unsafe_allow_html=True)

    # We use a form to batch the input and prevent reloading on every keystroke
    with st.form("registration_form", clear_on_submit=False):
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="John Doe", help="Enter your full legal name")
        
        with col2:
            phone = st.text_input("Phone Number", placeholder="9876543210", help="For buyers to contact you")

        email = st.text_input("Email Address*", placeholder="student@university.edu", help="This will be unique to your account")

        password = st.text_input("Password*", type="password", placeholder="••••••••", help="At least 8 characters")

        # role = st.selectbox("Role", ["Student", "Landlord"], index=0, help="Select your role") #this is unnecessary
        
        st.markdown("---")
        
        # Submit Button
        submitted = st.form_submit_button("Complete Registration", type="primary", use_container_width=True)

        if submitted:
            # 1. client-side Validation
            if not name or not email or not phone or not password:
                st.error("⚠️ All the fields are required fields.")
                return False

            
            if not is_valid_email(email):
                st.error("⚠️ Please enter a valid email address.")
                return False

            # 2. Prepare Data
            # Note: 'id' and 'created_at' are handled automatically by the database defaults
            user_data = {
                "name": name,
                "email": email,
                "phone": phone if phone else None,
                "password": password,
            }

            # 3. Database Insertion with Error Handling
            try:
                with st.spinner("Creating your profile..."):
                    response_logged_users = supabase.table("logged_users").insert(user_data).execute() #remove this code
                    response_users = supabase.auth.sign_up(user_data)

                # Check if data was returned (implies success)
                if response_logged_users.data and response_users.data:
                    st.success("✅ Profile created successfully!")
                    st.balloons()
                    time.sleep(1) # Give user a moment to see the success message
                    return True
            
            except Exception as e:
                error_msg = str(e)
                # Handle Unique Constraint Violation (Duplicate Email) specifically
                # Postgres error code 23505 is unique_violation
                if "23505" in error_msg or "duplicate key" in error_msg:
                    st.error(f"🚫 The email '{email}' is already registered. Please use a different email or log in.")
                else:
                    st.error(f"❌ An unexpected error occurred: {error_msg}")
                return False

        st.markdown("""
            <div style="text-align: center; margin: 20px 0 10px 0; color: #999; font-size: 0.8rem;">
                ━━━━━━━━━ OR ━━━━━━━━━
            </div>
        """, unsafe_allow_html=True)
        
        if st.form_submit_button("Sign In", type="secondary",use_container_width=True):
            st.session_state.page = "login" # Redirects to the registration logic
            st.rerun()

    return False


#original code
# if email and password:
#     try:
#         supabase.auth.sign_up({
#             "email": email,
#             "password": password
#         })
#         st.success("Account created! Please check your email to verify your account.")
#     except Exception:
#         st.error("Signup failed. Please try a different email.")
# else:
#     st.warning("Please enter both email and password")