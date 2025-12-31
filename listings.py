import streamlit as st
from supabase_client import supabase
from upload import upload_file

def create_listing(user):
    st.subheader("Create Listing")

    title = st.text_input("Title")
    description = st.text_area("Description")
    price = st.number_input("Price", min_value=0)
    category = st.selectbox("Category", ["Housing", "Electronics", "Furniture", "Books"])
    listing_type = st.selectbox("Type", ["house", "item"])

    images = st.file_uploader("Images", accept_multiple_files=True)
    video = st.file_uploader("Video", type=["mp4", "mov"])

    if st.button("Post Listing"):
        image_urls = [upload_file(img, "images") for img in images]
        video_url = upload_file(video, "videos") if video else None

        supabase.from_("listings").insert({
            "title": title,
            "description": description,
            "price": price,
            "category": category,
            "type": listing_type,
            "image_urls": image_urls,
            "video_url": video_url,
            "owner_id": user.id
        }).execute()

        st.success("Listing created!")
