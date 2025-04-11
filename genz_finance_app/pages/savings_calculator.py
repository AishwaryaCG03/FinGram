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
    if not st.session_state.logged_in:
        st.error("Bestie, you need to login first to see the tea! 🫖")
        return

    st.title("💰 Savings Calculator: Get That Bag! ")
    st.markdown("### Because we're trying to get rich, bestie!")

    col1, col2 = st.columns(2)

    with col1:
        monthly_save = st.slider(
            "Monthly Savings (Your 'No Starbucks' Money) 🧋",
            min_value=10,
            max_value=1000,
            value=100,
            step=10
        )
        
        years = st.slider(
            "Years (How long till main character status) ⭐",
            min_value=1,
            max_value=30,
            value=5
        )
        
        interest_rate = st.slider(
            "Interest Rate (The tea your bank spills) % 📈",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.1
        )

    # Calculate savings
    df = calculate_savings(monthly_save, years, interest_rate)
    
    with col2:
        final_amount = df['Savings'].iloc[-1]
        st.metric(
            label="Final Bag 💰",
            value=f"${final_amount:,.2f}",
            delta=f"Started from ${monthly_save:,.2f}/month"
        )

    # Create a plotly chart that's giving Instagram aesthetic
    fig = px.line(
        df,
        x='Month',
        y='Savings',
        title="Your Money Glow Up !!",
        labels={'Savings': 'Total Savings ($)', 'Month': 'Months'},
    )
    
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Add some motivational content
    st.markdown("""
    ### Quick Money Tips That Slap 👏
    - Skip the daily iced coffee (jk bestie, treat yourself) ☕
    - Use that student discount like it's your job 🎓
    - Invest in index funds (boring but boujee) 📈
    - Start an emergency fund (for when the main character needs a plot twist) 🎭
    """) 