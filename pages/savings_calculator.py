import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def calculate_savings(initial_amount, monthly_savings, interest_rate, years):
    # Convert annual interest rate to monthly
    monthly_rate = interest_rate / 12 / 100
    
    # Calculate number of months
    months = years * 12
    
    # Initialize lists for tracking
    dates = []
    balances = []
    contributions = []
    interests = []
    
    # Initial values
    current_balance = initial_amount
    total_contributions = initial_amount
    
    # Calculate for each month
    for month in range(months + 1):
        dates.append(datetime.now() + timedelta(days=30*month))
        balances.append(current_balance)
        contributions.append(total_contributions)
        interests.append(current_balance - total_contributions)
        
        # Add monthly savings
        current_balance += monthly_savings
        total_contributions += monthly_savings
        
        # Add interest
        current_balance *= (1 + monthly_rate)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Balance': balances,
        'Contributions': contributions,
        'Interest': interests
    })
    
    return df

def savings_calculator():
    st.title("💅 Savings Calculator")
    st.markdown("### Plan your glow-up journey bestie! ✨")
    
    # Input form
    with st.form("savings_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            initial_amount = st.number_input(
                "Initial Amount (₹)",
                min_value=0,
                value=10000,
                step=1000,
                help="How much you're starting with bestie"
            )
            
            monthly_savings = st.number_input(
                "Monthly Savings (₹)",
                min_value=0,
                value=5000,
                step=500,
                help="How much you'll save each month"
            )
        
        with col2:
            interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.0,
                max_value=20.0,
                value=6.0,
                step=0.1,
                help="Expected annual return on your savings"
            )
            
            years = st.number_input(
                "Time Period (Years)",
                min_value=1,
                max_value=50,
                value=5,
                step=1,
                help="How long you'll keep this up bestie"
            )
        
        submit = st.form_submit_button("Calculate My Future Bag 💅")
    
    if submit:
        # Calculate savings
        df = calculate_savings(initial_amount, monthly_savings, interest_rate, years)
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Final Balance",
                f"₹{df['Balance'].iloc[-1]:,.2f}",
                f"₹{df['Balance'].iloc[-1] - df['Balance'].iloc[0]:,.2f}"
            )
        
        with col2:
            st.metric(
                "Total Contributions",
                f"₹{df['Contributions'].iloc[-1]:,.2f}",
                f"₹{df['Contributions'].iloc[-1] - df['Contributions'].iloc[0]:,.2f}"
            )
        
        with col3:
            st.metric(
                "Interest Earned",
                f"₹{df['Interest'].iloc[-1]:,.2f}",
                f"₹{df['Interest'].iloc[-1] - df['Interest'].iloc[0]:,.2f}"
            )
        
        # Create charts
        fig1 = px.line(df, x='Date', y=['Balance', 'Contributions'],
                      title='Your Money Growth Journey 💸',
                      labels={'value': 'Amount (₹)', 'variable': 'Type'})
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = px.area(df, x='Date', y=['Contributions', 'Interest'],
                      title='Contributions vs Interest Earned 💅',
                      labels={'value': 'Amount (₹)', 'variable': 'Type'})
        st.plotly_chart(fig2, use_container_width=True)
        
        # Monthly breakdown
        st.subheader("Monthly Breakdown 📊")
        monthly_df = df.set_index('Date').resample('M').last()
        monthly_df['Monthly Growth'] = monthly_df['Balance'].diff()
        st.dataframe(monthly_df[['Balance', 'Monthly Growth']].style.format({
            'Balance': '₹{:,.2f}',
            'Monthly Growth': '₹{:,.2f}'
        }))

if __name__ == "__main__":
    savings_calculator() 