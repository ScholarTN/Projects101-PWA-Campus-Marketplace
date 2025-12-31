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



def view_listings():
    st.subheader("Available Listings")

    response = (
        supabase
        .from_("listings")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    listings = response.data

    if not listings:
        st.info("No listings available yet.")
        return

    for item in listings:
        with st.container():
            col_img, col_info = st.columns([1, 3])

            # ---------------- IMAGE COLUMN ----------------
            with col_img:
                if item.get("image_urls"):
                    st.image(
                        item["image_urls"][0],
                        width="stretch"
                    )
                else:
                    st.image(
                        "https://via.placeholder.com/200x200?text=No+Image",
                        width="stretch"
                    )

            # ---------------- INFO COLUMN ----------------
            with col_info:
                st.markdown(f"### {item['title']}")
                st.markdown(f"**₹ {item['price']}**")
                st.markdown(f"**Category:** {item['category']}")
                st.markdown(f"**Type:** {item['type']}")

                # Short preview
                if item.get("description"):
                    preview = item["description"][:120]
                    st.markdown(preview + "...")

                # Expandable details (Amazon-style)
                with st.expander("View more details"):
                    st.markdown(f"**Full Description:**\n\n{item['description']}")
                    st.markdown(f"**Listing ID:** `{item['id']}`")

            st.divider()
            