import streamlit as st
from supabase import create_client, Client

# --- Supabase Setup ---
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_KEY = "YOUR_ANON_OR_SERVICE_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def reset_password():
    # --- Page Layout ---
    st.set_page_config(page_title="Reset Password", page_icon="🔑", layout="centered")

    st.title("🔑 Reset Your Password")
    st.write("Enter your email address below and we'll send you a secure reset link.")

    # --- Form ---
    with st.form("reset_form"):
        email = st.text_input("📧 Email Address", placeholder="you@example.com")
        submitted =  st.form_submit_button("Send Reset Email")

        if submitted:
            if email.strip() == "":
                st.error("Please enter a valid email address.")
            else:
                try:
                    # Supabase Auth: send reset email
                    response = supabase.auth.reset_password_email(email)
                    # Send password reset email
                    st.success(
                        f"A password reset link has been sent to **{email}**. "
                        "Please check your inbox."
                    )
                except Exception as e:
                    st.error(f"Error sending reset email: {e}")

        #back to login
        if st.form_submit_button("⬅ Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

        