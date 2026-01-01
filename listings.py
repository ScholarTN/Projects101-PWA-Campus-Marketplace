import streamlit as st
from supabase_client import supabase
from upload import upload_file
import requests

def create_listing(user):
    st.markdown("### 📝 Create New Listing")
    st.markdown("Fill in the details below to create your listing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("📌 Title*")
        price = st.number_input("💰 Price (₹)*", min_value=0, step=100)
        category = st.selectbox("🏷️ Category*", ["Housing", "Electronics", "Furniture", "Books", "Clothing", "Services", "Other"])
    
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
                            "contact_phone": contact_phone,
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
    # Build query
    query = supabase.from_("listings").select("*")
    
    # Apply search filter
    if search_query:
        query = query.ilike("title", f"%{search_query}%").or_(f"description.ilike.%{search_query}%")
    
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
                        # Create listing card
                        st.markdown('<div class="listing-card">', unsafe_allow_html=True)
                        
                        # Image section - FIXED: Using width parameter instead of use_column_width
                        if item.get("image_urls") and len(item["image_urls"]) > 0:
                            try:
                                # Check if image URL is accessible
                                response = requests.head(item["image_urls"][0], timeout=5)
                                if response.status_code == 200:
                                    st.image(
                                        item["image_urls"][0],
<<<<<<< HEAD
                                        width=300,  # Fixed width instead of use_column_width
                                        caption=f"{item["image_urls"][0]}"
=======
                                        width=300,
                                        caption="Click to enlarge"
>>>>>>> f606d1fd43f952c15e096ade13d0d010eaba4bd0
                                    )
                                    #or  if response.status_code == 200:
                                    #st.markdown(f"**URLs:** {' '.join(item['image_urls'])}")
                                else:
                                    st.image(
                                        "img/cm_pholder.png",
                                        width=300
                                    )
                            except:
                                st.image(
                                    "img/cm_pholder.png",
                                    width=300
                                )
                        else:
                            st.image(
                                "img/cm_pholder.png",
                                width=300
                            )
                        
                        # Title and price
                        st.markdown(f"### {item['title'][:30]}{'...' if len(item['title']) > 30 else ''}")
                        st.markdown(f'<div class="price-tag">₹ {item["price"]:,}</div>', unsafe_allow_html=True)
                        
                        # Category and type badges
                        col_badge1, col_badge2 = st.columns(2)
                        with col_badge1:
                            st.markdown(f"**{item['category']}**")
                        with col_badge2:
                            st.markdown(f"*{item['type']}*")
                        
                        # Description preview
                        if item.get("description"):
                            description_preview = item["description"][:80] + "..." if len(item["description"]) > 80 else item["description"]
                            st.markdown(f"📝 {description_preview}")
                        
                        # Contact section
                        st.markdown("---")
                        st.markdown("#### 👤 Contact Seller")
                        
                        if item.get("contact_phone"):
                            # WhatsApp button
                            whatsapp_url = f"https://wa.me/91{item['contact_phone']}?text=Hi! I'm interested in your listing: {item['title']}"
                            st.markdown(f"""
                            <div class="contact-buttons">
                                <a href="{whatsapp_url}" target="_blank">
                                    <button class="whatsapp-btn">WhatsApp</button>
                                </a>
                                <a href="tel:{item['contact_phone']}">
                                    <button class="call-btn">Call</button>
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"📱 **Phone:** `{item['contact_phone']}`")
                        
                        if item.get("contact_email"):
                            st.markdown(f"📧 **Email:** `{item['contact_email']}`")
                        
                        # Expandable details
                        with st.expander("📋 View Full Details"):
                            st.markdown(f"**Full Description:**")
                            st.markdown(item['description'])
                            st.markdown(f"**Listing ID:** `{item['id']}`")
                            st.markdown(f"**Posted on:** {item.get('created_at', 'N/A')[:10]}")
                            
                            # Show all images if available
                            if item.get("image_urls") and len(item["image_urls"]) > 1:
                                st.markdown("**More Images:**")
                                img_cols = st.columns(min(3, len(item["image_urls"])))
                                for idx, img_url in enumerate(item["image_urls"][:3]):
                                    with img_cols[idx % 3]:
                                        st.markdown(f"**Image {img_url}:**")
                                        st.image(img_url, width=150)
                            
                            # Show video if available
                            if item.get("video_url"):
                                st.markdown(f"**Videos: {item['video_url']}**")
                                st.markdown("<style>iframe { width: 100%; height: 300px; }</style>", unsafe_allow_html=True)
                                st.markdown(f"<iframe src={item['video_url']}></iframe>", unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pagination suggestion
        if len(listings) > 9:
            st.markdown("---")
            st.markdown("**More items available** - Use filters to narrow results")
            
    except Exception as e:
        st.error("Error loading listings. Please try refreshing the page.")