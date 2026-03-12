import streamlit as st
import plotly.express as px
import pandas as pd

def calculate_savings(monthly_save, years, interest_rate):
    months = years * 12
    monthly_rate = interest_rate / 100 / 12
    future_value = 0
    savings_data = []
    
    for month in range(months + 1):
        future_value = (future_value + monthly_save) * (1 + monthly_rate)
        savings_data.append({
            'Month': month,
            'Savings': future_value,
            'Year': month // 12
        })
    
    return pd.DataFrame(savings_data)

def savings_calculator():
    st.title("✨ Savings Calculator")
    st.markdown("### Because we're trying to get wealthy, legend!")
    
    # User inputs
    col1, col2 = st.columns(2)
    with col1:
        current_savings = st.number_input("How much you got now? (₹)", min_value=0, value=1000, step=100)
        monthly_contribution = st.number_input("Monthly deposit (₹)", min_value=0, value=500, step=50)
    
    with col2:
        interest_rate = st.slider("Annual Interest Rate (%)", min_value=0.0, max_value=15.0, value=7.0, step=0.1)
        years = st.slider("Time horizon (Years)", min_value=1, max_value=40, value=5)

    # Calculate future value
    # Formula: FV = P(1 + r/n)^(nt) + PMT * [((1 + r/n)^(nt) - 1) / (r/n)]
    n = 12 # monthly compounding
    r = interest_rate / 100
    t = years
    
    future_value = current_savings * (1 + r/n)**(n*t) + monthly_contribution * (((1 + r/n)**(n*t) - 1) / (r/n))
    
    st.markdown("---")
    st.header(f"In {years} years, you'll have:")
    st.title(f"₹{future_value:,.2f} 💰")
    
    # Motivation
    if future_value > 100000:
        st.success("That's a whole lot of bag! Keep going! 🚀")
    elif future_value > 50000:
        st.info("Solid growth! Future you is vibing! ✨")
    else:
        st.warning("Every coin counts! Start small, finish big! 🔥")

    # Fun breakdown
    st.markdown("### How to get there faster:")
    st.markdown(f"""
    - **Total invested**: ₹{current_savings + (monthly_contribution * 12 * years):,.2f}
    - **Interest earned**: ₹{future_value - (current_savings + (monthly_contribution * 12 * years)):,.2f}
    - Skip the daily iced coffee (jk friend, treat yourself) ☕
    """)