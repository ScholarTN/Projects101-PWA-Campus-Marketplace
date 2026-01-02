import streamlit as st
from supabase_client import supabase
import profile_dashboard  # will create this next
import time

def inject_profile_css():
    st.markdown("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    """, unsafe_allow_html=True)

    with open("css/profile.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_user_stats(user_id):
    """Fetch basic stats for the user"""
    try:
        # Get count of user's listings
        response = supabase.from_("listings") \
            .select("id", count="exact") \
            .eq("owner_id", user_id) \
            .execute()
        listing_count = response.count if response.count is not None else 0
        return listing_count
    except Exception:
        return 0

def profile_page(user):  #param: user
    """
    Main Profile Entry Point
    :param user: The user object from Supabase auth
    """
    inject_profile_css()
    
    # if not user:
    #     st.warning("Please log in to view your profile.")
    #     return #uncomment

    # --- Fetch Data ---
    # Fetch additional profile data from your 'users' table if you have one, 
    # otherwise use the auth user object and metadata.
    # For this demo, I'll simulate the table fetch or use metadata.
    
    # Mocking 'users' table fetch for display (Replace with actual fetch if 'users' table exists)
    user_details = {
        "full_name": "No Username", #user.user_metadata.get("full_name", "Campus User"),
        "role": "Student", # Or fetch from DB
        "email": user.email,
        "email_verified": "Not Set",
        "phone": user.phone, #user.user_metadata.get("phone", "Not Set"),
        "joined":"Not Set",
        "avatar":  "img/cm_pholder.png" #user.user_metadata.get("avatar_url", "https://api.dicebear.com/7.x/avataaars/svg?seed=" + user.email)
    }
    
    listing_count = get_user_stats(user.id)

    # --- Profile Header Section ---
    st.markdown(f"""
    <div class="profile-header">
        <div class="row align-items-center">
            <div class="col-md-2 text-center">
                <img src="img/cm_pholder.png" class="profile-avatar" alt="Profile">
            </div>
            <div class="col-md-7">
                <h2 style="margin-bottom: 5px;">
                    {user_details['full_name']} 
                    <i class="bi bi-patch-check-fill verified-badge" title="Verified User"></i>
                </h2>
                <div class="mb-2">
                    <span class="role-badge">{user_details['role']}</span>
                </div>
                <div class="text-muted small">
                    <i class="bi bi-envelope me-2"></i> {user_details['email']} &nbsp;|&nbsp; 
                    <i class="bi bi-calendar3 me-2"></i> Joined {user_details['joined']}
                </div>
            </div>
            <div class="col-md-3">
                <div class="d-grid gap-2">
                     <button class="btn btn-outline-primary btn-sm">Edit Profile</button>
                     <button class="btn btn-outline-secondary btn-sm">Account Settings</button>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    #st.write(f"User Details: {user}")

    # --- Stats Row ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{listing_count}</div>
            <div class="stat-label">Active Listings</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">4.8</div>
            <div class="stat-label">Seller Rating</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">12</div>
            <div class="stat-label">Items Sold</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
         st.markdown("""
        <div class="stat-card">
            <div class="stat-value">85%</div>
            <div class="stat-label">Response Rate</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Tabs Navigation ---
    tab1, tab2 = st.tabs(["🛍️ My Listings", "⚙️ Account Security"])

    with tab1:
        # Load the dashboard logic for listings
        profile_dashboard.render_my_listings(user)
        pass
    
    with tab2:
        st.subheader("Security Settings")
        st.info("Password change and 2FA settings would go here.")
        if st.button("Log Out", type="secondary"):
            supabase.auth.sign_out()
            st.session_state.clear()
            st.rerun()