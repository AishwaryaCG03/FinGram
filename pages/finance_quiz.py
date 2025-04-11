import streamlit as st
import random
import json
from datetime import datetime
import sqlite3
import pandas as pd

def init_quiz_db():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    # Create quiz scores table
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_scores
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  score INTEGER,
                  total_questions INTEGER,
                  category TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY (username) REFERENCES users(username))''')
    
    conn.commit()
    conn.close()

def save_score(username, score, total_questions, category):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO quiz_scores (username, score, total_questions, category, created_at)
                 VALUES (?, ?, ?, ?, ?)''', 
              (username, score, total_questions, category, datetime.now()))
    
    conn.commit()
    conn.close()

def get_top_scores():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    scores = c.execute('''SELECT username, score, total_questions, category, created_at 
                         FROM quiz_scores 
                         ORDER BY score DESC, created_at DESC 
                         LIMIT 5''').fetchall()
    
    conn.close()
    return scores

# Quiz questions by category
quiz_questions = {
    "Budgeting": [
        {
            "question": "What's giving 'main character energy' in a 50/30/20 budget rule?",
            "options": [
                "50% needs, 30% wants, 20% savings",
                "50% wants, 30% savings, 20% needs",
                "50% savings, 30% needs, 20% wants",
                "50% vibes, 30% aesthetic, 20% reality"
            ],
            "correct": 0,
            "explanation": "The 50/30/20 rule is the moment! 50% for needs (rent, food), 30% for wants (that aesthetic coffee), and 20% for savings (future you will slay!) "
        },
        {
            "question": "Your bestie asks about an emergency fund. How many months of expenses should it cover?",
            "options": [
                "1 month (giving bare minimum energy)",
                "3-6 months (it's giving responsible queen)",
                "12 months (main character behavior)",
                "0 months (living on the edge bestie)"
            ],
            "correct": 1,
            "explanation": "3-6 months is giving responsible queen energy! It's enough to cover your hot girl walks even when life throws shade 💁‍♀️"
        },
        {
            "question": "Which budgeting app is giving 'red flag' energy?",
            "options": [
                "One that tracks your spending automatically (we love organization)",
                "One that doesn't have a password (security who?)",
                "One that sends spending alerts (accountability check)",
                "One that syncs with your bank (convenience queen)"
            ],
            "correct": 1,
            "explanation": "No password? That's giving major security risk energy! Protect your bag like you protect your heart bestie! 🔒"
        },
        {
            "question": "What's the tea on zero-based budgeting?",
            "options": [
                "When you spend zero money (not the vibe)",
                "When every rupee has a job (werk bestie)",
                "When you have zero savings (broke energy)",
                "When you only use credit cards (debt era)"
            ],
            "correct": 1,
            "explanation": "Zero-based budgeting is when every rupee has a purpose - like how every outfit needs a purpose! Make that money work bestie! "
        },
        {
            "question": "Which expense tracking method is giving 'organized queen' energy?",
            "options": [
                "Mental tracking (chaotic bestie)",
                "Daily expense journal (main character behavior)",
                "Asking parents for receipts (dependent era)",
                "Ignoring expenses (avoidance vibes)"
            ],
            "correct": 1,
            "explanation": "Daily expense journal is the organized queen we stan! Track those expenses like you track your ex's stories! 📱"
        },
        {
            "question": "What's the slay way to handle unexpected expenses?",
            "options": [
                "Ignore them (avoidance era)",
                "Use emergency fund (prepared queen)",
                "Borrow from friends (dependent vibes)",
                "Max out credit cards (toxic behavior)"
            ],
            "correct": 1,
            "explanation": "Using your emergency fund? That's why you're the main character! Being prepared is giving queen behavior! 👑"
        },
        {
            "question": "Which savings habit is giving 'growth mindset' energy?",
            "options": [
                "Save what's left after spending (pick me energy)",
                "Save first, spend later (boss behavior)",
                "Save only for shopping (material gworl)",
                "Save nothing (broke era)"
            ],
            "correct": 1,
            "explanation": "Save first, spend later is the ultimate boss move! It's giving 'I prioritize my future' energy! "
        },
        {
            "question": "What's the tea on budget categories?",
            "options": [
                "One category for everything (messy bestie)",
                "Detailed categories with subcategories (organized queen)",
                "No categories (chaotic energy)",
                "Just vibes (not the move)"
            ],
            "correct": 1,
            "explanation": "Detailed categories? That's giving Type A personality and we're here for it! Organization is the new aesthetic! ✨"
        },
        {
            "question": "How often should you review your budget for the glow up?",
            "options": [
                "Never (red flag energy)",
                "Monthly (consistent queen)",
                "Yearly (bare minimum)",
                "When things go wrong (crisis mode)"
            ],
            "correct": 1,
            "explanation": "Monthly reviews are giving consistent queen energy! Stay on top of your money like you stay on top of your skincare routine! "
        },
        {
            "question": "What's the moment in handling lifestyle inflation?",
            "options": [
                "Upgrade everything immediately (flex era)",
                "Keep expenses same, save the raise (smart queen)",
                "YOLO spending (chaotic bestie)",
                "Ask for more raises (greedy energy)"
            ],
            "correct": 1,
            "explanation": "Keeping expenses same and saving that raise? You're literally being a financial girlboss! Period! 💁‍♀️"
        }
    ],
    "Investing": [
        {
            "question": "Which investment is giving 'long-term relationship' vibes?",
            "options": [
                "Day trading (it's giving situationship)",
                "Index funds (committed and loyal bestie)",
                "Penny stocks (toxic ex behavior)",
                "Your friend's startup (bestie behavior but risky)"
            ],
            "correct": 1,
            "explanation": "Index funds are the committed relationship of investing - stable, reliable, and won't ghost you! 💍"
        },
        {
            "question": "What's the tea on compound interest?",
            "options": [
                "Interest on your initial investment only",
                "Interest on interest (it's giving exponential growth)",
                "A new cryptocurrency",
                "A type of bank fee (not the slay)"
            ],
            "correct": 1,
            "explanation": "Compound interest is interest on interest - it's giving exponential growth! Your money makes money which makes more money, period! "
        },
        {
            "question": "Which investment portfolio is serving 'main character energy'?",
            "options": [
                "100% in one stock (pick me energy)",
                "Diverse mix of assets (character development)",
                "All in crypto (chaotic bestie)",
                "Only in gold (old school vibes)"
            ],
            "correct": 1,
            "explanation": "Diversification is the ultimate character development! Don't put all your eggs in one basket bestie - that's giving pick me energy! 🥚"
        },
        {
            "question": "What's the slay way to handle market dips?",
            "options": [
                "Sell everything (panic isn't cute)",
                "Buy more if you can (buy the dip bestie)",
                "Ignore your portfolio (avoidance era)",
                "Post about it on social (drama queen)"
            ],
            "correct": 1,
            "explanation": "Buy the dip bestie! It's like getting your favorite fit on sale - a true girlboss move! "
        },
        {
            "question": "Which mutual fund is giving 'trustworthy bestie' vibes?",
            "options": [
                "High expense ratio funds (money grabber)",
                "Low-cost index funds (reliable queen)",
                "Random fund selection (chaotic energy)",
                "Whatever's trending (follower vibes)"
            ],
            "correct": 1,
            "explanation": "Low-cost index funds are the reliable besties of investing! They won't eat up your returns like a toxic friend! "
        },
        {
            "question": "What's the tea on SIP (Systematic Investment Plan)?",
            "options": [
                "Investing when you feel like it (moody)",
                "Regular, automated investing (consistent queen)",
                "One-time large investment (flex energy)",
                "Daily trading (chaotic bestie)"
            ],
            "correct": 1,
            "explanation": "Regular, automated investing through SIP? That's giving consistent queen energy! We love a planned glow up! ✨"
        },
        {
            "question": "How's the vibe check on your investment horizon?",
            "options": [
                "Next week (impatient energy)",
                "5+ years (long-term growth)",
                "Tomorrow (chaotic bestie)",
                "No plan (red flag)"
            ],
            "correct": 1,
            "explanation": "5+ years horizon is giving patient queen energy! Good things take time, just like your skincare routine! 💆‍♀️"
        },
        {
            "question": "What's the moment in risk assessment?",
            "options": [
                "YOLO everything (chaotic)",
                "Match risk to your goals (smart queen)",
                "Avoid all risks (scared energy)",
                "Copy friends (follower vibes)"
            ],
            "correct": 1,
            "explanation": "Matching risk to your goals? That's main character behavior! Know yourself like you know your coffee order! ☕"
        },
        {
            "question": "Which investment research is giving 'prepared queen' energy?",
            "options": [
                "Random social media tips (risky bestie)",
                "Multiple reliable sources (educated queen)",
                "Just vibes (chaotic energy)",
                "Hot tips from friends (gossip era)"
            ],
            "correct": 1,
            "explanation": "Using multiple reliable sources? You're literally being the valedictorian of investing! We stan an educated queen! 📚"
        },
        {
            "question": "What's the tea on rebalancing your portfolio?",
            "options": [
                "Never (avoidant vibes)",
                "Regular schedule (organized queen)",
                "When you're stressed (emotional)",
                "Daily changes (obsessed much?)"
            ],
            "correct": 1,
            "explanation": "Regular rebalancing schedule? That's giving organized queen energy! Keep your portfolio balanced like your chakras! ✨"
        }
    ],
    "Credit": [
        {
            "question": "What's giving 'green flag' energy in a credit score?",
            "options": [
                "300-579 (it's giving red flag)",
                "580-669 (mid bestie)",
                "670-739 (okay, we see you)",
                "740+ (main character behavior)"
            ],
            "correct": 3,
            "explanation": "740+ is main character behavior! It's giving 'I have my life together' energy and lenders are obsessed! ✨"
        },
        {
            "question": "Which is NOT the tea for building good credit?",
            "options": [
                "Paying bills on time (responsible queen behavior)",
                "Maxing out credit cards (toxic ex behavior)",
                "Keeping utilization low (we love boundaries)",
                "Having a credit mix (variety is the moment)"
            ],
            "correct": 1,
            "explanation": "Maxing out credit cards is giving toxic ex vibes! Keep that utilization low (under 30%) for the glow up! "
        },
        {
            "question": "What's the tea on credit card grace periods?",
            "options": [
                "Time to find a new card (not this)",
                "Extra time to pay without interest (we love free)",
                "When your credit limit increases (flex era)",
                "Minimum payment due date (basic)"
            ],
            "correct": 1,
            "explanation": "Grace period is that bestie who gives you extra time to pay without charging interest - we love a supportive queen! 👑"
        },
        {
            "question": "How often should you check your credit report for the glow up?",
            "options": [
                "Never (giving avoidant vibes)",
                "Once a year (bare minimum energy)",
                "Every few months (healthy boundaries)",
                "Every day (obsessed much?)"
            ],
            "correct": 2,
            "explanation": "Checking every few months is giving healthy relationship energy with your finances! Stay aware but not obsessed bestie! "
        },
        {
            "question": "What's the slay way to handle credit card rewards?",
            "options": [
                "Ignore them (wasteful energy)",
                "Strategic spending for points (smart queen)",
                "Overspend for points (toxic behavior)",
                "Random usage (chaotic bestie)"
            ],
            "correct": 1,
            "explanation": "Strategic spending for points? That's giving calculated queen energy! Make those rewards work for you! "
        },
        {
            "question": "Which credit limit behavior is giving 'responsible' vibes?",
            "options": [
                "Always maxed out (red flag)",
                "Under 30% usage (queen behavior)",
                "50% regular use (mid energy)",
                "100% sometimes (chaotic)"
            ],
            "correct": 1,
            "explanation": "Keeping it under 30%? That's the kind of boundary setting we love to see! Main character behavior! 👑"
        },
        {
            "question": "What's the moment in handling multiple credit cards?",
            "options": [
                "Random usage (messy energy)",
                "Organized system (strategic queen)",
                "Ignore some cards (avoidant)",
                "Max out all (toxic era)"
            ],
            "correct": 1,
            "explanation": "Having an organized system? You're giving Type A personality and we're living for it! "
        },
        {
            "question": "How to serve 'authorized user' realness?",
            "options": [
                "Add everyone (chaotic)",
                "Carefully select trusted people (wise queen)",
                "Never add anyone (trust issues)",
                "Random friends (risky bestie)"
            ],
            "correct": 1,
            "explanation": "Carefully selecting authorized users? That's giving boundaries queen energy! Choose your credit circle like your inner circle! 💫"
        },
        {
            "question": "What's the tea on credit card annual fees?",
            "options": [
                "Pay all fees (wasteful)",
                "Compare benefits vs cost (math queen)",
                "Avoid all fees (limiting)",
                "Ignore fees (avoidant)"
            ],
            "correct": 1,
            "explanation": "Comparing benefits vs costs? You're literally doing cost-benefit analysis! We stan a calculated queen! 📊"
        },
        {
            "question": "Which credit dispute behavior is main character energy?",
            "options": [
                "Ignore errors (avoidant)",
                "Document and dispute promptly (boss move)",
                "Dispute everything (drama queen)",
                "Ask friends to handle it (dependent)"
            ],
            "correct": 1,
            "explanation": "Documenting and disputing promptly? That's giving 'I know my worth' energy! Stand up for your credit like you stand up for yourself! "
        }
    ],
    "Taxes": [
        {
            "question": "What's the tea on tax deductions?",
            "options": [
                "Extra taxes you pay (not the vibe)",
                "Money subtracted from taxable income (we love savings)",
                "A type of cryptocurrency",
                "A new budgeting app"
            ],
            "correct": 1,
            "explanation": "Tax deductions reduce your taxable income - it's giving money-saving queen energy! The government said 'take this discount bestie' "
        },
        {
            "question": "When's the main character deadline for filing taxes in India?",
            "options": [
                "July 31st (unless you're giving extension vibes)",
                "December 31st (new year new you)",
                "April 15th (that's USA bestie)",
                "Whenever you feel like it (chaotic energy)"
            ],
            "correct": 0,
            "explanation": "July 31st is the moment for filing taxes in India! Unless you're giving extension vibes, then it's different bestie! 📅"
        },
        {
            "question": "What's the slay way to keep tax records?",
            "options": [
                "Screenshot everything (chaotic bestie)",
                "Organized digital folders (main character behavior)",
                "Just wing it (not the serve)",
                "Ask your parents (dependent era)"
            ],
            "correct": 1,
            "explanation": "Organized digital folders are giving 'I have my life together' energy! Keep those receipts like you keep the tea! 📂"
        },
        {
            "question": "Which tax saving investment is giving responsible queen vibes in India?",
            "options": [
                "PPF (Public Provident Fund, we love stability)",
                "Betting on cricket (not the move bestie)",
                "Keeping cash under mattress (old school energy)",
                "Lending to friends (risky bestie)"
            ],
            "correct": 0,
            "explanation": "PPF is the stable queen of tax-saving investments! It's giving long-term commitment with government backing - we love security! "
        },
        {
            "question": "What's the moment in Form 16?",
            "options": [
                "Ignore it (avoidant energy)",
                "Keep it safe for tax filing (organized queen)",
                "Share it on social (oversharing era)",
                "Give it to random people (unsafe bestie)"
            ],
            "correct": 1,
            "explanation": "Keeping Form 16 safe? That's giving responsible adult energy! Treat it like your favorite designer bag! 👜"
        },
        {
            "question": "How's the vibe check on advance tax?",
            "options": [
                "Pay when reminded (procrastinator energy)",
                "Calculate and pay on time (prepared queen)",
                "Ignore it completely (avoidant era)",
                "Pay random amounts (chaotic bestie)"
            ],
            "correct": 1,
            "explanation": "Calculating and paying advance tax on time? You're literally being the valedictorian of taxes! We stan a prepared queen! 📚"
        },
        {
            "question": "What's the tea on tax regime choice?",
            "options": [
                "Random selection (chaotic)",
                "Calculate benefits of both (math queen)",
                "Ask friends (follower vibes)",
                "Stick to old always (resistant energy)"
            ],
            "correct": 1,
            "explanation": "Calculating benefits of both regimes? That's giving financial analyst energy! Make that informed choice bestie! 🧮"
        },
        {
            "question": "Which tax-saving section is serving main character energy?",
            "options": [
                "Section 80C (versatile queen)",
                "No sections (avoidant vibes)",
                "Random sections (confused era)",
                "Whatever friends use (copycat energy)"
            ],
            "correct": 0,
            "explanation": "Section 80C is the versatile queen of tax savings! It's giving options and we love choices! "
        },
        {
            "question": "What's the slay way to handle tax refunds?",
            "options": [
                "Forget about them (wasteful)",
                "Track and follow up (vigilant queen)",
                "Ask friends to check (dependent)",
                "Ignore notifications (avoidant)"
            ],
            "correct": 1,
            "explanation": "Tracking and following up on refunds? That's giving 'my money matters' energy! Chase that bag bestie! 💰"
        },
        {
            "question": "How to serve income source disclosure realness?",
            "options": [
                "Hide some income (shady vibes)",
                "Declare everything properly (honest queen)",
                "Random declarations (messy energy)",
                "Copy others (follower era)"
            ],
            "correct": 1,
            "explanation": "Declaring all income properly? You're giving transparent queen energy! Honesty is always the best policy bestie! ✨"
        }
    ],
    "Digital Money": [
        {
            "question": "What's the tea on UPI safety?",
            "options": [
                "Share your PIN with besties (not the move)",
                "Never share PIN and use biometric (secure queen)",
                "Write PIN on phone case (convenience era)",
                "Use same PIN everywhere (lazy vibes)"
            ],
            "correct": 1,
            "explanation": "Never sharing your UPI PIN and using biometric is giving secure queen energy! Protect your bag at all costs! "
        },
        {
            "question": "Which digital payment habit is serving red flags?",
            "options": [
                "Checking transaction status (vigilant queen)",
                "Using public WiFi for banking (risk taker era)",
                "Having strong passwords (security first)",
                "Regular app updates (tech savvy bestie)"
            ],
            "correct": 1,
            "explanation": "Using public WiFi for banking? That's giving 'I love drama' energy! Secure network only bestie! 🚫"
        },
        {
            "question": "What's the moment in digital wallet limits?",
            "options": [
                "No limits (chaotic energy)",
                "Set according to your needs (responsible queen)",
                "Maximum possible (flex era)",
                "Whatever's trending (follower vibes)"
            ],
            "correct": 1,
            "explanation": "Setting limits according to your needs is the responsible queen behavior we stan! Know your budget, set your boundaries! "
        },
        {
            "question": "How to serve authentication realness?",
            "options": [
                "Single factor (basic energy)",
                "Two-factor (secure queen vibes)",
                "No authentication (chaotic bestie)",
                "Share with friends (trust issues)"
            ],
            "correct": 1,
            "explanation": "Two-factor authentication is giving extra security queen energy! Like having a bouncer and a guest list - period! "
        },
        {
            "question": "What's the slay way to handle payment apps?",
            "options": [
                "Install all apps (cluttered phone era)",
                "Select few trusted apps (curated queen)",
                "Random app selection (chaotic)",
                "Use whatever's trending (follower vibes)"
            ],
            "correct": 1,
            "explanation": "Using selected trusted apps? That's giving exclusive list energy! Quality over quantity bestie! ✨"
        },
        {
            "question": "How's the vibe check on digital payment receipts?",
            "options": [
                "Screenshot randomly (messy energy)",
                "Organize in folders (system queen)",
                "Delete immediately (risky bestie)",
                "Never check (avoidant era)"
            ],
            "correct": 1,
            "explanation": "Organizing receipts in folders? You're giving Type A personality and we're here for it! Stay organized bestie! 📱"
        },
        {
            "question": "What's the tea on mobile banking security?",
            "options": [
                "Use simple passwords (basic)",
                "Complex password + biometric (secure queen)",
                "Same password everywhere (lazy era)",
                "No password (chaotic energy)"
            ],
            "correct": 1,
            "explanation": "Complex password and biometric? That's giving Fort Knox energy! Protect your coins like your skincare routine! 🔒"
        },
        {
            "question": "Which online shopping habit is main character energy?",
            "options": [
                "Save card everywhere (risky)",
                "Use secure payment methods (smart queen)",
                "Share card details (unsafe bestie)",
                "Random payment choices (chaotic)"
            ],
            "correct": 1,
            "explanation": "Using secure payment methods? You're literally being the responsible queen of online shopping! Period! 🛍️"
        },
        {
            "question": "How to serve digital transaction monitoring?",
            "options": [
                "Check once a year (bare minimum)",
                "Regular monitoring (vigilant queen)",
                "Never check (avoidant vibes)",
                "Ask others to check (dependent era)"
            ],
            "correct": 1,
            "explanation": "Regular transaction monitoring? That's giving 'I'm on top of my game' energy! Stay alert bestie! 👀"
        },
        {
            "question": "What's the moment in digital payment disputes?",
            "options": [
                "Ignore issues (avoidant)",
                "Report immediately (proactive queen)",
                "Complain on social (drama era)",
                "Wait it out (passive energy)"
            ],
            "correct": 1,
            "explanation": "Reporting issues immediately? You're giving problem-solver queen energy! Don't let anyone mess with your coins! "
        }
    ]
}

def finance_quiz():
    if not st.session_state.logged_in:
        st.error("Bestie, you need to login first to serve this knowledge! 🫖")
        return
    
    # Initialize quiz state if not exists
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'questions_answered' not in st.session_state:
        st.session_state.questions_answered = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    
    # Initialize database
    init_quiz_db()
    
    st.title(" Financial Knowledge Check")
    st.markdown("### Spill the tea on your money knowledge bestie! ✨")
    
    # Category selection
    if not st.session_state.selected_category:
        st.markdown("### Choose your category bestie! 💁‍♀️")
        categories = list(quiz_questions.keys())
        cols = st.columns(len(categories))
        
        for i, category in enumerate(categories):
            with cols[i]:
                if st.button(f"{category} ", key=f"cat_{category}"):
                    st.session_state.selected_category = category
                    st.session_state.quiz_score = 0
                    st.session_state.questions_answered = 0
                    st.session_state.quiz_complete = False
                    st.rerun()
    
    # Quiz section
    if st.session_state.selected_category and not st.session_state.quiz_complete:
        category = st.session_state.selected_category
        questions = quiz_questions[category]
        
        if st.session_state.questions_answered < len(questions):
            question_data = questions[st.session_state.questions_answered]
            
            st.markdown(f"### Question {st.session_state.questions_answered + 1} of {len(questions)}")
            st.markdown(f"**{question_data['question']}**")
            
            # Create columns for options
            option_cols = st.columns(2)
            selected_option = None
            
            for i, option in enumerate(question_data['options']):
                col_idx = i % 2
                with option_cols[col_idx]:
                    if st.button(option, key=f"opt_{i}"):
                        selected_option = i
            
            if selected_option is not None:
                if selected_option == question_data['correct']:
                    st.success("Yasss queen! You slayed that answer! ✨")
                    st.session_state.quiz_score += 1
                else:
                    st.error("Not the serve bestie, but we move! 💁‍♀️")
                
                st.info(question_data['explanation'])
                st.session_state.questions_answered += 1
                
                if st.session_state.questions_answered < len(questions):
                    if st.button("Next Question Bestie! "):
                        st.rerun()
                else:
                    st.session_state.quiz_complete = True
                    save_score(st.session_state.username, 
                             st.session_state.quiz_score, 
                             len(questions), 
                             st.session_state.selected_category)
                    st.rerun()
    
    # Quiz complete section
    if st.session_state.quiz_complete:
        st.markdown("---")
        st.markdown("### The Final Tea ☕")
        
        score_percentage = (st.session_state.quiz_score / len(quiz_questions[st.session_state.selected_category])) * 100
        
        if score_percentage == 100:
            st.success("PERIOD! You ate and left no crumbs! ✨")
        elif score_percentage >= 75:
            st.success("You're giving financial guru energy bestie! 💁‍♀️")
        elif score_percentage >= 50:
            st.info("It's giving potential! A few more study sessions and you'll slay! ✨")
        else:
            st.warning("Bestie, we need to work on this! But no shade, we all start somewhere! ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Your Score",
                value=f"{st.session_state.quiz_score}/{len(quiz_questions[st.session_state.selected_category])}",
                delta=f"{score_percentage:.0f}% Slayage"
            )
        
        with col2:
            st.markdown("### Want to try another category? ")
            if st.button("New Category Bestie! ✨"):
                st.session_state.selected_category = None
                st.session_state.quiz_score = 0
                st.session_state.questions_answered = 0
                st.session_state.quiz_complete = False
                st.rerun()
        
        # Show leaderboard
        st.markdown("---")
        st.markdown("### Financial Girlboss Leaderboard 👑")
        
        top_scores = get_top_scores()
        if top_scores:
            score_df = pd.DataFrame(
                top_scores,
                columns=["Bestie", "Score", "Total Questions", "Category", "Date"]
            )
            st.dataframe(score_df, use_container_width=True)
        else:
            st.info("No scores yet bestie! Be the first to slay! ")

if __name__ == "__main__":
    finance_quiz() 