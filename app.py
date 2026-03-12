import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
from auth import init_db, init_session_state, login_page
from pages.learning_hub import meme_gallery, finance_quiz, investment_vibes
from pages.financial_tools import expense_tracker, savings_calculator, emi_calculator
from pages.user_hub import profile_view, problem_solver, feedback_form

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
    # Sidebar for navigation at the top
    st.sidebar.title("Vibe Check ✨")
    page = st.sidebar.selectbox(
        "What's the talk?",
        ["Dashboard 🔥", "Money Tools 💸", "Play & Learn 🎭", "Feedback ✨"]
    )

    # Main header
    st.title("💸 FinGram : Where Money Gets Real")
    st.markdown("### Because being broke isn't the aesthetic we're going for ")
    
    if page == "Dashboard 🔥":
        tab1, tab2 = st.tabs(["Home 🏠", "My Stats 📊"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.header(f"Today's Financial Talk ☕")
                st.markdown(f"""
                Hey **{st.session_state.username}**, ready to get that bag? 
                
                - ✨ **Emergency Fund**: Your 'toxic debt was right' backup plan
                - 🎭 **Investing**: Making your money work harder than your backup plan
                - 💸 **Budgeting**: Main character energy for your wallet
                """)
                
                st.info("Check the **My Stats** tab for your latest scores and expense tracking! 📊")
            
            with col2:
                st.header("Trending Money Moves 🔥")
                st.metric(
                    label="Savings Challenge",
                    value="₹1000",
                    delta="Better than your average credit score"
                )
                
                st.markdown("---")
                st.subheader("Vibe of the Day ✨")
                tips = [
                    "Cancel that subscription you haven't used in 3 months! ✂️",
                    "Invest ₹500 today - future you will legendary! 💸",
                    "Review your expenses - no shade, just awareness! 👀"
                ]
                import random
                st.write(random.choice(tips))
        
        with tab2:
            profile_view()

    elif page == "Money Tools 💸":
        tab1, tab2, tab3, tab4 = st.tabs([
            "Expense Tracker 💸", 
            "Savings Calculator 💰", 
            "Investment Vibes ✨", 
            "EMI Calculator 📈"
        ])
        
        with tab1:
            expense_tracker()
        with tab2:
            savings_calculator()
        with tab3:
            investment_vibes()
        with tab4:
            emi_calculator()
            
    elif page == "Play & Learn 🎭":
        tab1, tab2, tab3 = st.tabs([
            "Money Memes 🔥", 
            "Finance Quiz 📝", 
            "Problem Solver ☕"
        ])
        
        with tab1:
            meme_gallery()
        with tab2:
            finance_quiz()
        with tab3:
            problem_solver()
        
    elif page == "Feedback ✨":
        feedback_form()

    # Sidebar Logout at the bottom
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout 👋"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("Made with by a friend who wants you to get that bag") 