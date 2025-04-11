import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
from auth import init_db, init_session_state, login_page
from pages.meme_gallery import meme_gallery
from pages.savings_calculator import savings_calculator
from pages.problem_solver import problem_solver
from pages.emi_calculator import emi_calculator
from pages.finance_quiz import finance_quiz
from pages.expense_tracker import expense_tracker
from pages.feedback import feedback_form

# Initialize database and session state
init_db()
init_session_state()

# Page config - making it look aesthetic AF
st.set_page_config(
    page_title="FinGram ",
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
        background-color: #FF3B5C;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        border: none;
    }
    .stTitle {
        font-family: 'Arial Black', sans-serif;
        color: #FF3B5C;
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
        "What's the tea?",
        ["Home", "Money Memes", "Savings Calculator", "Investment Vibes", "Problem Solver", "EMI Calculator", "Finance Quiz", "Expense Tracker", "Feedback"]
    )

    if page == "Home":
        col1, col2 = st.columns(2)
        
        with col1:
            st.header(f"Today's Financial Tea ☕")
            st.markdown(f"""
            Hey **{st.session_state.username}**, ready to get that bag? 
            
            - 💅 **Emergency Fund**: Your 'toxic ex was right' backup plan
            - 🎭 **Investing**: Making your money work harder than your situationship
            - 💸 **Budgeting**: Main character energy for your wallet
            """)
        
        with col2:
            st.header("Trending Money Moves 🔥")
            st.metric(
                label="Savings Challenge",
                value="₹1000",
                delta="Better than your ex's credit score"
            )

    elif page == "Money Memes":
        meme_gallery()
        
    elif page == "Savings Calculator":
        savings_calculator()
        
    elif page == "Investment Vibes":
        st.header("Investment Vibes Check ✨")
        # Add investment content here
        
    elif page == "Problem Solver":
        problem_solver()
        
    elif page == "EMI Calculator":
        emi_calculator()
        
    elif page == "Finance Quiz":
        finance_quiz()
        
    elif page == "Expense Tracker":
        expense_tracker()
        
    elif page == "Feedback":
        feedback_form()

    # Footer
    st.markdown("---")
    st.markdown("Made with by a bestie who wants you to get that bag") 