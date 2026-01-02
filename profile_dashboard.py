import streamlit as st
from supabase_client import supabase
from upload import upload_file
import time

def inject_dashboard_css():
    with open("css/profile_dashboard.css") as f:
        st.markdown("""<style> """ + f.read() + """</style>""", unsafe_allow_html=True)

def fetch_user_listings(user_id):
    response = supabase.from_("listings") \
        .select("*") \
        .eq("owner_id", user_id) \
        .order("created_at", desc=True) \
        .execute()
    return response.data

def delete_listing(listing_id):
    try:
        supabase.from_("listings").delete().eq("id", listing_id).execute()
        return True, "Listing deleted successfully"
    except Exception as e:
        return False, str(e)

def update_listing_data(listing_id, update_data):
    try:
        supabase.from_("listings").update(update_data).eq("id", listing_id).execute()
        return True, "Listing updated successfully"
    except Exception as e:
        return False, str(e)

def render_edit_form(listing):
    """Renders the form to edit a specific listing"""
    st.markdown(f"#### ✏️ Editing: {listing['title']}")
    
    with st.form(key=f"edit_form_{listing['id']}"):
        col1, col2 = st.columns(2)
        with col1:
            new_title = st.text_input("Title", value=listing['title'])
            new_price = st.number_input("Price (₹)", value=listing['price'], min_value=0)
            new_category = st.selectbox("Category", #this needs fixing i is not consisyent with the app.py categories
                                       ["Housing", "Groceries", "Essentials", "Electronics", 
                                        "Furniture", "Books", "Clothing", "Services", "Other"],
                                       index=["Housing", "Groceries", "Essentials", "Electronics", 
                                        "Furniture", "Books", "Clothing", "Services", "Other"].index(listing['category']) 
                                        if listing['category'] in ["Housing", "Groceries", "Essentials", "Electronics", "Furniture", "Books", "Clothing", "Services", "Other"] else 0)
        
        with col2:
            new_type = st.selectbox("Type", ["For Sale", "For Rent", "Wanted", "Free"],
                                   index=["For Sale", "For Rent", "Wanted", "Free"].index(listing['type']))
            new_phone = st.text_input("Phone", value=listing.get('phone', ''))
        
        new_desc = st.text_area("Description", value=listing['description'], height=150)
        
        st.markdown("**Update Images (Optional)**")
        st.info("Uploading new images will append to existing ones. You can manage existing images below.")
        new_images = st.file_uploader("Add Images", accept_multiple_files=True, type=['jpg', 'png'])

        # Save Button
        if st.form_submit_button("💾 Save Changes", type="primary"):
            updates = {
                "title": new_title,
                "price": new_price,
                "category": new_category,
                "type": new_type,
                "phone": new_phone,
                "description": new_desc
            }
            
            # Handle new image uploads
            if new_images:
                current_urls = listing.get('image_urls', []) or []
                for img in new_images:
                    try:
                        url = upload_file(img, "images")
                        current_urls.append(url)
                    except Exception as e:
                        st.error(f"Failed to upload {img.name}")
                updates['image_urls'] = current_urls

            success, msg = update_listing_data(listing['id'], updates)
            if success:
                st.success(msg)
                time.sleep(1)
                st.session_state.edit_mode = None # Exit edit mode
                st.rerun()
            else:
                st.error(msg)
                
    if st.button("Cancel Editing"):
        st.session_state.edit_mode = None
        st.rerun()

def render_my_listings(user):
    if not user:
        st.warning("Please log in")
        return
    
    
    inject_dashboard_css()
    
    # State Management for Edit Mode
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = None # Stores listing ID being edited

    # If in edit mode, show form and return
    if st.session_state.edit_mode:
        # Fetch fresh data for the item being edited
        current_item = supabase.from_("listings").select("*").eq("id", st.session_state.edit_mode).execute().data
        if current_item:
            render_edit_form(current_item[0])
            return
        else:
            st.session_state.edit_mode = None # Reset if item not found

    # --- Main Dashboard View ---
    
    # Action Bar
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Manage Your Listings")
    with col2:
        if st.button("➕ New Listing", use_container_width=True):
           if "page" in st.session_state: #check back again that this works
                st.session_state.page = "create_listing"
                st.rerun()

                

    # Fetch Data
    listings = fetch_user_listings(user.id)
    
    if not listings:
        st.info("You haven't posted any listings yet.")
        return

    # Render Grid
    cols_per_row = 3
    for i in range(0, len(listings), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(listings):
                item = listings[i + j]
                with cols[j]:
                    #BUT PREVIOUSLY # img = item['image_urls'][0] if item.get('image_urls') else "https://via.placeholder.com/300x200?text=No+Image"
                    img = item.get('image_urls', [])
                    img = img[0] if img else "img/cm_pholder.png"
                    
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <div class="db-img-wrapper">
                            <span class="status-indicator">Active</span>
                            <img src="{img}" class="db-img">
                        </div>
                        <div class="db-body">
                            <div class="db-title" title="{item['title']}">{item['title']}</div>
                            <div class="db-price">₹ {item['price']:,}</div>
                            <small class="text-muted">{item['category']} • {item['type']}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action Buttons
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("✏️ Edit", key=f"edit_{item['id']}", use_container_width=True):
                            st.session_state.edit_mode = item['id']
                            st.rerun()
                    with b2:
                        if st.button("🗑️ Delete", key=f"del_{item['id']}", type="primary", use_container_width=True):
                            # In a real app, you might want a confirmation modal/dialog here
                            # For simplicity in Streamlit, we can use a warning or immediate action
                            # Let's do a simple session state check for confirmation in a future iteration
                            # or just delete for now.
                            success, msg = delete_listing(item['id'])
                            if success:
                                st.success("Deleted!")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("Error!")