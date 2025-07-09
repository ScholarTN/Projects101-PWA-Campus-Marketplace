import React from 'react';
import AddApartmentImages from './add_apartment_images.js';
import ShowApartmentImages from './show_apartment_images.js';

const ApartmentImages = ({ 
    route, 
    setRoute, 
    apartmentsImagesId, 
    setApartmentsImagesId, 
    apartmentsImagesName, 
    setApartmentsImagesName 
}) => {
    return (
        <div>
            <ShowApartmentImages 
                route={route} 
                setRoute={setRoute} 
                apartmentsImagesId={apartmentsImagesId} 
                setApartmentsImagesId={setApartmentsImagesId} 
                apartmentsImagesName={apartmentsImagesName} 
                setApartmentsImagesName={setApartmentsImagesName} 
            />
            <AddApartmentImages 
                route={route} 
                setRoute={setRoute} 
                apartmentsImagesId={apartmentsImagesId} 
                setApartmentsImagesId={setApartmentsImagesId} 
                apartmentsImagesName={apartmentsImagesName} 
                setApartmentsImagesName={setApartmentsImagesName} 
            />
        </div>
    );
};

export default ApartmentImages;