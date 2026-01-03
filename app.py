import streamlit as st
from auth import login
from profile import profile_page
from auth_registration import register_user_profile as signup
from profile_email_reset import reset_password
from listings import create_listing, view_listings
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Campus Marketplace",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Session state initialization
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login" #login is the default
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "price_range" not in st.session_state:
    st.session_state.price_range = (0, 100000)
if "category_filter" not in st.session_state:
    st.session_state.category_filter = "All"
if "user" not in st.session_state:
    st.session_state.user = None

# Custom CSS for styling, bootstrap and hide warnings

components.html(
    """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    """,
    height=0
)

with open("css/app.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


#end of css styling


# Hide warnings
import warnings
#warnings.filterwarnings("ignore")


# ----------------------------
# Page router
# ----------------------------
if st.session_state.page == "login":
    with open("css/auth.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    login()

if st.session_state.page == "signup":
    with open("css/auth_registration.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    signup()

if st.session_state.page == "reset_password":
    # with open("css/profile_email_reset.css") as f:
    #     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    reset_password()

if st.session_state.page == "profile":
    # with open("css/profile.css") as f: #now handled in profile.py
    #     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    profile_page(st.session_state.user) #st.session_state.user

elif st.session_state.page == "home":
    with open("css/listings.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Only show minimal header with search and logout
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col1:
        # Empty space or minimal logo
        st.markdown("### ")
    
    with col2:
        search_query = st.text_input(
            " Search items, categories, etc...",
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
                #st.info("Profile page coming soon!")
                st.session_state.page = "profile"
                st.rerun()
        with col3b:
            if st.button(" Logout", use_container_width=True):
                st.session_state.page = "login" #previosuly just these two lines plus the st.rerun()
                st.session_state.user = None
                # supabase.auth.sign_out()
                # st.session_state.clear()
                st.rerun()
    
    st.markdown("---")
    
    # Main layout with sidebar filters
    col_sidebar, col_main = st.columns([1, 4])
    
    with col_sidebar:
        st.markdown("###  Filters")
        st.markdown("---")
        
        # Price range filter
        st.markdown("**Price Range (₹)**")
        if "price_range" not in st.session_state:
            st.session_state.price_range = (0, 100000)  # default value

        min_price, max_price = st.session_state.price_range

        min_price, max_price = st.slider(
            "Select price range",
            min_value=0,
            max_value=100000,
            value=(min_price, max_price),
            step=100,
            label_visibility="collapsed",
            key="price_range"
        )
        #st.session_state.price_range = (min_price, max_price)
        st.markdown(f"*₹{min_price} - ₹{max_price}*")
        
        st.markdown("---")
        
        # Category filter
        st.markdown("**Category**")
        categories = ["All", "Housing", "Groceries", "Essentials", "Electronics", "Furniture", "Books", "Clothing", "Services", "Other"]
        
        if "category_filter" not in st.session_state:
            st.session_state.category_filter = "All"  # default value

        selected_category = st.selectbox(
            "Select category",
            categories,
            index=categories.index(st.session_state.category_filter) if st.session_state.category_filter in categories else 0,
            label_visibility="collapsed",
            key="category_filter"
        )
        ## No need to reassign — Streamlit already updates st.session_state["category_filter"]
        #st.session_state.category_filter = selected_category
        
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
        if st.button(" Clear Filters", use_container_width=True):
            st.session_state.search_query = ""
            st.session_state.price_range = (0, 100000)
            st.session_state.category_filter = "All"
            st.session_state.sort_option = "Newest"
            st.rerun()
    
    with col_main:
        # Page title and filters summary
        st.markdown("<h1 class='app-title'>Campus Marketplace</h1>", unsafe_allow_html=True)
        st.markdown("<p class='app-subtitle'>Your one-stop shop for campus essentials</p>", unsafe_allow_html=True)
        
        # Active filters display
        filters_active = []
        if st.session_state.search_query:
            filters_active.append(f"Search: '{st.session_state.search_query}'")
        if st.session_state.price_range != (0, 100000):
            filters_active.append(f"Price: ₹{st.session_state.price_range[0]}-₹{st.session_state.price_range[1]}")
        if st.session_state.category_filter != "All":
            filters_active.append(f"Category: {st.session_state.category_filter}")
        
        # Create listing button
        if st.button("➕ Create New Listing", use_container_width=True, type="primary"):
            st.session_state.page = "create_listing"
            st.rerun()
        
        st.markdown("---")

        #shifted active filters down here | remove after successful run
        if filters_active:
            st.markdown(f"**Active filters:** {', '.join(filters_active)}")
        
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