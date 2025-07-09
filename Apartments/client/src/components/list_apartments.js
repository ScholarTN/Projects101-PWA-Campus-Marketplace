import React, { useState, useEffect } from 'react';
import axios from 'axios'; 
import styles from "./list_apartments.module.css"; // Assuming you have a CSS file for styles
const API_BASE_URL = 'http://localhost:5001'; 

function ApartmentList({ route, setRoute,apartmentsImagesId, setApartmentsImagesId,apartmentsImagesName, setApartmentsImagesName}) {
    const [apartments, setApartments] = useState([]); // State to hold the list of apartments
    const [loading, setLoading] = useState(true);    // State to indicate loading status
    const [error, setError] = useState(null);         // State to hold any fetch errors

    useEffect(() => {
        const fetchApartments = async () => {
            setLoading(true); // Start loading
            setError(null);   // Clear previous errors
            try {
                // Make GET request to the backend endpoint
                const response = await axios.get(`${API_BASE_URL}/api/apartments`);
                setApartments(response.data); // Update state with fetched data
            } catch (err) {
                console.error("Error fetching apartments:", err);
                setError("Failed to load apartments. Please try again later.");
            } finally {
                setLoading(false);
            }
        };

        fetchApartments();

    }, []); // Empty dependency array means this effect runs only once when the component mounts

    // --- Render Logic ---

    if (loading) {
        return <p>Loading apartments...</p>;
    }

    if (error) {
        return <p style={{ color: 'red' }}>{error}</p>; // Show error message
    }

    if (apartments.length === 0) {
        return <p>No apartments found.</p>; // Handle case with no data
    }

    //for navigation to other components
    const handleNavigation = (newRoute,par_id,par_name) => {
        alert(`Navigating to ${newRoute}` + par_name + par_id); // Optional: Alert for navigation
        setApartmentsImagesId(par_id); // Set the apartment ID and name for image upload
        setApartmentsImagesName(par_name); // Set the apartment name for image upload
        setRoute(newRoute);
    };

    // --- Display the Apartment List ---
    return (
        <div className="apartment-list-container">
            <h2>Available Apartments</h2>
            {apartments.map((apt, index) => (
                // If no guaranteed unique ID, use index: key={index}
                <div key={apt.ap_id || index} className={styles.apartment_card}>
                    <h3>{apt.ap_name}</h3>
                    <div className={styles.apartment_inner_card}>
                    <p><strong>Address:</strong> {apt.ap_address}</p>
                    <p><strong>Description:</strong> {apt.ap_description || 'N/A'}</p>
                    <p><strong>Rent:</strong> ${apt.ap_rent_price ? apt.ap_rent_price.toLocaleString() : 'N/A'} / month</p>
                    <p><strong>Deposit:</strong> ${apt.ap_deposit_amount ? apt.ap_deposit_amount.toLocaleString() : 'N/A'}</p>
                    <p><strong>Available From:</strong> {apt.ap_availability_date ? new Date(apt.ap_availability_date).toLocaleDateString() : 'N/A'}</p>
                    <p><strong>Lease Length:</strong> {apt.ap_lease_length || 'N/A'}</p>

                    {/* Handle Image URLs (assuming ap_image_urls is an array) */}
                    {Array.isArray(apt.ap_image_urls) && apt.ap_image_urls.length > 0 && (
                        <div>
                            <strong>Images:</strong>
                            <ul>
                                {apt.ap_image_urls.map((url, imgIndex) => (
                                    <li key={imgIndex}>
                                        <a href={url} target="_blank" rel="noopener noreferrer">Image {imgIndex + 1}</a>
                                        {/* Or display thumbnails: <img src={url} alt={`Apartment ${imgIndex + 1}`} width="100" /> */}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {/* Handle Video URL */}
                    {apt.ap_video_url && (
                         <p><strong>Video:</strong> <a href={apt.ap_video_url} target="_blank" rel="noopener noreferrer">Watch Video</a></p>
                    )}
                    </div>

                    <hr style={{ margin: '15px 0' }}/>
                    <button onClick={() => handleNavigation("viewApartmentsImages", index, apt.ap_name)}>Images</button>
                    <button>Vidoes</button>
                     <br></br>
                    <button>Edit</button>
                    <button>Make Unavailable</button>
                    <button>View Bookings</button>
                    <button>Delete</button>
                </div>
            ))}
        </div>
    );
}


export default ApartmentList;