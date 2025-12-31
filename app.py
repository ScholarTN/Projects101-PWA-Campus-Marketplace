import streamlit as st
from auth import login
from listings import create_listing, view_listings

st.set_page_config(
    page_title="Campus Marketplace | Amazon Style",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Session state initialization
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "price_range" not in st.session_state:
    st.session_state.price_range = (0, 10000)
if "category_filter" not in st.session_state:
    st.session_state.category_filter = "All"
if "user" not in st.session_state:
    st.session_state.user = None

# Custom CSS for Amazon-like styling
st.markdown("""
<style>
    /* Amazon-like theme */
    .main {
        background-color: #f3f3f3;
    }
    .stButton>button {
        background-color: #FFD814;
        color: black;
        border: none;
        border-radius: 20px;
        padding: 8px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #F7CA00;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stSelectbox>div>div {
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    .listing-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .listing-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    .price-tag {
        background: #FFD814;
        color: #B12704;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
    }
    .contact-buttons {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }
    .whatsapp-btn {
        background-color: #25D366 !important;
        color: white !important;
    }
    .call-btn {
        background-color: #007BFF !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header with Logo and Navigation
# ----------------------------
if st.session_state.page != "login":
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown("## 🛒 Campus Marketplace")
    
    with col2:
        search_query = st.text_input(
            "🔍 Search for items...",
            value=st.session_state.search_query,
            key="search_input"
        )
        if search_query != st.session_state.search_query:
            st.session_state.search_query = search_query
            st.rerun()
    
    with col3:
        if st.button("👤 Logout"):
            st.session_state.page = "login"
            st.session_state.user = None
            st.rerun()

# ----------------------------
# Page router
# ----------------------------
if st.session_state.page == "login":
    login()

elif st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; color: #232F3E;'>Campus Marketplace</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #565959;'>Your one-stop shop for campus essentials</p>", unsafe_allow_html=True)
    
    # Filters sidebar
    with st.sidebar:
        st.markdown("### 🔍 Filters")
        
        # Price range filter
        st.markdown("**Price Range (₹)**")
        min_price, max_price = st.slider(
            "Select price range",
            min_value=0,
            max_value=10000,
            value=st.session_state.price_range,
            step=100,
            label_visibility="collapsed"
        )
        st.session_state.price_range = (min_price, max_price)
        
        # Category filter
        st.markdown("**Category**")
        categories = ["All", "Housing", "Electronics", "Furniture", "Books", "Other"]
        selected_category = st.selectbox(
            "Select category",
            categories,
            index=categories.index(st.session_state.category_filter) if st.session_state.category_filter in categories else 0,
            label_visibility="collapsed"
        )
        st.session_state.category_filter = selected_category
        
        # Sort options
        st.markdown("**Sort By**")
        sort_option = st.selectbox(
            "Sort items by",
            ["Newest", "Price: Low to High", "Price: High to Low"],
            label_visibility="collapsed"
        )
        st.session_state.sort_option = sort_option
        
        # Clear filters button
        if st.button("Clear All Filters"):
            st.session_state.search_query = ""
            st.session_state.price_range = (0, 10000)
            st.session_state.category_filter = "All"
            st.session_state.sort_option = "Newest"
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"### 📦 Available Listings")
        if st.session_state.search_query:
            st.markdown(f"*Search results for: '{st.session_state.search_query}'*")
        
        # Display active filters
        filters_text = []
        if st.session_state.price_range != (0, 10000):
            filters_text.append(f"Price: ₹{st.session_state.price_range[0]} - ₹{st.session_state.price_range[1]}")
        if st.session_state.category_filter != "All":
            filters_text.append(f"Category: {st.session_state.category_filter}")
        if filters_text:
            st.markdown(f"**Active filters:** {', '.join(filters_text)}")
    
    with col2:
        if st.button("➕ Create New Listing", use_container_width=True):
            st.session_state.page = "create_listing"
            st.rerun()
    
    st.divider()
    
    # Amazon-style listings feed with filters
    view_listings(
        search_query=st.session_state.search_query,
        price_range=st.session_state.price_range,
        category_filter=st.session_state.category_filter,
        sort_option=getattr(st.session_state, 'sort_option', 'Newest')
    )

elif st.session_state.page == "create_listing":
    create_listing(st.session_state.user)
    
    st.divider()
    if st.button("⬅ Back to Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()