import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ShowApartmentImages = ({ apartmentsImagesId, setApartmentsImagesId, apartmentsImagesName, setApartmentsImagesName }) => {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchImages = async () => {
            try {
                setLoading(true);
                setError(null);

                // Make a POST request to fetch images for the given apartment ID
                const response = await axios.post('/api/apartments/images', {
                    recordno: apartmentsImagesId,
                });

                // Update state with the received images
                setImages(response.data.images || []);
                setApartmentsImagesName(response.data.apartmentName || '');
            } catch (err) {
                setError('Failed to fetch images. Please try again.');
            } finally {
                setLoading(false);
            }
        };

        if (apartmentsImagesId) {
            fetchImages();
        }
    }, [apartmentsImagesId, setApartmentsImagesName]);

    return (
        <div>
            <h2>Apartment Images</h2>
            {loading && <p>Loading images...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {!loading && !error && images.length === 0 && <p>No images found for this apartment.</p>}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                {images.map((image, index) => (
                    <img
                        key={index}
                        src={`../server/uploads/${image.url}`}
                        alt={`Apartment ${apartmentsImagesName} - Image ${index + 1}`}
                        style={{ width: '150px', height: '150px', objectFit: 'cover', borderRadius: '8px' }}
                    />
                ))}
            </div>
        </div>
    );
};

export default ShowApartmentImages;