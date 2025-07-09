import React, { useState } from "react";
import axios from "axios";
import ap_img_styles from "./add_apartment_images.module.css"; // Assuming you have a CSS file for styles

const AddApartmentImages = ({ route, setRoute, apartmentsImagesId, setApartmentsImagesId,apartmentsImagesName, setApartmentsImagesName }) => {
    const [apartmentName, setApartmentName] = useState("");
    const [images, setImages] = useState([]);

    const handleFileChange = (e) => {
        setImages(e.target.files);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (images.length === 0) {
            alert("Please provide an apartment name and select images.");
            return;
        }
        
        const formData = new FormData();
        formData.append("recordno",apartmentsImagesId)
        Array.from(images).forEach((image) => {
            formData.append("images", image);
        });

        try {
            const response = await axios.post("http://localhost:5001/api/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            if (response.data.success) {
                alert("Images uploaded successfully!");
            } else {
                alert("Failed to upload images.");
            }
        } catch (error) {
            console.error("Error uploading images:", error);
            alert("An error occurred while uploading images. Front");
        }
    };

    return (
        <div>
            <h1 styles={ap_img_styles.h1}>Apartment Name: {apartmentsImagesName}</h1>
            <form onSubmit={handleSubmit} styles={ap_img_styles.form}>
                <div>
                    <input
                        type="text"
                        id="apartmentId"
                        name="apartmentId"
                        readOnly
                        value={apartmentsImagesId}
                    />
                </div>
                <div>
                    <label htmlFor="images">Upload Images:</label>
                    <input
                        type="file"
                        id="images"
                        name="images"
                        accept="image/*"
                        multiple
                        onChange={handleFileChange}
                    />
                </div>
                <button type="submit">Send</button>
            </form>
        </div>
    );
};

export default AddApartmentImages;