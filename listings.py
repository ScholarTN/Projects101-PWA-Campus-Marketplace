import streamlit as st
from supabase_client import supabase
from upload import upload_file
import requests
#from listings_features import extract_top_features #uncomment when spacy now works on python verson 3.14 or above

def inject_custom_css():
    st.markdown("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
        <style>
           

        </style>
    """, unsafe_allow_html=True)

def create_listing(user):
    st.markdown("### 📝 Create New Listing")
    st.markdown("Fill in the details below to create your listing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("📌 Title*")
        price = st.number_input("💰 Price (₹)*", min_value=0, step=100)
        category = st.selectbox("🏷️ Category*", ["Housing", "Groceries", "Essentials", "Electronics", "Furniture", "Books", "Clothing", "Services", "Other"])
    
    with col2:
        listing_type = st.selectbox("📦 Type*", ["For Sale", "For Rent", "Wanted", "Free"])
        contact_phone = st.text_input("📱 Your Phone Number*")
        contact_email = st.text_input("📧 Your Email", value=user.email if user else "")
    
    description = st.text_area("📄 Description*", height=150)
    
    st.markdown("### 🖼️ Media")
    col1, col2 = st.columns(2)
    
    with col1:
        images = st.file_uploader("Upload Images (max 5)", 
                                 accept_multiple_files=True, 
                                 type=['jpg', 'jpeg', 'png', 'gif'],
                                 help="Upload clear photos of your item")
    
    with col2:
        video = st.file_uploader("Upload Video (optional)", type=["mp4", "mov", "avi"])
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        if st.button("🚀 Post Listing", use_container_width=True, type="primary"):
            if not all([title, price, description, contact_phone]):
                st.error("Please fill in all required fields (*)")
            else:
                with st.spinner("Creating your listing..."):
                    # Upload images
                    image_urls = []
                    if images:
                        for img in images[:5]:  # Limit to 5 images
                            try:
                                url = upload_file(img, "images")
                                image_urls.append(url)
                            except Exception as e:
                                st.warning(f"Could not upload {img.name}")
                    
                    # Upload video if exists
                    video_url = None
                    if video:
                        try:
                            video_url = upload_file(video, "videos")
                        except Exception as e:
                            st.warning(f"Could not upload video")
                    
                    # Insert into database
                    try:
                        supabase.from_("listings").insert({
                            "title": title,
                            "description": description,
                            "price": price,
                            "category": category,
                            "type": listing_type,
                            "image_urls": image_urls,
                            "video_url": video_url,
                            "owner_id": user.id,
                            "owner_email": user.email,
                            "phone": contact_phone,
                            "contact_email": contact_email or user.email
                        }).execute()
                        
                        st.success("✅ Listing created successfully!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error("Failed to create listing. Please try again.")
    
    with col3:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

def view_listings(search_query="", price_range=(0, 100000), category_filter="All", sort_option="Newest"):
    # Inject Styles
    inject_custom_css()
    
    # --- NAVIGATION LOGIC ---
    # Check if a specific listing is selected for detailed view
    if "selected_listing" not in st.session_state:
        st.session_state.selected_listing = None

    if st.session_state.selected_listing:
        render_detail_view(st.session_state.selected_listing)
        return
    # ------------------------

    # Build query
    query = supabase.from_("listings").select("*")
    
    # Apply search filter
    if search_query:
        query = query.ilike("title", f"%{search_query}%") # Removed OR description query due to syntax complexity in Supabase client usually needing specific format, kept simple for stability
    
    # Apply price filter
    query = query.gte("price", price_range[0]).lte("price", price_range[1])
    
    # Apply category filter
    if category_filter != "All":
        query = query.eq("category", category_filter)
    
    # Apply sorting
    if sort_option == "Price: Low to High":
        query = query.order("price", desc=False)
    elif sort_option == "Price: High to Low":
        query = query.order("price", desc=True)
    else:  # Newest first
        query = query.order("created_at", desc=True)
    
    try:
        response = query.execute()
        listings = response.data
        
        if not listings:
            st.info("📭 No listings found. Try adjusting your filters or be the first to create a listing!")
            return
        
        st.markdown(f"**Found {len(listings)} item(s)**")
        
        # Display listings in grid 
        cols_per_row = 3
        for i in range(0, len(listings), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for col_idx in range(cols_per_row):
                if i + col_idx < len(listings):
                    item = listings[i + col_idx]
                    
                    with cols[col_idx]:
                        # --- DATA PREPARATION ---
                        img_src = item["image_urls"][0] if item.get("image_urls") else "https://via.placeholder.com/300x200?text=No+Image"
                        wa_link = f"https://wa.me/91{item['phone']}?text=Hi! I'm interested in: {item['title']}" if item.get('phone') else "#"
                        tel_link = f"tel:{item['phone']}" if item.get('phone') else "#"
                        mail_link = f"mailto:{item['email']}" if item.get('email') else "#"
                        
                        # --- UPDATED CARD HTML ---
                        st.markdown(f"""
                        <div class="listing-card">
                            <div class="card-img-wrapper">
                                <img src="{img_src}" class="card-img" alt="Listing Image">
                                <a href="{img_src}" target="_blank" class="expand-btn" title="Expand Image">
                                    <i class="bi bi-arrows-angle-expand"></i>
                                </a>
                            </div>
                            <div class="card-body-custom">
                                <div class="card-title-text" title="{item['title']}">
                                    {item['title']}
                                </div>
                                <div class="card-meta">
                                    <span class="meta-badge">{item['category']}</span>
                                    <span>•</span>
                                    <span class="text-light" style="font-size: 0.8rem;">{item['type']}</span>
                                </div>
                                <div class="action-row">
                                    <div class="price-badge">
                                        ₹ {item['price']:,}
                                    </div>
                                    <div style="flex-grow:1;"></div> <a href="{wa_link}" target="_blank" class="icon-btn whatsapp" title="WhatsApp">
                                        <i class="bi bi-whatsapp"></i>
                                    </a>
                                    <a href="{mail_link}" class="icon-btn email" title="Email">
                                        <i class="bi bi-envelope-fill"></i>
                                    </a>
                                    <a href="{tel_link}" class="icon-btn phone" title="Call">
                                        <i class="bi bi-telephone-fill"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Native Streamlit Button for Page Navigation
                        if st.button("View Details", key=f"btn_{item['id']}", use_container_width=True):
                            st.session_state.selected_listing = item
                            st.rerun()

        # Pagination suggestion
        if len(listings) > 9:
            st.markdown("---")
            st.markdown("**More items available** - Use filters to narrow results")
            
    except Exception as e:
        st.error(f"Error loading listings: {str(e)}")


#for detailed view of listing
def render_detail_view(item):
    """
    Renders the detailed view of a single listing.
    Acts as a 'separate page'.
    """
    if st.button("← Back to Listings"):
        st.session_state.selected_listing = None
        st.rerun()
    
    st.markdown("---")
    
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.title(item['title'])
        st.markdown(f"#### ₹ {item['price']:,}")
        
        # Tags
        st.markdown(f"**Category:** {item['category']} | **Type:** {item['type']}")
        
        st.markdown("### Description")
        st.write(item['description'])
        
        st.markdown("### Contact Seller")
        if item.get("phone"):
            st.info(f"📞 **Phone:** {item['phone']}")
            # WhatsApp Logic
            whatsapp_url = f"https://wa.me/91{item['phone']}?text=Hi! I'm interested in your listing: {item['title']}"
            st.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-Chat_Now-25D366?style=for-the-badge&logo=whatsapp)]({whatsapp_url})")

        if item.get("contact_email"):
            st.markdown(f"📧 **Email:** {item['contact_email']}")
            
        st.markdown(f"**Listing ID:** `{item['id']}`")
        st.markdown(f"**Posted on:** {item.get('created_at', 'N/A')[:10]}")

    with c2:
        # Gallery Logic
        if item.get("image_urls"):
            st.image(item["image_urls"][0], caption="Primary Image", use_container_width=True)
            
            # Additional Images
            if len(item["image_urls"]) > 1:
                st.markdown("**More Images:**")
                grid = st.columns(3)
                for idx, img_url in enumerate(item["image_urls"][1:]):
                    with grid[idx % 3]:
                        st.image(img_url, use_container_width=True)
        else:
            st.image("img/cm_pholder.png", use_container_width=True)
            
        # Video Logic
        if item.get("video_url"):
            st.markdown("### Video")
            try:
                # Fixed f-string quote nesting issue from original code
                st.markdown(
                    f'<iframe src="{item["video_url"]}" width="100%" height="250" frameborder="0" allowfullscreen></iframe>',
                    unsafe_allow_html=True
                )
            except:
                st.write(f"Video Link: {item['video_url']}")