import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# --- Profile Section ---
def get_user_scores(username):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    scores = c.execute('''SELECT category, score, total_questions, created_at FROM quiz_scores WHERE username = ? ORDER BY created_at DESC''', (username,)).fetchall()
    conn.close()
    return scores

def get_user_expenses(username):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    expenses = c.execute('''SELECT amount, category, description, date FROM expenses WHERE username = ?''', (username,)).fetchall()
    conn.close()
    return expenses

def profile_view():
    if not st.session_state.get('logged_in', False):
        st.error("Bestie, login first! 🫖")
        return
    username = st.session_state.username
    st.title(f"👑 {username}'s Financial Empire")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Quiz Achievements 🏆")
        scores = get_user_scores(username)
        if scores:
            df = pd.DataFrame(scores, columns=["Category", "Score", "Total", "Date"])
            df['Percentage'] = (df['Score'] / df['Total']) * 100
            st.metric("Total Quizzes Slayed", len(df))
            st.metric("Avg Slay Rate", f"{df['Percentage'].mean():.1f}%")
            st.dataframe(df[['Category', 'Score', 'Total', 'Date']].head(5), use_container_width=True)
            st.plotly_chart(px.pie(df, names='Category', title="Your Knowledge Portfolio 📚"), use_container_width=True)
        else: st.info("No quizzes taken yet! ✍️")
    with col2:
        st.header("Expense Vibe Check 💸")
        expenses = get_user_expenses(username)
        if expenses:
            df = pd.DataFrame(expenses, columns=["Amount", "Category", "Description", "Date"])
            st.metric("Total Bag Spent", f"₹{df['Amount'].sum():,.2f}")
            cat_breakdown = df.groupby('Category')['Amount'].sum().reset_index()
            st.plotly_chart(px.bar(cat_breakdown, x='Category', y='Amount', title="Where Your Coins Are Going 🛍️", color='Category'), use_container_width=True)
            st.dataframe(cat_breakdown.sort_values(by='Amount', ascending=False), use_container_width=True)
        else: st.info("No expenses tracked yet! 💰")

# --- Problem Solver Section ---
def init_problem_solver_db():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS financial_problems (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, problem TEXT, created_at TIMESTAMP, FOREIGN KEY (username) REFERENCES users(username))''')
    conn.commit()
    conn.close()

def save_problem(username, problem):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    c.execute('''INSERT INTO financial_problems (username, problem, created_at) VALUES (?, ?, ?)''', (username, problem, datetime.now()))
    conn.commit()
    conn.close()

def get_problems():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    problems = c.execute('''SELECT id, username, problem, created_at FROM financial_problems ORDER BY created_at DESC''').fetchall()
    conn.close()
    return problems

def generate_meme_response(problem):
    responses = {"budget": ["Bestie, your budget is giving 'I don't know her' vibes ", "That budget is more broken than my ex's promises 😭"], "default": ["That's giving 'main character era' ✨", "Your financial situation is giving 'villain origin story' 🖤"]}
    advice = {"budget": ["**Real Talk Bestie:** Try the 50/30/20 rule! 💅", "**Financial Tea:** Track spending with an app! ✨"], "default": ["**Real Talk Bestie:** Start by tracking all expenses for a month! 💅", "**Financial Tea:** Set specific goals! ✨"]}
    problem_lower = problem.lower()
    if "budget" in problem_lower: return random.choice(responses["budget"]), random.choice(advice["budget"])
    else: return random.choice(responses["default"]), random.choice(advice["default"])

def problem_solver():
    if not st.session_state.logged_in:
        st.error("Bestie, login first! 🫖")
        return
    init_problem_solver_db()
    st.title(" Financial Problem Solver")
    with st.form("problem_form"):
        st.subheader("What's the financial tea? ☕")
        problem = st.text_area("Drop your financial problem here! 💸", placeholder="Example: I can't stop spending on coffee...")
        if st.form_submit_button("Get That Tea 🚀") and problem:
            save_problem(st.session_state.username, problem)
            st.success("Your tea has been spilled! 🫖")
            st.rerun()
    st.markdown("---")
    st.subheader("Recent Financial Tea ☕")
    problems = get_problems()
    if not problems: st.info("No tea spilled yet! 🫖")
    else:
        for p_id, user, p_text, created_at in problems:
            with st.expander(f"Tea from {user} - {created_at}", expanded=False):
                st.markdown(f"**Problem:** {p_text}")
                res, adv = generate_meme_response(p_text)
                st.markdown(f"**GenZ Response:** {res}")
                st.markdown("---")
                st.markdown(f"### 💰 Advice 💰\n{adv}")

# --- Feedback Section ---
def feedback_form():
    if not st.session_state.logged_in:
        st.error("Bestie, login first! 🫖")
        return
    st.title("💅 Feedback Form")
    st.markdown("### Spill the tea on your experience! ✨")
    with st.form("feedback_form"):
        st.subheader("How's the vibe? 🌟")
        rating = st.slider("Rate your experience", 1, 5, 3, help="1 = Not it, 5 = Slayed!", format="%d ⭐")
        st.subheader("What's the tea? 🫖")
        feedback_text = st.text_area("Tell us what you think", placeholder="Spill the tea bestie! 💅")
        feature_request = st.text_area("Feature requests", placeholder="What features would make this app even more iconic? ✨")
        if st.form_submit_button("Submit Feedback Bestie! 💅"):
            if feedback_text or feature_request:
                st.success("Thanks for the feedback bestie! You're the best! ✨")
                st.balloons()
            else: st.error("Bestie, give us some tea! 💁‍♀️")
