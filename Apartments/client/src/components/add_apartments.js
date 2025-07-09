import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import add_ap_styles from './add_apartments.module.css';


const AddApartmentForm = ({ onCancel}) => {
    const [formData, setFormData] = useState({
        apartment_name: '',
        apartment_address: '',
        apartment_description: '',
        apartment_rent_price: '',
        apartment_deposit_amount: '',
        apartment_availability_date: '',
        apartment_lease_length: '',
        apartment_images: null,
        apartment_videos: null,
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const API_URL = 'http://localhost:5001/api'; // Adjust if your server port is different

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleFileChange = (e) => {
        setFormData({ ...formData, apartment_images: e.target.files[0] });
    };

    const handleVideoChange = (e) => {
        setFormData({ ...formData, apartment_videos: e.target.files[0] });
    };

    /*const handleSubmit = async (e) => {
        //onSave(formData);
        e.preventDefault(); // Prevent default form submission page reload
        if (!formData.apartment_name.trim()) {
            setError('Apartment name cannot be empty.');
            return;
        }
        if (!formData.apartment_address.trim()) {
            setError('Apartment address cannot be empty.');
            return;
        }
        if (!formData.apartment_description.trim()) {
            setError('Apartment description cannot be empty.');
            return;
        }
        setError(null);
        setLoading(true); // Indicate loading state

        try {
            const response = await axios.post(`${API_URL}/apartments`, {
                content: formData, // Send the content in the request body
            });

            console.log('Data sent:', response.data);
        } catch (err) {
            
        } finally {
            setLoading(false); // Reset loading state
        }
    };*/

    const handleSubmit = async (event) => {
        event.preventDefault();
        const apartmentData = {
            apartment_name: formData.apartment_name, // From your component's state
            apartment_address: formData.apartment_address, // From your component's state
            apartment_description: formData.apartment_description,
            apartment_rent_price: parseFloat(formData.apartment_rent_price) || 0, // Ensure it's a number, handle potential NaN if needed
            apartment_deposit_amount: parseFloat(formData.apartment_deposit_amount) || null, // Handle potentially empty optional fields
            apartment_availability_date: formData.apartment_availability_date, // Ensure this is not empty/null/undefined
            apartment_lease_length: formData.apartment_lease_length,
            apartment_images: formData.apartment_images, // Assuming this is a file object or array of file objects
            apartment_videos: FormData.apartment_videos, // Assuming this is a file object or array of file objects 
        };
    
        console.log('Data being sent to server:', apartmentData); // <--- INSPECT THIS OUTPUT CAREFULLY
    
        try {
            const response = await axios.post('http://localhost:5001/api/apartments', apartmentData); // Ensure URL is correct
            console.log('Server response:', response.data);
            // Handle success
        } catch (err) {
            console.error("Error sending message:", err);
            setError('Failed to send message. Please try again.');
            // Log the specific response data from the server if it exists
            if (err.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.error('Server Response Data:', err.response.data); // <--- LOOK AT THIS
                console.error('Server Response Status:', err.response.status);
                console.error('Server Response Headers:', err.response.headers);
            } else if (err.request) {
                // The request was made but no response was received
                console.error('No response received:', err.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.error('Error setting up request:', err.message);
            }
        } finally {
            setLoading(false); // Reset loading state
        }
    };

    return (
        <div styles={add_ap_styles.container}>
            <h2>Add Apartment</h2>
            <p>Please fill in the details below to add a new apartment.</p>
            <form onSubmit={handleSubmit} styles={add_ap_styles.form}>
                <div>
                    <label htmlFor="apartment_name">Apartment Name</label>
                    <input
                        type="text"
                        id="apartment_name"
                        name="apartment_name"
                        value={formData.apartment_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="apartment_address">Apartment Address</label>
                    <textarea
                        name="apartment_address"
                        id="apartment_address"
                        value={formData.apartment_address}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="apartment_description">Apartment Description</label>
                    <textarea
                        name="apartment_description"
                        id="apartment_description"
                        placeholder="Apartment Description i.e. 2BHK, 3BHK, etc."
                        rows="4"
                        value={formData.apartment_description}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="apartment_rent_price">Monthly Rent Amount (in Rupees)</label>
                    <input
                        type="number"
                        name="apartment_rent_price"
                        id="apartment_rent_price"
                        placeholder="i.e. 8000 etc."
                        value={formData.apartment_rent_price}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="apartment_deposit_amount">Deposit Amount</label>
                    <input
                        type="number"
                        name="apartment_deposit_amount"
                        id="apartment_deposit_amount"
                        placeholder="i.e. 1000 etc."
                        value={formData.apartment_deposit_amount}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="apartment_availability_date">Availability Date</label>
                    <input
                        type="date"
                        name="apartment_availability_date"
                        id="apartment_availability_date"
                        value={formData.apartment_availability_date}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="apartment_lease_length">Lease Length (in Months)</label>
                    <input
                        type="number"
                        name="apartment_lease_length"
                        id="apartment_lease_length"
                        placeholder="i.e. 6 etc."
                        value={formData.apartment_lease_length}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="apartment_images">Upload Image(s):</label>
                    <input
                        type="file"
                        id="apartment_images"
                        name="apartment_images"
                        onChange={handleFileChange}
                        multiple="multiple"
                        accept="image/*"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="apartment_videos">Upload Video(s):</label>
                    <input
                        type="file"
                        id="apartment_videos"
                        name="apartment_videos"
                        onChange={handleVideoChange}
                        multiple="multiple"
                        accept="video/*"
                        required
                    />
                </div>
                <div>
                <button type="submit">Save</button>
                    <button type="button" className='btn btn-danger p-2' onClick={onCancel}>
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
};

export default AddApartmentForm;