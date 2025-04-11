import streamlit as st
import random
import sqlite3
from datetime import datetime

def init_problem_solver_db():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    # Create problems table
    c.execute('''CREATE TABLE IF NOT EXISTS financial_problems
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  problem TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY (username) REFERENCES users(username))''')
    
    # Create responses table
    c.execute('''CREATE TABLE IF NOT EXISTS problem_responses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  problem_id INTEGER,
                  response TEXT,
                  advice TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY (problem_id) REFERENCES financial_problems(id))''')
    
    conn.commit()
    conn.close()

def save_problem(username, problem):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO financial_problems (username, problem, created_at)
                 VALUES (?, ?, ?)''', (username, problem, datetime.now()))
    
    problem_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return problem_id

def get_problems():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    problems = c.execute('''SELECT id, username, problem, created_at 
                           FROM financial_problems 
                           ORDER BY created_at DESC''').fetchall()
    
    conn.close()
    return problems

def get_responses(problem_id):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    responses = c.execute('''SELECT response, advice, created_at 
                            FROM problem_responses 
                            WHERE problem_id = ? 
                            ORDER BY created_at DESC''', (problem_id,)).fetchall()
    
    conn.close()
    return responses

def generate_meme_response(problem):
    # Dictionary of GenZ slang responses based on problem keywords
    responses = {
        "budget": [
            "Bestie, your budget is giving 'I don't know her' vibes ",
            "That budget is more broken than my ex's promises 😭",
            "Your budget is giving 'I'm in my broke era' and I'm here for it ✨",
            "Budget? More like bud-get out of here with those expenses 💸",
            "Your budget is giving 'I'm in my villain era' and I'm living for it 🖤"
        ],
        "savings": [
            "Your savings account is giving 'I'm in my ghosting era' because it's empty 👻",
            "Savings? More like 'saving for another day' because today is not that day ",
            "Your savings are giving 'I'm in my main character era' because they're the star of your financial story ✨",
            "Savings account? More like 'savings account who?' because it's giving amnesia vibes 🧠",
            "Your savings are giving 'I'm in my independent era' because they're doing their own thing 💁‍♀️"
        ],
        "debt": [
            "That debt is giving 'I'm in my toxic era' and I'm not here for it 😤",
            "Debt? More like 'debt-ached to my life' because it's not going anywhere 💀",
            "Your debt is giving 'I'm in my villain origin story' and I'm living for it 🖤",
            "Debt is giving 'I'm in my main character era' because it's the star of your financial story 💅",
            "That debt is giving 'I'm in my chaotic era' and I'm not here for it 😭"
        ],
        "invest": [
            "Investing? More like 'in-vesting my money in things I don't understand' 🤡",
            "Your investment strategy is giving 'I'm in my delulu era' and I'm here for it ✨",
            "Investing is giving 'I'm in my main character era' because you're the star of your financial story 💅",
            "That investment is giving 'I'm in my villain era' and I'm living for it 🖤",
            "Investing? More like 'in-vesting my money in things that make me happy' because that's what matters 💁‍♀️"
        ],
        "money": [
            "Money? More like 'money who?' because it's giving amnesia vibes 🧠",
            "Your money situation is giving 'I'm in my broke era' and I'm here for it ✨",
            "Money is giving 'I'm in my main character era' because you're the star of your financial story 💅",
            "That money situation is giving 'I'm in my villain era' and I'm living for it 🖤",
            "Money? More like 'money who?' because it's giving ghosting vibes 👻"
        ],
        "default": [
            "That's giving 'I'm in my main character era' and I'm here for it ✨",
            "Your financial situation is giving 'I'm in my villain origin story' and I'm living for it 🖤",
            "That's giving 'I'm in my chaotic era' and I'm not here for it 😭",
            "Your money moves are giving 'I'm in my independent era' because they're doing their own thing 💁‍♀️",
            "That's giving 'I'm in my delulu era' and I'm here for it ✨"
        ]
    }
    
    # Dictionary of financial advice based on problem keywords
    advice = {
        "budget": [
            "**Real Talk Bestie:** Try the 50/30/20 rule - 50% for needs, 30% for wants, 20% for savings. It's giving responsible vibes! 💅",
            "**Financial Tea:** Track your spending with a budgeting app. It's like having a bestie who keeps you accountable! ✨",
            "**Money Moves:** Set up automatic transfers to your savings account on payday. Out of sight, out of mind! 💸",
            "**Pro Tip:** Use cash-back apps for your regular purchases. Free money is always the aesthetic! 🤑",
            "**Bestie Advice:** Create a 'no-spend' day once a week. Your wallet will thank you! 💅"
        ],
        "savings": [
            "**Real Talk Bestie:** Start with a small emergency fund of $500, then build to 3-6 months of expenses. It's giving security! 💅",
            "**Financial Tea:** Use the 'pay yourself first' method - transfer money to savings before paying bills. It's giving priority! ✨",
            "**Money Moves:** Open a high-yield savings account. Your money should work harder than your ex! 💸",
            "**Pro Tip:** Set up automatic savings transfers. It's like having a financial bestie who's always looking out for you! 🤑",
            "**Bestie Advice:** Try the 52-week savings challenge - save $1 the first week, $2 the second, and so on. By year-end, you'll have $1,378! 💅"
        ],
        "debt": [
            "**Real Talk Bestie:** Try the debt snowball method - pay off your smallest debt first, then roll that payment into the next. It's giving momentum! 💅",
            "**Financial Tea:** Consider a balance transfer card with 0% APR for a year to tackle high-interest debt. It's giving strategy! ✨",
            "**Money Moves:** Cut unnecessary subscriptions and put that money toward debt. Netflix can wait! 💸",
            "**Pro Tip:** Use the debt avalanche method - pay off highest interest debt first. It's giving efficiency! 🤑",
            "**Bestie Advice:** Create a debt payoff calendar to visualize your progress. It's giving motivation! 💅"
        ],
        "invest": [
            "**Real Talk Bestie:** Start with index funds or ETFs - they're giving diversification without the stress! 💅",
            "**Financial Tea:** Open a Roth IRA if you have earned income. Your future self will thank you! ✨",
            "**Money Moves:** Use dollar-cost averaging - invest the same amount regularly regardless of market conditions. It's giving consistency! 💸",
            "**Pro Tip:** Consider a robo-advisor if you're new to investing. It's like having a financial bestie who's always available! 🤑",
            "**Bestie Advice:** Start small with micro-investing apps that let you invest spare change. Every penny counts! 💅"
        ],
        "money": [
            "**Real Talk Bestie:** Create multiple savings accounts for different goals - emergency fund, vacation, new phone. It's giving organization! 💅",
            "**Financial Tea:** Use the envelope method - allocate cash to different categories and only spend what's in each envelope. It's giving control! ✨",
            "**Money Moves:** Look for side hustles that match your skills - freelancing, tutoring, or content creation. Extra money is always the aesthetic! 💸",
            "**Pro Tip:** Negotiate your bills - call providers and ask for better rates. Your wallet deserves the best! 🤑",
            "**Bestie Advice:** Practice the 24-hour rule - wait a day before making non-essential purchases. It's giving mindfulness! 💅"
        ],
        "default": [
            "**Real Talk Bestie:** Start by tracking all your expenses for a month to see where your money is going. Knowledge is power! 💅",
            "**Financial Tea:** Set specific, measurable financial goals with deadlines. It's giving direction! ✨",
            "**Money Moves:** Automate your finances - bill payments, savings transfers, and investments. It's giving consistency! 💸",
            "**Pro Tip:** Use cash-back credit cards responsibly and pay off the balance monthly. Free money is always the aesthetic! 🤑",
            "**Bestie Advice:** Create a vision board for your financial goals. It's giving manifestation! 💅"
        ]
    }
    
    # Check for keywords in the problem
    problem_lower = problem.lower()
    
    if "budget" in problem_lower:
        return random.choice(responses["budget"]), random.choice(advice["budget"])
    elif "sav" in problem_lower:
        return random.choice(responses["savings"]), random.choice(advice["savings"])
    elif "debt" in problem_lower:
        return random.choice(responses["debt"]), random.choice(advice["debt"])
    elif "invest" in problem_lower:
        return random.choice(responses["invest"]), random.choice(advice["invest"])
    elif "money" in problem_lower or "cash" in problem_lower or "dollar" in problem_lower:
        return random.choice(responses["money"]), random.choice(advice["money"])
    else:
        return random.choice(responses["default"]), random.choice(advice["default"])

def problem_solver():
    if not st.session_state.logged_in:
        st.error("Bestie, you need to login first to see the tea! 🫖")
        return
    
    # Initialize database
    init_problem_solver_db()
    
    st.title(" Financial Problem Solver")
    st.markdown("### Spill your financial tea and get that GenZ advice you didn't know you needed")
    
    # Problem submission form
    with st.form("problem_form"):
        st.subheader("What's the financial tea? ☕")
        problem = st.text_area("Drop your financial problem here bestie (no judgment, we've all been there) 💸", 
                              placeholder="Example: I can't stop spending money on coffee and my budget is crying")
        
        submitted = st.form_submit_button("Get That Tea 🚀")
        
        if submitted and problem:
            problem_id = save_problem(st.session_state.username, problem)
            st.success("Your tea has been spilled! Let's get you that advice bestie! ")
            st.rerun()
    
    # Display problems and responses
    st.markdown("---")
    st.subheader("Recent Financial Tea ☕")
    
    problems = get_problems()
    
    if not problems:
        st.info("No financial tea spilled yet! Be the first to share your financial drama bestie! ")
    else:
        for problem_id, username, problem_text, created_at in problems:
            with st.expander(f"Tea from {username} - {created_at}", expanded=False):
                st.markdown(f"**Problem:** {problem_text}")
                
                # Generate and display response
                response, advice = generate_meme_response(problem_text)
                st.markdown(f"**GenZ Response:** {response}")
                
                # Display financial advice
                st.markdown("---")
                st.markdown("### 💰 Financial Advice 💰")
                st.markdown(advice)
                
                # Add some emojis for extra flair
                st.markdown("### ✨ 🔥 💸 🫖")
                
                # Add a button to generate a new response
                if st.button("Get Another Response Bestie", key=f"new_response_{problem_id}"):
                    new_response, new_advice = generate_meme_response(problem_text)
                    st.markdown(f"**New GenZ Response:** {new_response}")
                    st.markdown("---")
                    st.markdown("### 💰 New Financial Advice 💰")
                    st.markdown(new_advice)
                    st.markdown("### ✨ 🔥 💸 🫖")

if __name__ == "__main__":
    problem_solver() 