import streamlit as st
from supabase_client import supabase
import time

def inject_edit_css():
    st.markdown("""
        <style>
            /*.edit-form-container {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                border: 1px solid #e9ecef;
            }*/
            .section-header {
                color: #2c3e50;
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #f8f9fa;
            }
            .readonly-field {
                background-color: #e9ecef;
                cursor: not-allowed;
            }
        </style>
    """, unsafe_allow_html=True)

def fetch_user_details(email):
    """Fetch user details from logged_users table"""
    try:
        response = supabase.table("logged_users") \
            .select("*") \
            .eq("email", email) \
            .execute()
        
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error fetching profile: {str(e)}")
        return None

def update_profile_data(user_id, updates):
    """Push updates to the database"""
    # Update password for the logged-in user
    password = updates.get("password")
    
    try:
        supabase.auth.update_user({
            "password": password
        })
        #old code:
        # response = supabase.auth.update_user({
        #     "password": password
        # })
    except Exception as e:
        st.error(f"Error updating password: {str(e)}")
    

    try:
        response = supabase.table("logged_users") \
            .update(updates) \
            .eq("id", user_id) \
            .execute()
        return True, "Profile updated successfully!"
    except Exception as e:
        return False, f"Update failed: {str(e)}"

def render_edit_profile(user):
    """
    Renders the full-scale edit profile form.
    :param user: The user object from session state (contains email/id)
    """
    inject_edit_css()
    
    # 1. Fetch latest data from DB (don't rely solely on session state)
    current_data = fetch_user_details(user.email)
    
    if not current_data:
        st.error("Could not load user profile data.")
        return

    st.markdown("## ✏️ Edit Profile")
    st.markdown("Update your personal information and contact details below.")

    # 2. Main Edit Form
    with st.container():
        st.markdown('<div class="edit-form-container">', unsafe_allow_html=True)
        
        with st.form("profile_update_form"):
            st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
            
            # Read-only Email (Identity)
            st.text_input("Email Address (Cannot be changed)", 
                         value=current_data.get('email'), 
                         disabled=True,
                         help="Contact support to change your email address.")

            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Full Name", value=current_data.get('name', ''))
                
            with col2:
                new_phone = st.text_input("Phone Number", value=current_data.get('phone', ''))

            # Role Selection (if applicable)
            current_role = current_data.get('role', 'Student')
            role_options = ["Student", "Landlord", "Other"]
            
            # Handle case where current role isn't in standard options
            index = 0
            if current_role in role_options:
                index = role_options.index(current_role)
            
            new_role = st.selectbox("Campus Role", role_options, index=index)
            
            st.markdown("---")
            
            # Submit Button
            submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
            
            if submitted:
                # Validation
                if not new_name.strip():
                    st.error("Name cannot be empty.")
                else:
                    updates = {
                        "name": new_name,
                        "phone": new_phone,
                        "role": new_role
                    }
                    
                    with st.spinner("Updating profile..."):
                        success, msg = update_profile_data(current_data['id'], updates)
                        
                        if success:
                            st.success(msg)
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
                            
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Security Section (Separate Form)
    st.markdown("### 🔐 Security")
    with st.expander("Change Password"):
        with st.form("password_update_form"):
            st.warning("Make sure your new password is strong.")
            
            p1 = st.text_input("New Password", type="password")
            p2 = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Update Password"):
                if not p1:
                    st.error("Password cannot be empty")
                elif p1 != p2:
                    st.error("Passwords do not match")
                elif len(p1) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    # Update Password Logic
                    success, msg = update_profile_data(current_data['id'], {"password": p1})
                    if success:
                        st.success("Password updated successfully!")
                    else:
                        st.error(msg)