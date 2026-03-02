import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Expense Tracker Section ---
def init_expense_db():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  amount REAL,
                  category TEXT,
                  description TEXT,
                  date TEXT,
                  split_with TEXT,
                  split_amount REAL,
                  created_at TIMESTAMP,
                  FOREIGN KEY (username) REFERENCES users(username))''')
    conn.commit()
    conn.close()

def save_expense(username, amount, category, description, date, split_with=None, split_amount=None):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    c.execute('''INSERT INTO expenses 
                 (username, amount, category, description, date, split_with, split_amount, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (username, amount, category, description, date, split_with, split_amount, datetime.now()))
    conn.commit()
    conn.close()

def get_expenses(username):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    expenses = c.execute('''SELECT amount, category, description, date, split_with, split_amount 
                           FROM expenses 
                           WHERE username = ? 
                           ORDER BY date DESC''', (username,)).fetchall()
    conn.close()
    return expenses

def expense_tracker():
    if not st.session_state.logged_in:
        st.error("Bestie, login first! 🫖")
        return
    init_expense_db()
    st.title(" Expense Tracker")
    st.markdown("### Track your coins and split bills like a boss! ✨")
    categories = ["Food & Drinks 🍕", "Shopping 🛍️", "Transportation 🚗", "Entertainment 🎮", "Bills & Utilities 📱", "Health & Fitness 💪", "Education 📚", "Travel ✈️", "Other 💅"]
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Add New Expense 💸")
        with st.form("expense_form"):
            amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
            category = st.selectbox("Category", categories)
            description = st.text_input("Description")
            date = st.date_input("Date")
            st.markdown("### Split the Bill? 💁‍♀️")
            split_bill = st.checkbox("Split this expense")
            if split_bill:
                split_with = st.text_input("Split with (comma-separated names)")
                split_ways = st.number_input("Split into how many ways?", min_value=2, value=2)
                split_amount = amount / split_ways if split_ways > 0 else amount
                st.info(f"Each person pays: ₹{split_amount:.2f}")
            submit = st.form_submit_button("Add Expense Bestie! ")
            if submit:
                if amount > 0 and category and description:
                    save_expense(st.session_state.username, amount, category, description, date.strftime("%Y-%m-%d"), split_with if split_bill else None, split_amount if split_bill else None)
                    st.success("Expense added! You're giving organized queen energy! ✨")
                else:
                    st.error("Bestie, fill in all the details! 💁‍♀️")
    with col2:
        st.subheader("Your Expenses 📊")
        expenses = get_expenses(st.session_state.username)
        if expenses:
            df = pd.DataFrame(expenses, columns=["Amount", "Category", "Description", "Date", "Split With", "Split Amount"])
            total_expenses = df["Amount"].sum()
            st.metric("Total Expenses", f"₹{total_expenses:,.2f}")
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            st.download_button(label="Download Expenses Bestie! 📥", data=csv, file_name="expenses.csv", mime="text/csv")
        else:
            st.info("No expenses yet bestie! Start tracking your coins! ")

# --- EMI Calculator Section ---
def emi_calculator():
    if not st.session_state.logged_in:
        st.error("Bestie, login first! 🫖")
        return
    st.title(" EMI Calculator")
    st.markdown("### Know Your Monthly Drama 💸")
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
        actual_loan_amount = loan_amount - down_payment
        monthly_interest_rate = (interest_rate / 100) / 12
        num_payments = loan_tenure_years * 12
        if monthly_interest_rate > 0:
            emi = actual_loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**num_payments / ((1 + monthly_interest_rate)**num_payments - 1)
        else:
            emi = actual_loan_amount / num_payments
        st.markdown("---")
        st.subheader("Your Financial Tea ☕")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Monthly Payment", value=f"₹{emi:.2f}", delta="Monthly commitment")
        with col2:
            total_payment = emi * num_payments
            st.metric(label="Total Payment", value=f"₹{total_payment:.2f}", delta=f"₹{total_payment - actual_loan_amount:.2f} in interest")
        with col3:
            st.metric(label="Total Interest", value=f"₹{total_payment - actual_loan_amount:.2f}", delta="A lot of chai money")
        schedule_data = []
        remaining_balance = actual_loan_amount
        for month in range(1, num_payments + 1):
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = emi - interest_payment
            remaining_balance -= principal_payment
            schedule_data.append({"Month": month, "Payment": emi, "Principal": principal_payment, "Interest": interest_payment, "Remaining Balance": max(0, remaining_balance)})
        df = pd.DataFrame(schedule_data)
        st.markdown("### Visualize Your Financial Journey 📈")
        tab1, tab2, tab3 = st.tabs(["Payment Breakdown", "Principal vs Interest", "Remaining Balance"])
        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df["Month"], y=df["Principal"], name="Principal", marker_color="#FF3B5C"))
            fig.add_trace(go.Bar(x=df["Month"], y=df["Interest"], name="Interest", marker_color="#00F2EA"))
            fig.update_layout(title="Monthly Payment Breakdown", barmode="stack")
            st.plotly_chart(fig, use_container_width=True)
        with tab2:
            fig = px.pie(values=[df["Principal"].sum(), df["Interest"].sum()], names=["Principal", "Interest"], title="Total Payment Breakdown", color_discrete_sequence=["#FF3B5C", "#00F2EA"])
            st.plotly_chart(fig, use_container_width=True)
        with tab3:
            fig = px.line(df, x="Month", y="Remaining Balance", title="Remaining Balance Over Time")
            fig.update_traces(line_color="#FF3B5C")
            st.plotly_chart(fig, use_container_width=True)

# --- Savings Calculator Section ---
def calculate_savings(initial_amount, monthly_savings, interest_rate, years):
    monthly_rate = interest_rate / 12 / 100
    months = years * 12
    dates, balances, contributions, interests = [], [], [], []
    current_balance = initial_amount
    total_contributions = initial_amount
    for month in range(months + 1):
        dates.append(datetime.now() + timedelta(days=30*month))
        balances.append(current_balance)
        contributions.append(total_contributions)
        interests.append(current_balance - total_contributions)
        current_balance += monthly_savings
        total_contributions += monthly_savings
        current_balance *= (1 + monthly_rate)
    return pd.DataFrame({'Date': dates, 'Balance': balances, 'Contributions': contributions, 'Interest': interests})

def savings_calculator():
    st.title("💅 Savings Calculator")
    st.markdown("### Plan your glow-up journey bestie! ✨")
    with st.form("savings_form"):
        col1, col2 = st.columns(2)
        with col1:
            initial_amount = st.number_input("Initial Amount (₹)", min_value=0, value=10000, step=1000)
            monthly_savings = st.number_input("Monthly Savings (₹)", min_value=0, value=5000, step=500)
        with col2:
            interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=20.0, value=6.0, step=0.1)
            years = st.number_input("Time Period (Years)", min_value=1, max_value=50, value=5, step=1)
        submit = st.form_submit_button("Calculate My Future Bag 💅")
    if submit:
        df = calculate_savings(initial_amount, monthly_savings, interest_rate, years)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Final Balance", f"₹{df['Balance'].iloc[-1]:,.2f}", f"₹{df['Balance'].iloc[-1] - df['Balance'].iloc[0]:,.2f}")
        with col2:
            st.metric("Total Contributions", f"₹{df['Contributions'].iloc[-1]:,.2f}", f"₹{df['Contributions'].iloc[-1] - df['Contributions'].iloc[0]:,.2f}")
        with col3:
            st.metric("Interest Earned", f"₹{df['Interest'].iloc[-1]:,.2f}", f"₹{df['Interest'].iloc[-1] - df['Interest'].iloc[0]:,.2f}")
        fig1 = px.line(df, x='Date', y=['Balance', 'Contributions'], title='Your Money Growth Journey 💸')
        st.plotly_chart(fig1, use_container_width=True)
        fig2 = px.area(df, x='Date', y=['Contributions', 'Interest'], title='Contributions vs Interest 💅')
        st.plotly_chart(fig2, use_container_width=True)
