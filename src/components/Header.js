import React, { useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import SearchBar from './SearchBar';
import NotificationBell from './NotificationBell';
import AuthModal from './AuthModal';

function Header() {
  const { currentUser, logout } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState('login');
  const history = useHistory();

  const handleAuthClick = (mode) => {
    setAuthMode(mode);
    setShowAuthModal(true);
  };

  const handleSearch = (query) => {
    history.push(`/search?q=${encodeURIComponent(query)}`);
  };

  return (
    <header className="app-header">
      <nav>
        <Link to="/" className="logo">Campus Marketplace</Link>
        
        <SearchBar onSearch={handleSearch} />
        
        <div className="nav-links">
          <Link to="/buy">Buy Items</Link>
          <Link to="/housing">Housing</Link>
          
          {currentUser ? (
            <>
              {currentUser.userType === 'student' && <Link to="/sell">Sell</Link>}
              {currentUser.userType === 'landlord' && <Link to="/housing/add">List Property</Link>}
              <Link to="/messages"><i className="fas fa-envelope"></i></Link>
              <NotificationBell />
              <Link to="/profile">Profile</Link>
              <button onClick={logout}>Logout</button>
            </>
          ) : (
            <>
              <button onClick={() => handleAuthClick('login')}>Login</button>
              <button onClick={() => handleAuthClick('signup')}>Sign Up</button>
            </>
          )}
        </div>
      </nav>
      
      {showAuthModal && (
        <AuthModal 
          mode={authMode} 
          onClose={() => setShowAuthModal(false)}
        />
      )}
    </header>
  );
}

export default Header;