import streamlit as st

# Set page config
st.set_page_config(page_title="404 Page Not Found", layout="centered")

def error_404():
    # Custom CSS for styling
    st.markdown("""
        <style>
        body {
            background: linear-gradient(135deg, #a1c4fd, #d4a5ff);
        }
        .error-card {
            background-color: white;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 600px;
            margin: auto;
        }
        .error-code {
            font-size: 96px;
            font-weight: bold;
            background: linear-gradient(135deg, #d4a5ff, #a1c4fd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .error-title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 1rem;
        }
        .error-message {
            font-size: 16px;
            color: #666;
            margin-bottom: 2rem;
        }
        .button-row {
            display: flex;
            justify-content: center;
            gap: 1rem;
        }
        .stButton > button {
            border-radius: 6px;
            padding: 0.75rem 1.5rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # HTML layout
    st.markdown("""
        <div class="error-card">
            <div class="error-code">404</div>
            <div class="error-title">Oops! Page Not Found</div>
            <div class="error-message">
                Sorry, the page you're looking for doesn't exist.<br>
                If you think something is broken, report a problem.
            </div>
        </div>
        <br>
    """, unsafe_allow_html=True)


    # # Buttons
    col1, col2, col3, col4, col5 = st.columns([2, 1, 0.5, 1, 2])

    with col2:
        if st.button("Return Home"):
            st.session_state.page = "home"
            st.rerun()

    with col4:
        if st.button("Report Error"):
            st.info("Redirecting to report form...")
