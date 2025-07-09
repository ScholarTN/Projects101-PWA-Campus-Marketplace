import React, { useState } from "react";
import styles from "./side_bar.module.css";
//import { FaBars } from "react-icons/fa";

const Sidebar = ({ route, setRoute }) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    };

    const handleNavigation = (newRoute) => {
        setRoute(newRoute);
    };

    return (
        <div className={`sidebar-container ${isOpen ? "open" : ""}`}>
            <div className={styles.menu_icon} onClick={toggleSidebar}>
                <button className={styles.toggleButton}>Menu</button>
            </div>
            <div className={styles.sidebar_menu}>
                <ul>
                    <li onClick={() => handleNavigation("welcome")}>Home</li>
                    <li onClick={() => handleNavigation("addApartment")}>Add Apartment</li>
                    <li onClick={() => handleNavigation("viewApartments")}>View Apartments</li>
                    <li onClick={() => handleNavigation("other-options")}>Other Options</li>
                    <li className={styles.logout} onClick={() => handleNavigation("logout")}>Logout</li>
                </ul>
            </div>
        </div>
    );
};

export default Sidebar;