import streamlit as st
from auth import login
from listings import create_listing, view_listings

st.set_page_config(
    page_title="Campus Marketplace",
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

# Custom CSS for styling and hide warnings
st.markdown("""
<style>
    /* Hide Streamlit warnings and errors */
    .stAlert {
        display: none !important;
    }
    [data-testid="stDecoration"] {
        display: none !important;
    }
    .stException {
        display: none !important;
    }
    
    /* theme */
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
    /* Hide Streamlit menu */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Hide warnings
import warnings
warnings.filterwarnings("ignore")

# ----------------------------
# Page router
# ----------------------------
if st.session_state.page == "login":
    login()

elif st.session_state.page == "home":
    # Only show minimal header with search and logout
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col1:
        # Empty space or minimal logo
        st.markdown("### 🛒")
    
    with col2:
        search_query = st.text_input(
            "🔍 Search items, categories, etc...",
            value=st.session_state.search_query,
            key="search_input",
            label_visibility="collapsed",
            placeholder="Search items, categories, etc..."
        )
        if search_query != st.session_state.search_query:
            st.session_state.search_query = search_query
            st.rerun()
    
    with col3:
        col3a, col3b = st.columns(2)
        with col3a:
            if st.button("👤 Profile", use_container_width=True):
                st.info("Profile page coming soon!")
        with col3b:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.page = "login"
                st.session_state.user = None
                st.rerun()
    
    st.markdown("---")
    
    # Main layout with sidebar filters
    col_main, col_sidebar = st.columns([4, 1])
    
    with col_sidebar:
        st.markdown("### 🔍 Filters")
        st.markdown("---")
        
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
        st.markdown(f"*₹{min_price} - ₹{max_price}*")
        
        st.markdown("---")
        
        # Category filter
        st.markdown("**Category**")
        categories = ["All", "Housing", "Electronics", "Furniture", "Books", "Clothing", "Services", "Other"]
        selected_category = st.selectbox(
            "Select category",
            categories,
            index=categories.index(st.session_state.category_filter) if st.session_state.category_filter in categories else 0,
            label_visibility="collapsed"
        )
        st.session_state.category_filter = selected_category
        
        st.markdown("---")
        
        # Sort options
        st.markdown("**Sort By**")
        sort_option = st.selectbox(
            "Sort items by",
            ["Newest", "Price: Low to High", "Price: High to Low", "Popular"],
            label_visibility="collapsed"
        )
        st.session_state.sort_option = sort_option
        
        st.markdown("---")
        
        # Clear filters button
        if st.button("🧹 Clear Filters", use_container_width=True):
            st.session_state.search_query = ""
            st.session_state.price_range = (0, 10000)
            st.session_state.category_filter = "All"
            st.session_state.sort_option = "Newest"
            st.rerun()
    
    with col_main:
        # Page title and filters summary
        st.markdown("<h1 style='color: #232F3E; margin-bottom: 10px;'>Campus Marketplace</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #565959; margin-top: 0;'>Your one-stop shop for campus essentials</p>", unsafe_allow_html=True)
        
        # Active filters display
        filters_active = []
        if st.session_state.search_query:
            filters_active.append(f"Search: '{st.session_state.search_query}'")
        if st.session_state.price_range != (0, 10000):
            filters_active.append(f"Price: ₹{st.session_state.price_range[0]}-₹{st.session_state.price_range[1]}")
        if st.session_state.category_filter != "All":
            filters_active.append(f"Category: {st.session_state.category_filter}")
        
        if filters_active:
            st.markdown(f"**Active filters:** {', '.join(filters_active)}")
        
        # Create listing button
        if st.button("➕ Create New Listing", use_container_width=True, type="primary"):
            st.session_state.page = "create_listing"
            st.rerun()
        
        st.markdown("---")
        
        # Display listings
        view_listings(
            search_query=st.session_state.search_query,
            price_range=st.session_state.price_range,
            category_filter=st.session_state.category_filter,
            sort_option=getattr(st.session_state, 'sort_option', 'Newest')
        )

elif st.session_state.page == "create_listing":
    create_listing(st.session_state.user)
    
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("⬅ Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()