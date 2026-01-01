#module code to create and validate session cookies. Too bad i used a class

import streamlit as st
from datetime import datetime, timedelta
import json

class CookiesManager:
    """Manages user session cookies for login persistence."""
    
    COOKIE_NAME = "campus_marketplace_session"
    COOKIE_EXPIRY_DAYS = 7
    
    @staticmethod
    def set_session_cookie(user_id: str, email: str, access_token: str, refresh_token: str = None):
        """
        Store user session data in Streamlit session state (simulating cookies).
        
        Args:
            user_id: User's unique identifier
            email: User's email
            access_token: JWT access token from Supabase
            refresh_token: Optional refresh token
        """
        cookie_data = {
            "user_id": user_id,
            "email": email,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=CookiesManager.COOKIE_EXPIRY_DAYS)).isoformat()
        }
        
        st.session_state[CookiesManager.COOKIE_NAME] = cookie_data
    
    @staticmethod
    def get_session_cookie() -> dict or None:
        """
        Retrieve user session data from cookies.
        
        Returns:
            Dictionary with session data if valid, None otherwise
        """
        if CookiesManager.COOKIE_NAME not in st.session_state:
            return None
        
        cookie_data = st.session_state[CookiesManager.COOKIE_NAME]
        
        # Check if cookie has expired
        expires_at = datetime.fromisoformat(cookie_data.get("expires_at"))
        if datetime.now() > expires_at:
            CookiesManager.clear_session_cookie()
            return None
        
        return cookie_data
    
    @staticmethod
    def clear_session_cookie():
        """Clear user session cookies (logout)."""
        if CookiesManager.COOKIE_NAME in st.session_state:
            del st.session_state[CookiesManager.COOKIE_NAME]
    
    @staticmethod
    def is_user_logged_in() -> bool:
        """Check if user has a valid session cookie."""
        return CookiesManager.get_session_cookie() is not None
    
    @staticmethod
    def get_user_email() -> str or None:
        """Get email from session cookie."""
        cookie_data = CookiesManager.get_session_cookie()
        return cookie_data.get("email") if cookie_data else None
    
    @staticmethod
    def get_access_token() -> str or None:
        """Get access token from session cookie."""
        cookie_data = CookiesManager.get_session_cookie()
        return cookie_data.get("access_token") if cookie_data else None


    #code for checking if session is valid
    @staticmethod
    def is_session_valid(session_token: str, email: str) -> bool:
        """
        Validate session token and email against session cookie data.
        
        Args:
            session_token: JWT access token from Supabase
            email: User's email
        
        Returns:
            True if session token and email match session cookie data, False otherwise
        """
        cookie_data = CookiesManager.get_session_cookie()
        if not cookie_data:
            return False
        
        return cookie_data.get("access_token") == session_token and cookie_data.get("email") == email
