import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import random
from datetime import datetime
import os
import google.generativeai as genai
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

# --- Local AI Knowledge Base ---
KNOWLEDGE_BASE = {
    "budgeting": {
        "problems": [
            "I spend too much on coffee and dining out",
            "I can't stick to a budget",
            "I don't know where my money goes",
            "How to save money on rent and bills",
            "I want to start budgeting but don't know how"
        ],
        "response": "Bestie, your budget is giving 'I don't know her' vibes 👩‍🦯",
        "advice": """
        - **Try the 50/30/20 rule**: 50% for needs, 30% for wants, 20% for savings. It's the ultimate slay! 💅
        - **Track everything**: Use the Expense Tracker tab to see exactly where your bag is leaking. No cap! 💸
        - **Automate your savings**: Set up a direct transfer to your savings account on payday. Future you will thank you! ✨
        """
    },
    "investing": {
        "problems": [
            "How to start investing in stocks",
            "What are mutual funds and index funds",
            "Is crypto a good investment",
            "I'm scared of losing money in the market",
            "When is the best time to start investing"
        ],
        "response": "Investing is giving 'main character energy' 👑",
        "advice": """
        - **Start small with Index Funds**: They are stable, reliable, and perfect for long-term growth. No gatekeeping here! 📈
        - **Time in the market > Timing the market**: The earlier you start, the more compound interest works its magic. Slay! ✨
        - **Diversify your portfolio**: Don't put all your coins in one basket (or one meme coin). Stay balanced, bestie! ⚖️
        """
    },
    "debt": {
        "problems": [
            "I have too much credit card debt",
            "How to pay off student loans faster",
            "I'm struggling with high interest rates",
            "Should I pay off debt or save money first",
            "I feel overwhelmed by my monthly payments"
        ],
        "response": "Debt is giving 'toxic ex' vibes and we need to block it 🚫",
        "advice": """
        - **Debt Snowball Method**: Pay off the smallest debts first to get those quick wins and momentum. You got this! 🔥
        - **Debt Avalanche Method**: Focus on the debt with the highest interest rate first to save money in the long run. Big brain moves! 🧠
        - **Negotiate your rates**: Call your bank and ask for a lower interest rate. If you don't ask, the answer is always no, bestie! 📞
        """
    },
    "savings": {
        "problems": [
            "I want to save for a vacation or a new phone",
            "How much should I have in my emergency fund",
            "I struggle to save any money at the end of the month",
            "Best ways to save money as a student",
            "I want to build a house or buy a car"
        ],
        "response": "Saving for your goals is the ultimate glow-up! ✨",
        "advice": """
        - **Emergency Fund is a must**: Aim for 3-6 months of expenses. It's your 'toxic situationship' backup plan! 💅
        - **Use the 'Pay Yourself First' method**: Treat your savings like a bill that must be paid first. Period! 💸
        - **High-Yield Savings Accounts (HYSA)**: Put your emergency fund where it actually earns interest. Don't let your money sleep! 😴💰
        """
    }
}

# --- AI Problem Solver Logic ---
def get_local_ai_advice(problem):
    # Prepare documents for TF-IDF
    categories = list(KNOWLEDGE_BASE.keys())
    all_problems = []
    for cat in categories:
        all_problems.extend(KNOWLEDGE_BASE[cat]["problems"])
    
    # Add user problem to the list
    all_docs = all_problems + [problem]
    
    # Vectorize
    vectorizer = TfidfVectorizer().fit_transform(all_docs)
    vectors = vectorizer.toarray()
    
    # Calculate similarity between user problem (last vector) and all others
    user_vec = vectors[-1].reshape(1, -1)
    kb_vecs = vectors[:-1]
    
    similarities = cosine_similarity(user_vec, kb_vecs)[0]
    best_match_idx = similarities.argsort()[-1]
    max_similarity = similarities[best_match_idx]
    
    # If similarity is too low, return default
    if max_similarity < 0.2:
        return "That's giving 'villain origin story' 🖤", "**Real Talk Bestie:** Start by tracking all your expenses for a month to see where the tea is spilling! 💅"
    
    # Find which category the best match belongs to
    current_idx = 0
    for cat in categories:
        num_problems = len(KNOWLEDGE_BASE[cat]["problems"])
        if best_match_idx < current_idx + num_problems:
            return KNOWLEDGE_BASE[cat]["response"], KNOWLEDGE_BASE[cat]["advice"]
        current_idx += num_problems
    
    return "That's giving 'main character era' ✨", "Keep doing you, bestie! 💅"

def get_ai_advice(problem):
    # Try Gemini first if API key exists
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"""
            You are a financial advisor for GenZ. You give practical, expert advice but use GenZ slang (like 'bestie', 'no cap', 'slay', 'tea', 'bag', 'main character energy'). 
            The user has the following financial problem: '{problem}'
            Provide your response in two parts:
            1. A 'GenZ Response': A short, witty, and relatable comment about their situation.
            2. 'Financial Advice': 2-3 bullet points of solid, practical financial advice.
            Format the response clearly.
            """
            response = model.generate_content(prompt)
            parts = response.text.split("Financial Advice")
            genz_res = parts[0].replace("GenZ Response:", "").strip()
            advice_res = parts[1].strip() if len(parts) > 1 else "No advice generated, bestie. 😭"
            return genz_res, advice_res
        except:
            pass
    
    # Fallback to Local "AI" matching engine
    return get_local_ai_advice(problem)

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

def problem_solver():
    if not st.session_state.logged_in:
        st.error("Bestie, login first! 🫖")
        return
    init_problem_solver_db()
    st.title(" Financial Problem Solver")
    st.markdown("### Spill your financial tea and get that GenZ advice you didn't know you needed ✨")

    # API Key Input for AI (Optional)
    with st.expander("✨ Want even more personalized advice? (Optional)"):
        st.info("The app uses a built-in AI model by default. To unlock the 'Premium' Gemini AI, add your API key here! 💅")
        user_api_key = st.text_input("Enter your Google Gemini API Key", type="password", help="Get your key at aistudio.google.com")
        if user_api_key:
            os.environ["GOOGLE_API_KEY"] = user_api_key
            st.success("Premium AI unlocked! Slay! 🚀")

    # Problem submission form
    with st.form("problem_form"):
        st.subheader("What's the financial tea? ☕")
        problem = st.text_area("Drop your financial problem here! 💸", placeholder="Example: I can't stop spending money on coffee and my budget is crying 😭")
        
        submitted = st.form_submit_button("Get That Tea 🚀")
        
        if submitted and problem:
            save_problem(st.session_state.username, problem)
            st.success("Your tea has been spilled! Let's get you that advice bestie! 🫖")
            st.rerun()
    
    st.markdown("---")
    st.subheader("Recent Financial Tea ☕")
    
    problems = get_problems()
    
    if not problems:
        st.info("No financial tea spilled yet! Be the first to share your financial drama bestie! 🫖")
    else:
        for p_id, user, p_text, created_at in problems:
            with st.expander(f"Tea from {user} - {created_at}", expanded=False):
                st.markdown(f"**Problem:** {p_text}")
                
                # Get Advice (will automatically use Gemini if key is present, otherwise local AI)
                res, adv = get_ai_advice(p_text)
                
                st.markdown("### 💅 Vibe Check")
                st.markdown(f"**GenZ Response:** {res}")
                st.markdown("---")
                st.markdown("### 💰 Financial Advice 💰")
                st.markdown(adv)
                
                st.markdown("### ✨ 🔥 💸 🫖")

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
