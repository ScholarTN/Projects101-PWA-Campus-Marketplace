data = supabase.from_("listings").select("title", "description", "price", "category", "type", "image_urls", "video_url", "owner_id").eq("owner_id", user.id).execute()
st.write("<style>* { display: flex; flex-wrap: wrap; }</style>", unsafe_allow_html=True)

for listing in data.data:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(listing["image_urls"][0], width=200)
    with col2:
        st.write(f"**{listing['title']}**")
        st.write(f"{listing['description']}")
        st.write(f"**Price:** {listing['price']}**")
        st.write(f"**Category:** {listing['category']}**")
        st.write(f"**Type:** {listing['type']}**")
        if listing["video_url"]:
            st.write("<style>iframe { width: 100%; height: 300px; }</style>", unsafe_allow_html=True)
            st.write(f"<iframe src={listing['video_url']}></iframe>", unsafe_allow_html=True)
            
            #code not finished iwe
