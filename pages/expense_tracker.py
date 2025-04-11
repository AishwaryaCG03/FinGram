import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import json

def init_expense_db():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    # Create expenses table
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
        st.error("Bestie, you need to login first to track your expenses! 🫖")
        return
    
    # Initialize database
    init_expense_db()
    
    st.title(" Expense Tracker")
    st.markdown("### Track your coins and split bills like a boss! ✨")
    
    # Expense categories
    categories = [
        "Food & Drinks 🍕",
        "Shopping 🛍️",
        "Transportation 🚗",
        "Entertainment 🎮",
        "Bills & Utilities 📱",
        "Health & Fitness 💪",
        "Education 📚",
        "Travel ✈️",
        "Other 💅"
    ]
    
    # Create two columns for the form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Add New Expense 💸")
        with st.form("expense_form"):
            amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
            category = st.selectbox("Category", categories)
            description = st.text_input("Description")
            date = st.date_input("Date")
            
            # Bill splitting section
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
                    save_expense(
                        st.session_state.username,
                        amount,
                        category,
                        description,
                        date.strftime("%Y-%m-%d"),
                        split_with if split_bill else None,
                        split_amount if split_bill else None
                    )
                    st.success("Expense added! You're giving organized queen energy! ✨")
                else:
                    st.error("Bestie, fill in all the details! 💁‍♀️")
    
    with col2:
        st.subheader("Your Expenses 📊")
        expenses = get_expenses(st.session_state.username)
        
        if expenses:
            df = pd.DataFrame(expenses, columns=[
                "Amount", "Category", "Description", "Date", "Split With", "Split Amount"
            ])
            
            # Calculate total expenses
            total_expenses = df["Amount"].sum()
            st.metric("Total Expenses", f"₹{total_expenses:,.2f}")
            
            # Show expenses table
            st.dataframe(df, use_container_width=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Expenses Bestie! 📥",
                data=csv,
                file_name="expenses.csv",
                mime="text/csv"
            )
        else:
            st.info("No expenses yet bestie! Start tracking your coins! ")

if __name__ == "__main__":
    expense_tracker() 