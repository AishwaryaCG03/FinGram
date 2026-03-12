import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
from auth import init_db, init_session_state, login_page
from pages.meme_gallery import meme_gallery
from pages.savings_calculator import savings_calculator

# Initialize database and session state
init_db()
init_session_state()

# Page config - making it look aesthetic AF
st.set_page_config(
    page_title="FinGram",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make it look like a TikTok feed
st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: #ffffff;
    }
    .stButton button {
        background-color: #BC13FE;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        border: none;
    }
    .stTitle {
        font-family: 'Arial Black', sans-serif;
        color: #BC13FE;
    }
    </style>
    """, unsafe_allow_html=True)

# Check if user is logged in
if not st.session_state.logged_in:
    login_page()
else:
    # Main header
    st.title("💸 FinGram : Where Money Gets Real")
    st.markdown("### Because being broke isn't the aesthetic we're going for ")
    
    # Add logout button in sidebar
    if st.sidebar.button("Logout 👋"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # Sidebar for navigation
    st.sidebar.title("Vibe Check ✨")
    page = st.sidebar.selectbox(
        "What's the talk?",
        ["Home", "Money Memes", "Savings Calculator", "Investment Vibes"]
    )

    if page == "Home":
        col1, col2 = st.columns(2)
        
        with col1:
            st.header(f"Today's Financial Talk ☕")
            st.markdown(f"""
            Hey **{st.session_state.username}**, ready to get that bag? 
            
            - ✨ **Emergency Fund**: Your 'toxic debt was right' backup plan
            - 🎭 **Investing**: Making your money work harder than your backup plan
            - 💸 **Budgeting**: Main character energy for your wallet
            """)
        
        with col2:
            st.header("Trending Money Moves 🔥")
            st.metric(
                label="Savings Challenge",
                value="$100",
                delta="Better than your average credit score"
            )

    elif page == "Money Memes":
        meme_gallery()
        
    elif page == "Savings Calculator":
        savings_calculator()
        
    elif page == "Investment Vibes":
        st.header("Investment Vibes Check ✨")
        st.markdown("Coming soon! We're making it extra legendary! 🚀")

    # Footer
    st.markdown("---")
    st.markdown("Made with by a friend who wants you to get that bag") 