import streamlit as st
from supabase_client import supabase
from upload import upload_file
import time

# --- RATING MANAGER CLASS ---
class RatingManager:
    @staticmethod
    def get_user_rating(listing_id, user_id):
        """Fetch the specific rating a user gave to a listing"""
        if not user_id: return 0
        try:
            response = supabase.table("listing_ratings")\
                .select("listing_rating")\
                .eq("listing_id", listing_id)\
                .eq("user_id", user_id)\
                .execute()
            return response.data[0]['listing_rating'] if response.data else 0
        except Exception:
            return 0

    @staticmethod
    def get_listing_stats(listing_id):
        """Get average rating and count for a listing"""
        try:
            response = supabase.table("listing_ratings")\
                .select("listing_rating")\
                .eq("listing_id", listing_id)\
                .execute()
            
            ratings = [r['listing_rating'] for r in response.data]
            if not ratings:
                return 0.0, 0
            
            avg = sum(ratings) / len(ratings)
            return round(avg, 1), len(ratings)
        except Exception:
            return 0.0, 0

    @staticmethod
    def submit_rating(listing_id, user_id, owner_id, rating_value):
        """Upsert rating (Insert or Update if exists)"""
        try:
            data = {
                "user_id": user_id,
                "listing_id": listing_id,
                "listing_owner_id": owner_id,
                "listing_rating": rating_value
            }
            # The on_conflict parameter uses the Unique Constraint we created in SQL
            supabase.table("listing_ratings").upsert(data, on_conflict="user_id, listing_id").execute()
            return True
        except Exception as e:
            st.error(f"Rating failed: {str(e)}")
            return False

def inject_custom_css():
    st.markdown("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
        <style>
            .listing-card {
                background: white;
                border: 1px solid #eee;
                border-radius: 12px;
                overflow: hidden;
                margin-bottom: 20px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .listing-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.08);
            }
            .card-img-wrapper {
                position: relative;
                height: 200px;
                background-color: #f8f9fa;
                overflow: hidden;
            }
            .card-img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .expand-btn {
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(255,255,255,0.9);
                padding: 5px 8px;
                border-radius: 50%;
                color: #333;
                text-decoration: none;
            }
            .card-body-custom {
                padding: 15px;
            }
            .card-title-text {
                font-weight: 600;
                font-size: 1.05rem;
                margin-bottom: 5px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .card-meta {
                font-size: 0.8rem;
                color: #6c757d;
                margin-bottom: 10px;
            }
            .meta-badge {
                background: #e9ecef;
                padding: 2px 8px;
                border-radius: 10px;
                color: #495057;
            }
            .action-row {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-top: 10px;
            }
            .price-badge {
                background: #e8f5e9;
                color: #2e7d32;
                font-weight: 700;
                padding: 5px 12px;
                border-radius: 20px;
            }
            .icon-btn {
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                color: white;
                text-decoration: none;
                transition: opacity 0.2s;
            }
            .icon-btn:hover { opacity: 0.8; color: white; }
            .whatsapp { background-color: #25D366; }
            .email { background-color: #EA4335; }
            .phone { background-color: #0d6efd; }
            
            /* Rating Styles */
            .rating-container {
                display: flex;
                align-items: center;
                gap: 5px;
                margin-bottom: 10px;
            }
            .star-btn {
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                transition: color 0.2s;
                padding: 0;
            }
            .star-filled { color: #ffc107; }
            .star-empty { color: #e4e5e9; }
        </style>
    """, unsafe_allow_html=True)

def create_listing(user):
    st.markdown("### 📝 Create New Listing")
    
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("📌 Title*")
        price = st.number_input("💰 Price (₹)*", min_value=0, step=100)
        category = st.selectbox("🏷️ Category*", 
                               [ "Housing", "Groceries", "Essentials", "Electronics", 
                                "Furniture", "Books", "Clothing", "Services", "Other"])
    
    with col2:
        listing_type = st.selectbox("📦 Type*", 
                                   ["For Sale", "For Rent", "Wanted", "Free"])
        contact_phone = st.text_input("📱 Your Phone Number*")
        contact_email = st.text_input("📧 Your Email", value=user.email if user else "")
    
    description = st.text_area("📄 Description*", height=150)
    
    st.markdown("### 🖼️ Media")
    col1, col2 = st.columns(2)
    with col1:
        images = st.file_uploader("Upload Images (max 5)", accept_multiple_files=True, type=['jpg', 'jpeg', 'png', 'gif'])
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
                    image_urls = []
                    if images:
                        for img in images[:5]:
                            try:
                                url = upload_file(img, "images")
                                image_urls.append(url)
                            except Exception: pass
                    
                    video_url = None
                    if video:
                        try:
                            video_url = upload_file(video, "videos")
                        except Exception: pass
                    
                    try:
                        listing_data = {
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
                        }
                        
                        supabase.from_("listings").insert(listing_data).execute()
                        st.success("✅ Listing created successfully!")
                        time.sleep(2)
                        st.session_state.page = "home"
                        st.rerun()
                            
                    except Exception as e:
                        st.error(f"Failed to create listing: {str(e)}")
    
    with col3:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

def render_star_rating(item):
    """Renders the interactive star rating component"""
    user = st.session_state.get("user")
    
    # 1. Get Stats
    avg_rating, total_ratings = RatingManager.get_listing_stats(item['id'])
    
    # 2. Display Average
    st.markdown(f"#### ⭐ {avg_rating} / 5.0")
    st.caption(f"({total_ratings} ratings)")
    
    if not user:
        st.info("Log in to rate this item")
        return

    # 3. Check if Owner (Prevent Self-Rating)
    if user.id == item['owner_id']:
        st.info("You cannot rate your own listing.")
        return

    # 4. Get Current User's Rating
    current_user_rating = RatingManager.get_user_rating(item['id'], user.id)
    
    st.markdown("---")
    st.write("Rate this product:")
    
    # 5. Interactive Stars
    cols = st.columns([1,1,1,1,1, 8]) # 5 small cols for stars, rest filler
    
    def set_rating(val):
        RatingManager.submit_rating(item['id'], user.id, item['owner_id'], val)
        st.toast(f"You rated this {val} stars!")
        time.sleep(0.5) # small delay for UX

    # Render 5 buttons masquerading as stars
    # If the button index is less than user rating, show filled star
    for i in range(1, 6):
        with cols[i-1]:
            is_filled = i <= current_user_rating
            label = "★" if is_filled else "☆"
            if st.button(label, key=f"rate_{item['id']}_{i}", help=f"Rate {i} stars"):
                set_rating(i)
                st.rerun()

def render_detail_view(item):
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
        
        # --- NEW RATING SECTION ---
        st.markdown("### Ratings & Reviews")
        render_star_rating(item)
        # --------------------------
        
        st.markdown("### Contact Seller")
        wa_link = f"https://wa.me/91{item['phone']}?text=Hi! I'm interested in: {item['title']}"
        tel_link = f"tel:{item['phone']}" if item.get('phone') else "#"
        mail_link = f"mailto:{item.get('contact_email') or ''}"

        st.markdown(f"""
            <div style="display:inline-flex; gap:10px;"> 
                <a href="{wa_link}" target="_blank" class="icon-btn whatsapp" style="width:40px;height:40px;"><i class="bi bi-whatsapp"></i></a>
                <a href="{mail_link}" class="icon-btn email" style="width:40px;height:40px;"><i class="bi bi-envelope-fill"></i></a>
                <a href="{tel_link}" class="icon-btn phone" style="width:40px;height:40px;"><i class="bi bi-telephone-fill"></i></a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        st.caption(f"ID: {item['id']} | Posted: {item.get('created_at', 'N/A')[:10]}")

    with c2:
        if item.get("image_urls"):
            st.image(item["image_urls"][0], use_container_width=True)
            if len(item["image_urls"]) > 1:
                st.markdown("**More Images:**")
                grid = st.columns(3)
                for idx, img_url in enumerate(item["image_urls"][1:]):
                    with grid[idx % 3]:
                        st.image(img_url, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/400x300?text=No+Image", use_container_width=True)
            
        if item.get("video_url"):
            st.markdown("### Video")
            st.video(item["video_url"])

def view_listings(search_query="", price_range=(0, 100000), category_filter="All", sort_option="Newest"):
    inject_custom_css()
    
    if "selected_listing" not in st.session_state:
        st.session_state.selected_listing = None

    if st.session_state.selected_listing:
        render_detail_view(st.session_state.selected_listing)
        return

    # Build query
    query = supabase.from_("listings").select("*")
    if search_query: query = query.ilike("title", f"%{search_query}%")
    query = query.gte("price", price_range[0]).lte("price", price_range[1])
    if category_filter != "All": query = query.eq("category", category_filter)
    
    if sort_option == "Price: Low to High": query = query.order("price", desc=False)
    elif sort_option == "Price: High to Low": query = query.order("price", desc=True)
    else: query = query.order("created_at", desc=True)
    
    try:
        response = query.execute()
        listings = response.data
        
        if not listings:
            st.info("📭 No listings found.")
            return
        
        st.markdown(f"**Found {len(listings)} item(s)**")
        
        cols_per_row = 3
        for i in range(0, len(listings), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                if i + col_idx < len(listings):
                    item = listings[i + col_idx]
                    with cols[col_idx]:
                        img = item["image_urls"][0] if item.get("image_urls") else "https://via.placeholder.com/300x200"
                        
                        st.markdown(f"""
                        <div class="listing-card">
                            <div class="card-img-wrapper">
                                <img src="{img}" class="card-img">
                            </div>
                            <div class="card-body-custom">
                                <div class="card-title-text">{item['title']}</div>
                                <div class="card-meta">{item['category']} • {item['type']}</div>
                                <div class="price-badge">₹ {item['price']:,}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("View Details", key=f"btn_{item['id']}", use_container_width=True):
                            st.session_state.selected_listing = item
                            st.rerun()
            
    except Exception as e:
        st.error(f"Error loading listings: {str(e)}")