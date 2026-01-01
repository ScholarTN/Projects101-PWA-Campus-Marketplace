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



html_form = f"""
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-10">   
            <div class="profile-card">
                <div class="profile-header"></div>
                <div class="card-body p-0">
                    <div class="row g-0">
                        <div class="col-md-4 p-4 border-end-md text-center bg-light">
                            <div class="profile-avatar-container mb-3">
                                <img src="img/cm_pholder.png" alt="Profile Picture" class="profile-avatar">
                                <div class="edit-icon" title="Change Picture">
                                    <i class="bi bi-camera"></i>
                                </div>
                            </div>
                            <h5 class="fw-bold mb-1">{user_data['full_name']}</h5>
                            <p class="text-muted mb-3">{user_data['role']}</p>
                            <div class="d-flex justify-content-center gap-2 mb-4">
                                <span class="badge-student">
                                    <i class="bi bi-mortarboard me-1"></i> {user_data['is_student']}
                                </span>
                                <span class="badge bg-secondary bg-opacity-10 text-secondary border border-secondary border-opacity-10">
                                    {user_data['student_id']}
                                </span>
                            </div>
                            <div class="text-start px-3">
                                <h6 class="text-uppercase text-muted fs-7 fw-bold mb-3 small">Account Status</h6>
                                <div class="d-flex align-items-center justify-content-between mb-3">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-shield-check text-success me-2"></i>
                                        <span class="status-label">Verified: {user_data['is_verified']}</span>
                                    </div>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="isVerified" checked>
                                    </div>
                                </div>
                                <div class="d-flex align-items-center justify-content-between">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-circle-fill text-success me-2" style="font-size: 0.8rem;"></i>
                                        <span class="status-label">Online Status: {user_data['online_status']}</span>
                                    </div>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="onlineStatus" checked>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-4 pt-3 border-top text-start px-3">
                                <small class="text-muted d-block">
                                    <i class="bi bi-clock me-1"></i> Last Login
                                </small>
                                <span class="fw-medium text-dark">{user_data['last_login']}</span>
                            </div>
                        </div>
                        <div class="col-md-8 p-4 p-md-5">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h4 class="fw-bold mb-0">Profile Details</h4>
                            </div>
                            <form>
                                <div class="row g-3">
                                    <div class="col-12">
                                        <label for="fullName" class="form-label">Full Name</label>
                                        <div class="input-group">
                                            <span class="input-group-text bg-white text-muted border-end-0"><i class="bi bi-person"></i></span>
                                            <input type="text" class="form-control border-start-0 ps-0" id="fullName" value="{user_data['full_name']}" placeholder="Enter full name">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <label for="email" class="form-label">Email Address</label>
                                        <div class="input-group">
                                            <span class="input-group-text bg-white text-muted border-end-0"><i class="bi bi-envelope"></i></span>
                                            <input type="email" class="form-control border-start-0 ps-0" id="email" value="{user_data['email']}">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <label for="phone" class="form-label">Phone Number</label>
                                        <div class="input-group">
                                            <span class="input-group-text bg-white text-muted border-end-0"><i class="bi bi-telephone"></i></span>
                                            <input type="tel" class="form-control border-start-0 ps-0" id="phone" value="{user_data['phone_number']}">
                                        </div>
                                    </div>
                                    <div class="col-12"><hr class="my-2 text-muted opacity-25"></div>
                                    <div class="col-md-6">
                                        <label class="form-label">Role</label>
                                        <input type="text" class="form-control" value="{user_data['role']}" readonly>
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label">Is Student?</label>
                                        <input type="text" class="form-control" value="{user_data['is_student']}" readonly>
                                    </div>
                                    <div class="col-12 mt-4">
                                        <label for="password" class="form-label">Password</label>
                                        <div class="d-flex gap-2">
                                            <input type="password" class="form-control" id="password" value="{user_data['password']}" readonly>
                                            <button type="button" class="btn btn-outline-secondary px-3">Change</button>
                                        </div>
                                        <div class="form-text">To change your password, verification will be sent to your email.</div>
                                    </div>
                                    <div class="col-12 mt-5 text-end">
                                        <button type="button" class="btn btn-light text-muted me-2">Cancel</button>
                                        <button type="submit" class="btn btn-save text-white shadow-sm">Save Changes</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

def profile():
    st.markdown(html_form, unsafe_allow_html=True)
