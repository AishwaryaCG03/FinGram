import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
def emi_calculator():
    if not st.session_state.logged_in:
        st.error("Bestie, you need to login first to see the tea! 🫖")
        return
    
    st.title(" EMI Calculator: Know Your Monthly Drama")
    st.markdown("### Because adulting is expensive and we need to know how much we're paying for that bag 💸")
    
    # Create a form for EMI calculation
    with st.form("emi_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Loan Details")
            loan_amount = st.number_input("Loan Amount (₹) 💰", min_value=1000, value=100000, step=1000)
            interest_rate = st.slider("Annual Interest Rate (%) 📊", min_value=1.0, max_value=30.0, value=10.0, step=0.1)
        
        with col2:
            st.subheader("Payment Details")
            loan_tenure_years = st.slider("Loan Tenure (Years) ⏳", min_value=1, max_value=30, value=5, step=1)
            down_payment = st.number_input("Down Payment (₹) 💵", min_value=0, value=0, step=1000)
        
        submitted = st.form_submit_button("Calculate That EMI Bestie 🚀")
    
    if submitted:
        # Calculate loan amount after down payment
        actual_loan_amount = loan_amount - down_payment
        
        # Calculate monthly interest rate
        monthly_interest_rate = (interest_rate / 100) / 12
        
        # Calculate number of monthly payments
        num_payments = loan_tenure_years * 12
        
        # Calculate EMI
        if monthly_interest_rate > 0:
            emi = actual_loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**num_payments / ((1 + monthly_interest_rate)**num_payments - 1)
        else:
            emi = actual_loan_amount / num_payments
            
        # Display results
        st.markdown("---")
        st.subheader("Your Financial Tea ☕")
        
        # Create metrics for key information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Monthly Payment",
                value=f"₹{emi:.2f}",
                delta="That's your monthly commitment bestie"
            )
        
        with col2:
            total_payment = emi * num_payments
            st.metric(
                label="Total Payment",
                value=f"₹{total_payment:.2f}",
                delta=f"₹{total_payment - actual_loan_amount:.2f} in interest"
            )
        
        with col3:
            st.metric(
                label="Total Interest",
                value=f"₹{total_payment - actual_loan_amount:.2f}",
                delta="That's a lot of chai money bestie"
            )
        
        # Create amortization schedule
        st.markdown("### Amortization Schedule 📊")
        st.markdown("See how your payments break down over time (because we love a good breakdown) ")
        
        # Create amortization data
        schedule_data = []
        remaining_balance = actual_loan_amount
        
        for month in range(1, num_payments + 1):
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = emi - interest_payment
            remaining_balance -= principal_payment
            
            schedule_data.append({
                "Month": month,
                "Payment": emi,
                "Principal": principal_payment,
                "Interest": interest_payment,
                "Remaining Balance": max(0, remaining_balance)
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(schedule_data)
        
        # Format currency columns
        df["Payment"] = df["Payment"].apply(lambda x: f"₹{x:.2f}")
        df["Principal"] = df["Principal"].apply(lambda x: f"₹{x:.2f}")
        df["Interest"] = df["Interest"].apply(lambda x: f"₹{x:.2f}")
        df["Remaining Balance"] = df["Remaining Balance"].apply(lambda x: f"₹{x:.2f}")
        
        # Display the first 12 months
        st.dataframe(df.head(12), use_container_width=True)
        
        # Create a button to show all months (outside the form)
        show_all = st.button("Show All Months Bestie")
        if show_all:
            st.dataframe(df, use_container_width=True)
        
        # Create visualizations
        st.markdown("### Visualize Your Financial Journey 📈")
        
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["Payment Breakdown", "Principal vs Interest", "Remaining Balance"])
        
        with tab1:
            # Payment breakdown over time
            # Convert back to numeric for plotting
            df_numeric = pd.DataFrame(schedule_data)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df_numeric["Month"], y=df_numeric["Principal"], name="Principal", marker_color="#FF3B5C"))
            fig.add_trace(go.Bar(x=df_numeric["Month"], y=df_numeric["Interest"], name="Interest", marker_color="#00F2EA"))
            fig.update_layout(
                title="Monthly Payment Breakdown Over Time",
                xaxis_title="Month",
                yaxis_title="Amount (₹)",
                barmode="stack",
                legend_title="Payment Type"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Principal vs Interest pie chart
            total_principal = df_numeric["Principal"].sum()
            total_interest = df_numeric["Interest"].sum()
            
            fig = px.pie(
                values=[total_principal, total_interest],
                names=["Principal", "Interest"],
                title="Total Payment Breakdown",
                color_discrete_sequence=["#FF3B5C", "#00F2EA"]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Remaining balance over time
            fig = px.line(
                df_numeric,
                x="Month",
                y="Remaining Balance",
                title="Remaining Loan Balance Over Time",
                line_shape="spline"
            )
            fig.update_traces(line_color="#FF3B5C")
            fig.update_layout(yaxis_title="Amount (₹)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Add some GenZ advice
        st.markdown("---")
        st.subheader("Financial Tea ☕")
        
        if interest_rate > 15:
            st.warning("Bestie, that interest rate is giving 'toxic ex' vibes! Consider looking for better rates or saving up more for a down payment. ")
        elif interest_rate > 10:
            st.info("That interest rate is giving 'situationship' vibes - not the worst, but you could do better! 💁‍♀️")
        else:
            st.success("That interest rate is giving 'main character energy'! You're slaying with those financial moves! ✨")
        
        # Add some tips
        st.markdown("### Pro Tips 💡")
        tips = [
            "**Extra Payments:** Making extra payments can significantly reduce your total interest. It's giving financial freedom! ",
            "**Refinancing:** If rates drop, consider refinancing your loan. It's like upgrading your ex to a better model! ✨",
            "**Down Payment:** A larger down payment means lower monthly payments. Your future self will thank you! 💸",
            "**Loan Term:** Shorter terms mean higher payments but less interest overall. Choose wisely bestie! 🧠",
            "**Credit Score:** A better credit score can get you lower interest rates. It's giving privilege! 💁‍♀️"
        ]
        
        for tip in tips:
            st.markdown(tip)

if __name__ == "__main__":
    emi_calculator() 
