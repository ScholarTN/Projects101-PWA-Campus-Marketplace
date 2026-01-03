import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta
import json

class CookiesManager:
    COOKIE_NAME = "campus_marketplace_session"

    @staticmethod
    def get_manager():
        """
        Initialize the cookie manager. 
        IMPORTANT: This must be called at the start of the app layout.
        """
        # This creates a singleton instance in session state to avoid re-initializing
        if 'cookie_manager' not in st.session_state:
            st.session_state.cookie_manager = stx.CookieManager()
        return st.session_state.cookie_manager

    @staticmethod
    def set_session_cookie(user_id: str, email: str, access_token: str, refresh_token: str):
        manager = CookiesManager.get_manager()
        
        cookie_payload = {
            "user_id": user_id,
            "email": email,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        
        # Save to browser (expires in 7 days)
        # Note: We verify persistence by saving it as a stringified JSON
        manager.set(
            CookiesManager.COOKIE_NAME, 
            json.dumps(cookie_payload), 
            expires_at=datetime.now() + timedelta(days=7)
        )

    @staticmethod
    def get_session_cookie():
        manager = CookiesManager.get_manager()
        # This gets the actual browser cookie
        cookie_val = manager.get(CookiesManager.COOKIE_NAME)
        
        if cookie_val:
            try:
                return json.loads(cookie_val)
            except:
                return None
        return None

    @staticmethod
    def clear_session_cookie():
        manager = CookiesManager.get_manager()
        manager.delete(CookiesManager.COOKIE_NAME)
        
    @staticmethod
    def get_access_token():
        data = CookiesManager.get_session_cookie()
        return data.get('user_id') if data else "None - noid"