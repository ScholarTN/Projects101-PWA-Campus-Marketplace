import React from 'react';
import WelcomeBanner from './welcome_banner.js';
import AddApartmentForm from './add_apartments.js';
import ApartmentList from './list_apartments.js';
import { useState } from 'react';
import AddApartmentImages from './add_apartment_images.js';
import ApartmentImages from './apartment_images.js';

const MainComponent = ({ route, setRoute, apartmentsImagesId, setApartmentsImagesId,apartmentsImagesName, setApartmentsImagesName }) => {
    // State to manage the current route or page
    const renderComponent = () => {
        switch (route) {
            case 'welcome':
                return <WelcomeBanner />;
            case 'addApartment':
                return <AddApartmentForm />;
            case 'viewApartments':
                return <ApartmentList  route={route} setRoute={setRoute} apartmentsImagesId = {apartmentsImagesId} setApartmentsImagesId = {setApartmentsImagesId} apartmentsImagesName ={apartmentsImagesName} setApartmentsImagesName ={setApartmentsImagesName}/>;
            case 'viewApartmentsImages':
                return <ApartmentImages route={route} setRoute={setRoute}  apartmentsImagesId={apartmentsImagesId} setApartmentsImagesId={setApartmentsImagesId} apartmentsImagesName={apartmentsImagesName} setApartmentsImagesName={setApartmentsImagesName} />;
            case 'logout':
                    return <p>Successfully Logged Out</p>;
            default:
                return <p>Page not found</p>;
        }
    };

    return (
        <div>
            {renderComponent()}
        </div>
    );
};

export default MainComponent;