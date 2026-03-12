import streamlit as st
import random
import json
from datetime import datetime
import sqlite3
import pandas as pd
import plotly.express as px
from auth import save_engagement, get_engagement_counts, get_comments
import urllib.parse
import yfinance as yf
import time
import os

# Set yfinance cache to a local writable directory to avoid 'unable to open database file' errors
# Create a .cache directory if it doesn't exist
cache_dir = os.path.join(os.getcwd(), ".cache")
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
yf.set_tz_cache_location(cache_dir)

# --- Meme Gallery Section ---
def get_social_share_links(caption, hashtags=None):
    if hashtags is None: hashtags = ["FinTok", "MoneyMoves", "SecureTheBag", "FinanceCheck"]
    encoded_caption = urllib.parse.quote(caption)
    encoded_hashtags = urllib.parse.quote(" ".join(f"#{tag}" for tag in hashtags))
    return {
        "WhatsApp": f"https://api.whatsapp.com/send?text={encoded_caption}%20{encoded_hashtags}",
        "Twitter": f"https://twitter.com/intent/tweet?text={encoded_caption}&hashtags={','.join(hashtags)}",
        "LinkedIn": f"https://www.linkedin.com/sharing/share-offsite/?url=https://fingram.com&title={encoded_caption}",
        "Instagram": "instagram://story-camera"
    }

def meme_gallery():
    if not st.session_state.logged_in:
        st.error("Log in first! 🫖")
        return
    
    st.title("� The FinTok Feed")
    st.markdown("### Scroll for the financial facts! ☕🔥")

    # --- Upload Your Own Meme ---
    with st.expander("📤 Post Your Own Meme (Legend Status)", expanded=False):
        uploaded_file = st.file_uploader("Upload your meme (image/gif) 🖼️", type=["png", "jpg", "jpeg", "gif"])
        meme_caption = st.text_input("Caption your masterpiece... ✍️", placeholder="e.g. Me watching my portfolio dip but staying delulu ✨")
        meme_cat = st.selectbox("Category", ["Savings", "Investing", "Budgeting", "Crypto", "Taxes 📝"])
        
        if st.button("Post to Feed 🚀"):
            if uploaded_file and meme_caption:
                # Save file locally
                upload_dir = os.path.join(os.getcwd(), "uploads")
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                file_path = os.path.join(upload_dir, f"{st.session_state.username}_{int(time.time())}_{uploaded_file.name}")
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Save to DB
                conn = sqlite3.connect('genz_finance.db')
                c = conn.cursor()
                c.execute('''INSERT INTO user_memes (username, category, caption, image_path, created_at)
                             VALUES (?, ?, ?, ?, ?)''', (st.session_state.username, meme_cat, meme_caption, file_path, datetime.now()))
                conn.commit()
                conn.close()
                
                st.success("Legendary! Your meme is live! 🚀")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("We need both a meme and a caption! 🧐")

    # Spotlight Section: Meme of the Day
    st.markdown("---")
    st.markdown("## � Meme of the Day �")
    spotlight_meme = {
        "category": "Savings",
        "index": 2,
        "caption": "That moment when your emergency fund is looking thicker than your monthly bills 💰",
        "tag": "Iconic Behavior"
    }
    
    with st.container():
        st.markdown(
            f"""
            <div style="background-color: #1e1e1e; padding: 20px; border-radius: 15px; border: 2px solid #BC13FE; text-align: center; margin-bottom: 20px;">
                <h2 style="color: #BC13FE; margin-bottom: 10px;">{spotlight_meme['tag']} ✨</h2>
                <p style="font-size: 24px; font-weight: bold; color: white;">"{spotlight_meme['caption']}"</p>
                <div style="height: 200px; background: linear-gradient(45deg, #BC13FE, #39FF14); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 50px;">🤑💰💸</span>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        # Engagement for spotlight
        likes, comments_count, _ = get_engagement_counts(spotlight_meme['category'], spotlight_meme['index'])
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button(f"❤️ {likes}", key="spotlight_like"):
                save_engagement(st.session_state.username, spotlight_meme['category'], spotlight_meme['index'], "like")
                st.rerun()
        with col2:
            if st.button(f"💬 {comments_count}", key="spotlight_comment"):
                st.session_state["show_spotlight_comments"] = not st.session_state.get("show_spotlight_comments", False)
        
        if st.session_state.get("show_spotlight_comments", False):
            with st.expander("💭 Spotlight Talk", expanded=True):
                for user, text in get_comments(spotlight_meme['category'], spotlight_meme['index']):
                    st.markdown(f"**{user}**: {text}")

    st.markdown("---")
    
    # Filter by category
    meme_categories = {
        "Savings": ["Me looking at my bank account after saying 'treat yourself' 👀", "My savings account watching me buy another iced coffee ☕", "That moment when your emergency fund is looking thicker than your monthly bills 💰"],
        "Investing": ["Stock market be like: 📈📉 and I be like: 🙃", "Me pretending to understand crypto while buying the dip 🤡", "When someone says they're investing in their 401k: 'It's giving responsible' ✨"],
        "Budgeting": ["My budget: exists\nMe: I pretend I do not see it 👩‍🦯", "When you make a budget but forget about existing ✌️", "That moment when you realize adulting requires actual money management 😭"]
    }
    
    selected_cat = st.radio("What's the vibe today?", ["All"] + list(meme_categories.keys()), horizontal=True)
    
    st.markdown("### Trending Now 🚀")
    
    # Flatten memes for the feed
    all_memes = []
    
    # 1. Add hardcoded memes
    for cat, captions in meme_categories.items():
        if selected_cat == "All" or selected_cat == cat:
            for i, cap in enumerate(captions):
                all_memes.append({"category": cat, "index": i, "caption": cap, "is_user_meme": 0})
    
    # 2. Add user memes from DB
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    query = "SELECT id, username, category, caption, image_path FROM user_memes"
    if selected_cat != "All":
        query += f" WHERE category = '{selected_cat}'"
    user_memes_db = c.execute(query).fetchall()
    conn.close()
    
    for um in user_memes_db:
        all_memes.append({
            "index": um[0], # Using DB ID as index for user memes
            "username": um[1],
            "category": um[2],
            "caption": um[3],
            "image_path": um[4],
            "is_user_meme": 1
        })
    
    # Shuffle for a "discovery" feel if looking at All
    if selected_cat == "All":
        random.seed(42) # Keep it consistent for the session
        random.shuffle(all_memes)

    # Vertical Feed
    for i, meme in enumerate(all_memes):
        is_user = meme.get("is_user_meme", 0)
        with st.container():
            # Styling for the meme card
            border_color = "#BC13FE" if is_user else "#39FF14"
            user_tag = f"<br><span style='font-size: 12px; color: #888;'>Posted by @{meme['username']} ✨</span>" if is_user else ""
            
            st.markdown(
                f"""
                <div style="background-color: #262626; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid {border_color};">
                    <span style="background-color: {border_color}; color: black; padding: 2px 8px; border-radius: 5px; font-size: 12px; font-weight: bold;">#{meme['category']}</span>
                    <p style="font-size: 18px; margin-top: 10px;">{meme['caption']}</p>
                    {user_tag}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Display image if it's a user meme
            if is_user and meme.get('image_path') and os.path.exists(meme['image_path']):
                st.image(meme['image_path'], use_container_width=True)
            
            likes, comments_count, _ = get_engagement_counts(meme['category'], meme['index'], is_user_meme=is_user)
            
            eng_col1, eng_col2, eng_col3, _ = st.columns([1, 1, 1, 3])
            with eng_col1:
                if st.button(f"❤️ {likes}", key=f"feed_like_{i}_{is_user}"):
                    save_engagement(st.session_state.username, meme['category'], meme['index'], "like", is_user_meme=is_user)
                    st.rerun()
            with eng_col2:
                if st.button(f"💬 {comments_count}", key=f"feed_comment_btn_{i}_{is_user}"):
                    st.session_state[f"show_feed_comments_{i}_{is_user}"] = not st.session_state.get(f"show_feed_comments_{i}_{is_user}", False)
            with eng_col3:
                share_links = get_social_share_links(meme['caption'])
                share_platform = st.selectbox("Share", ["Share 🔄"] + list(share_links.keys()), key=f"feed_share_{i}_{is_user}", label_visibility="collapsed")
                if share_platform != "Share 🔄":
                    st.markdown(f"[Send It! 🚀]({share_links[share_platform]})")
                    save_engagement(st.session_state.username, meme['category'], meme['index'], "share", is_user_meme=is_user)
            
            if st.session_state.get(f"show_feed_comments_{i}_{is_user}", False):
                with st.expander("💭 The Comments Section", expanded=True):
                    comment = st.text_input("Share your thoughts... ✨", key=f"feed_input_{i}_{is_user}")
                    if st.button("Post 🚀", key=f"feed_post_{i}_{is_user}"):
                        if comment:
                            save_engagement(st.session_state.username, meme['category'], meme['index'], "comment", comment, is_user_meme=is_user)
                            st.rerun()
                    
                    for user, text in get_comments(meme['category'], meme['index'], is_user_meme=is_user):
                        st.markdown(f"**{user}**: {text}")
            
            st.markdown("<br>", unsafe_allow_html=True)

# --- Finance Quiz Section ---
def init_quiz_db():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_scores (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, score INTEGER, total_questions INTEGER, category TEXT, created_at TIMESTAMP, FOREIGN KEY (username) REFERENCES users(username))''')
    conn.commit()
    conn.close()

def save_score(username, score, total_questions, category):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    c.execute('''INSERT INTO quiz_scores (username, score, total_questions, category, created_at) VALUES (?, ?, ?, ?, ?)''', (username, score, total_questions, category, datetime.now()))
    conn.commit()
    conn.close()

def get_top_scores():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    scores = c.execute('''SELECT username, score, total_questions, category, created_at FROM quiz_scores ORDER BY score DESC, created_at DESC LIMIT 5''').fetchall()
    conn.close()
    return scores

quiz_questions = {
    "Budgeting": [
        {"question": "What's giving 'main character energy' in a 50/30/20 budget rule?", "options": ["50% needs, 30% wants, 20% savings", "50% wants, 30% savings, 20% needs", "50% savings, 30% needs, 20% wants", "50% vibes, 30% aesthetic, 20% reality"], "correct": 0, "explanation": "50% for needs, 30% for wants, and 20% for savings! ✨"},
        {"question": "Emergency fund should cover how many months?", "options": ["1 month", "3-6 months", "12 months", "0 months"], "correct": 1, "explanation": "3-6 months is giving responsible legend energy! �"},
        {"question": "What's a 'sunk cost' in your financial era?", "options": ["Money already spent that can't be recovered", "The cost of a new sink", "A type of high-interest loan", "Money you're planning to spend"], "correct": 0, "explanation": "Sunk costs are gone, friend. Don't throw good money after bad! 🚫"},
        {"question": "Which of these is a 'variable expense'?", "options": ["Rent", "Netflix subscription", "Dining out", "Car insurance"], "correct": 2, "explanation": "Dining out changes every month depending on your vibes! 🍕"},
        {"question": "What does 'paying yourself first' mean?", "options": ["Buying a new outfit on payday", "Saving money before spending on anything else", "Paying your bills on time", "Treating your friends to dinner"], "correct": 1, "explanation": "Put that money in savings first to secure the future bag! 💰"},
        {"question": "What is 'lifestyle creep'?", "options": ["When your spending increases as your income increases", "A scary movie about budgeting", "When you sneak into a VIP lounge", "The cost of moving to a new city"], "correct": 0, "explanation": "Don't let your expenses grow as fast as your bag! 🛑"},
        {"question": "Which of these is a 'fixed expense'?", "options": ["Rent", "Groceries", "Entertainment", "Shopping"], "correct": 0, "explanation": "Rent stays the same every month, it's consistent! 🏠"},
        {"question": "What is 'zero-based budgeting'?", "options": ["When you have zero money left", "Assigning every dollar a job until you reach zero", "Budgeting only for things that cost zero", "A budget that failed"], "correct": 1, "explanation": "Every coin has a purpose in this strategy! 🎯"},
        {"question": "What's the 'latte factor'?", "options": ["The cost of coffee beans", "Small daily expenses that add up over time", "A discount at cafes", "The price of a milk frother"], "correct": 1, "explanation": "Those daily ₹200 coffees add up to a lot of bag over time! ☕"},
        {"question": "What is 'gross income'?", "options": ["Income that is disgusting", "Income after taxes", "Income before taxes and deductions", "Income from side hustles only"], "correct": 2, "explanation": "Gross is the big number before the government takes their cut! 💸"},
        {"question": "What is 'net income'?", "options": ["Income from fishing", "Income before taxes", "Your actual take-home pay after taxes", "Income from the internet"], "correct": 2, "explanation": "Net is what actually hits your bank account! 📥"},
        {"question": "What's an 'envelope system'?", "options": ["Sending letters to your bank", "Using physical envelopes for cash budgeting", "A type of digital filing", "Hiding money in envelopes"], "correct": 1, "explanation": "Old school but effective for tracking cash! ✉️"},
        {"question": "What is 'discretionary spending'?", "options": ["Money spent on needs", "Money spent on wants and fun", "Money spent on taxes", "Money spent on rent"], "correct": 1, "explanation": "This is your 'treat yourself' fund! ✨"},
        {"question": "What's a 'sinking fund'?", "options": ["A fund for a boat", "Saving small amounts for a specific future expense", "A fund that is losing money", "A type of insurance"], "correct": 1, "explanation": "Saving for that vacation or new iPhone bit by bit! 📱"},
        {"question": "What is 'inflation'?", "options": ["When your bank account grows", "When the general price of goods increases", "When taxes are lowered", "When the stock market crashes"], "correct": 1, "explanation": "Inflation makes your coins buy less over time! 🎈"},
        {"question": "What's the '30-day rule'?", "options": ["Wait 30 days before making a non-essential purchase", "Pay your bills in 30 days", "Save for 30 days only", "A 30-day fitness challenge"], "correct": 0, "explanation": "Wait 30 days to see if you actually want it or if it's just an impulse! ⏳"},
        {"question": "What is 'debt-to-income ratio'?", "options": ["Your total debt divided by your gross income", "Your income divided by your debt", "A way to avoid debt", "The interest rate on your debt"], "correct": 0, "explanation": "Lenders use this to see if you can handle more credit! ⚖️"},
        {"question": "What does it mean to 'reconcile' your budget?", "options": ["To delete your budget", "To compare your actual spending with your planned budget", "To ask for a loan", "To pay off all debt"], "correct": 1, "explanation": "Checking if you actually stayed on track friend! ✅"},
        {"question": "What is a 'liquid asset'?", "options": ["Money kept in a bottle", "Assets that can be quickly converted to cash", "A type of crypto coin", "Investments in water companies"], "correct": 1, "explanation": "Cash in your bank is the most liquid asset! 💧"},
        {"question": "What's the purpose of an 'audit'?", "options": ["To get a free loan", "An official inspection of financial accounts", "A way to increase your salary", "A type of bank meeting"], "correct": 1, "explanation": "Making sure the numbers add up correctly! 🧐"},
        {"question": "What is 'opportunity cost'?", "options": ["The cost of a new opportunity", "What you give up when you choose one option over another", "The price of a job application", "A type of investment fee"], "correct": 1, "explanation": "Buying that bag means you can't invest that money. Choose wisely! 🛍️"},
        {"question": "What is 'frugality'?", "options": ["Being cheap and never spending", "Being intentional and careful with your spending", "A type of fruit-based diet", "Investing in low-risk assets"], "correct": 1, "explanation": "Frugality is about value, not just being cheap! 💡"},
        {"question": "What's the 'rule of 72'?", "options": ["A rule for budgeting 72% of income", "A way to estimate how long it takes to double your money", "The age you should retire", "The maximum interest rate allowed"], "correct": 1, "explanation": "72 divided by the interest rate = years to double! 📈"},
        {"question": "What is 'automatic bill pay'?", "options": ["A way to avoid paying bills", "Setting up recurring payments from your account", "A government grant for bills", "Paying bills only when you feel like it"], "correct": 1, "explanation": "Set it and forget it to avoid late fee drama! 🤖"},
        {"question": "What's the main difference between a checking and savings account?", "options": ["Checking is for daily spending, savings is for growth", "Checking is for old people, savings is for GenZ", "Checking has higher interest than savings", "There is no difference"], "correct": 0, "explanation": "Checking is your 'spending vibe', savings is your 'future vibe'! 🏦"}
    ],
    "Investing": [
        {"question": "Which investment is giving 'long-term relationship' vibes?", "options": ["Day trading", "Index funds", "Penny stocks", "Friend's startup"], "correct": 1, "explanation": "Index funds are stable and reliable! 💍"},
        {"question": "What is 'diversification'?", "options": ["Investing only in tech stocks", "Spreading money across different assets", "Keeping all money in a savings account", "Buying only Bitcoin"], "correct": 1, "explanation": "Don't put all your eggs in one basket, it's not the vibe! 🥚"},
        {"question": "What is a 'bull market'?", "options": ["When prices are falling", "When prices are rising", "When the market is closed", "A market for agricultural products"], "correct": 1, "explanation": "Bull markets are charging up! 📈"},
        {"question": "What does ROI stand for?", "options": ["Risk of Investment", "Return on Investment", "Rate of Interest", "Really Over-Invested"], "correct": 1, "explanation": "Return on Investment - we love to see that bag grow! 💸"},
        {"question": "Which of these is generally the highest risk?", "options": ["Savings Account", "Government Bonds", "Individual Stocks", "Fixed Deposits"], "correct": 2, "explanation": "Stocks can be a rollercoaster, stay safe! 🎢"},
        {"question": "What is a 'bear market'?", "options": ["When prices are rising", "When prices are falling", "A market for wildlife", "When the market is stable"], "correct": 1, "explanation": "Bear markets are hibernating and falling! 📉"},
        {"question": "What are 'dividends'?", "options": ["Fees you pay to brokers", "Payments made by a corporation to its shareholders", "The cost of buying a stock", "Tax on investments"], "correct": 1, "explanation": "Companies sharing their profits with you. Free money vibes! 💰"},
        {"question": "What is an 'ETF'?", "options": ["Exchange Traded Fund", "Extra Transaction Fee", "Equity Trading Firm", "Electronic Transfer Fund"], "correct": 0, "explanation": "Like a mutual fund but trades like a stock. Very aesthetic! 📊"},
        {"question": "What is 'compound interest' in investing?", "options": ["Interest on the original amount only", "Interest calculated on the principal and accumulated interest", "A type of bank fee", "Tax on your profit"], "correct": 1, "explanation": "The 8th wonder of the world for your bag! ❄️"},
        {"question": "What is 'market capitalization'?", "options": ["The city where the stock exchange is located", "The total value of a company's shares", "The amount of cash a company has", "The number of employees in a company"], "correct": 1, "explanation": "It tells you how big the company's 'main character' energy is! �"},
        {"question": "What is 'dollar-cost averaging' (DCA)?", "options": ["Investing the same amount regularly regardless of price", "Buying only when the price is low", "Selling when the price is high", "Trading dollars for other currencies"], "correct": 0, "explanation": "A consistent way to build wealth without timing the market! 📅"},
        {"question": "What is a 'P/E ratio'?", "options": ["Price-to-Earnings ratio", "Profit-to-Expense ratio", "Portfolio-to-Equity ratio", "Price-to-Entry ratio"], "correct": 0, "explanation": "Helps you see if a stock is overpriced or a steal! 🔍"},
        {"question": "What is 'asset allocation'?", "options": ["Giving away your assets", "Dividing your portfolio among different categories", "Choosing which bank to use", "Buying only one type of stock"], "correct": 1, "explanation": "The mix of stocks, bonds, and <span class=\"math-inline\">\\\\text\{cash\}\</span> in your portfolio! 🎨"},
        {"question": "What is 'risk tolerance'?", "options": ["The amount of risk you can handle without panicking", "The total amount of money you have", "A type of insurance policy", "The interest rate on a loan"], "correct": 0, "explanation": "Knowing your vibe when the market dips! 📉"},
        {"question": "What is a 'stock split'?", "options": ["When a company goes bankrupt", "Increasing the number of shares by splitting existing ones", "Selling half of your shares", "When two companies merge"], "correct": 1, "explanation": "More shares at a lower price, same total value! ✂️"},
        {"question": "What is an 'IPO'?", "options": ["Initial Public Offering", "Internal Profit Option", "International Price Order", "Instant Payment Online"], "correct": 0, "explanation": "When a company first goes public on the stock market! 🚀"},
        {"question": "What are 'blue chip stocks'?", "options": ["Stocks of small, new companies", "Stocks of large, well-established, profitable companies", "Stocks that cost very little", "Stocks in the gambling industry"], "correct": 1, "explanation": "The 'Legacy' of the stock market. Stable vibes! 💎"},
        {"question": "What is 'value investing'?", "options": ["Buying stocks that are popular on TikTok", "Buying stocks that are undervalued compared to their worth", "Buying stocks with the highest price", "Investing in expensive jewelry"], "correct": 1, "explanation": "Finding those hidden gems at a discount! 💎"},
        {"question": "What is 'rebalancing' a portfolio?", "options": ["Withdrawing all your money", "Adjusting the weights of your assets back to your target", "Buying more of your favorite stock", "Opening a new brokerage account"], "correct": 1, "explanation": "Keeping your investment vibes in check! ⚖️"},
        {"question": "What is 'capital gains tax'?", "options": ["Tax on your salary", "Tax on the profit from selling an asset", "Tax on your savings account", "Tax for living in a capital city"], "correct": 1, "explanation": "The government's cut when you sell for a profit! 💸"},
        {"question": "What is 'volatility'?", "options": ["When the market stays the same", "The rate at which the price of an asset increases or decreases", "A type of high-speed trading", "When a company pays a dividend"], "correct": 1, "explanation": "The rollercoaster vibes of the market! 🎢"},
        {"question": "What is a 'bond'?", "options": ["A type of stock", "A loan you give to a government or corporation", "A contract with your broker", "A shared bank account"], "correct": 1, "explanation": "You're the lender now, friend! 📜"},
        {"question": "What is 'liquidity' in investing?", "options": ["How much cash a company has", "How easily an asset can be turned into cash", "Investing in beverage companies", "The total volume of trades in a day"], "correct": 1, "explanation": "How fast can you get your bag back! 💧"},
        {"question": "What is a 'REIT'?", "options": ["Real Estate Investment Trust", "Return on Equity Investment Tool", "Regional Equity Information Team", "Real Estate Interest Tax"], "correct": 0, "explanation": "Investing in real estate without buying a whole building! 🏢"},
        {"question": "What is a 'mutual fund'?", "options": ["A fund you share with a friend", "A pool of money from many investors managed by a pro", "A fund that only buys Bitcoin", "A type of personal savings account"], "correct": 1, "explanation": "The ultimate group project for your money! 🤝"}
    ],
    "Credit": [
        {"question": "What's a good credit score giving?", "options": ["Lower interest rates on loans", "Free coffee at Starbucks", "More followers on TikTok", "Higher taxes"], "correct": 0, "explanation": "A high score gets you the best deals on loans! 💳"},
        {"question": "What is 'compound interest' in debt?", "options": ["Interest on the principal only", "Interest on interest", "A type of bank fee", "Tax on your savings"], "correct": 1, "explanation": "Interest on interest makes your debt grow exponentially! ❄️"},
        {"question": "Which factor affects your credit score the most?", "options": ["Your income", "Payment history", "The bank you use", "Your age"], "correct": 1, "explanation": "Pay those bills on time to keep your score iconic! ✅"},
        {"question": "What's a 'credit limit'?", "options": ["The maximum you can spend on your card", "The minimum you must pay", "Your daily withdrawal limit", "The interest rate you pay"], "correct": 0, "explanation": "Don't max out your card, it's not the aesthetic! 🛑"},
        {"question": "What is an APR?", "options": ["Annual Percentage Rate", "Automatic Payment Receipt", "Account Premium Ratio", "Annual Profit Return"], "correct": 0, "explanation": "APR is the yearly cost of borrowing money! 📉"},
        {"question": "What is 'credit utilization ratio'?", "options": ["The amount of credit you use compared to your limit", "How many credit cards you have", "Your total credit score", "How often you use your card"], "correct": 0, "explanation": "Keep it under 30% for that healthy score vibe! 📉"},
        {"question": "What is a 'hard inquiry'?", "options": ["When you check your own score", "When a lender checks your credit for a loan application", "When you forget your password", "A difficult question from a bank"], "correct": 1, "explanation": "This can temporarily dip your score, use it wisely! 🔍"},
        {"question": "What is a 'soft inquiry'?", "options": ["Checking your own credit score", "Applying for a mortgage", "Getting a new credit card", "A background check by an employer"], "correct": 0, "explanation": "Checking your own score doesn't hurt it! ✨"},
        {"question": "What's the difference between a secured and unsecured loan?", "options": ["Secured requires collateral, unsecured doesn't", "Secured is only for rich people", "Unsecured is always better", "There is no difference"], "correct": 0, "explanation": "Collateral (like a car or house) makes a loan 'secured'! 🛡️"},
        {"question": "What is a 'co-signer'?", "options": ["Someone who uses your credit card", "Someone who agrees to pay your loan if you can't", "A witness to a contract", "Your bank manager"], "correct": 1, "explanation": "They're putting their score on the line for you! 🤝"},
        {"question": "What is 'identity theft'?", "options": ["When someone steals your physical ID card", "When someone uses your personal info for fraud", "Forgetting your name", "Using a fake name on social media"], "correct": 1, "explanation": "Protect your info like it's your private story! 🔐"},
        {"question": "What is a 'credit report'?", "options": ["A list of your social media posts", "A detailed history of your credit use", "A report card from school", "A bank statement"], "correct": 1, "explanation": "It's your financial resume! 📜"},
        {"question": "What is 'foreclosure'?", "options": ["When you close your bank account", "When a lender takes your home because you didn't pay", "A type of lock on a vault", "Closing a credit card"], "correct": 1, "explanation": "A serious consequence of missing mortgage payments! 🏠"},
        {"question": "What is 'bankruptcy'?", "options": ["When you're out of cash for the weekend", "A legal process for when you can't pay your debts", "A way to get free money", "A type of bank account"], "correct": 1, "explanation": "A last resort that stays on your record for a long time! 🛑"},
        {"question": "What is a 'balance transfer'?", "options": ["Moving money from savings to checking", "Moving debt from one credit card to another", "Withdrawing cash from an ATM", "Giving money to a friend"], "correct": 1, "explanation": "Often used to get a lower interest rate on debt! 🔄"},
        {"question": "What's the 'minimum payment trap'?", "options": ["Paying only the minimum due, which leads to massive interest", "A fee for not using your card", "When your card gets stuck in an ATM", "A discount for paying early"], "correct": 0, "explanation": "Only paying the minimum means you'll be in debt forever! 🪤"},
        {"question": "What is an 'annual fee'?", "options": ["A fee you pay every month", "A yearly fee for having certain credit cards", "The interest rate you pay", "A bonus you get every year"], "correct": 1, "explanation": "Make sure the perks are worth the price friend! 💸"},
        {"question": "What are 'credit card rewards'?", "options": ["Gifts from your friends", "Points, miles, or cash back you earn for spending", "A higher credit score", "Free interest for a year"], "correct": 1, "explanation": "Getting paid to spend your own money. Win! 🎁"},
        {"question": "What's the main difference between a credit and debit card?", "options": ["Credit is borrowing, debit is using your own money", "Credit is plastic, debit is metal", "Credit is for shopping, debit is for bills", "There is no difference"], "correct": 0, "explanation": "Debit is your current bag, credit is a future debt! 💳"},
        {"question": "What is 'revolving credit'?", "options": ["A loan for a revolving door", "A line of credit you can use and repay repeatedly", "A loan that must be paid in one go", "A type of high-interest investment"], "correct": 1, "explanation": "Like a credit card, the limit resets as you pay it off! 🔄"},
        {"question": "What does it mean to 'default' on a loan?", "options": ["To pay it off early", "Failing to repay the loan according to the terms", "To change the interest rate", "To ask for more money"], "correct": 1, "explanation": "This will wreck your credit score vibes! 📉"},
        {"question": "What is 'credit counseling'?", "options": ["Talking to your friends about money", "Professional help for managing debt and credit", "A type of bank commercial", "A class on how to use ATMs"], "correct": 1, "explanation": "Getting expert help when the debt drama is too much! 🧠"},
        {"question": "What is 'debt consolidation'?", "options": ["Taking more loans", "Combining multiple debts into one single payment", "Deleting your debt records", "Investing in debt companies"], "correct": 1, "explanation": "Simplifying your life by merging those bills! 🤝"},
        {"question": "What's an 'interest-free period'?", "options": ["A time when you don't have to pay anything", "A period where no interest is charged on new purchases", "When the bank gives you free money", "A type of holiday for banks"], "correct": 1, "explanation": "Pay it off before this ends to avoid the drama! ⏳"},
        {"question": "How do you start building credit from scratch?", "options": ["By not using any banks", "Getting a secured credit card or being an authorized user", "Winning the lottery", "Spending all your cash"], "correct": 1, "explanation": "Start small to show you can handle the responsibility! 🌱"}
    ],
    "Taxes 📝": [
        {"question": "What is 'Income Tax' giving?", "options": ["A percentage of your earnings paid to the government", "A fee for having a bank account", "A discount on your groceries", "A prize for working hard"], "correct": 0, "explanation": "Income tax is your contribution to public services! 🛣️"},
        {"question": "What does 'Tax Deductible' mean?", "options": ["An expense that reduces your taxable income", "A tax that is deducted twice", "A way to avoid paying taxes entirely", "A fee for late tax payment"], "correct": 0, "explanation": "Deductions lower the amount of income you're taxed on. Legal discount! 💸"},
        {"question": "What is a 'TDS'?", "options": ["Tax Deducted at Source", "Total Debt Status", "Tax Discount System", "Terminal Debt Service"], "correct": 0, "explanation": "TDS is tax collected right when you earn money! 💼"},
        {"question": "When is the typical deadline for tax filing in India?", "options": ["July 31st", "December 25th", "January 1st", "April 1st"], "correct": 0, "explanation": "Keep July 31st in your calendar to avoid the 'late fee' drama! 🗓️"},
        {"question": "What is 'GST'?", "options": ["Goods and Services Tax", "General Savings Tax", "Government Service Token", "Grand Sales Tax"], "correct": 0, "explanation": "GST is the tax you pay on most things you buy! 🛍️"},
        {"question": "What are 'tax brackets'?", "options": ["Brackets used to hold tax documents", "Ranges of income that are taxed at different rates", "A type of bank account", "The cost of filing taxes"], "correct": 1, "explanation": "The more you earn, the higher your bracket energy! 📈"},
        {"question": "What is a 'standard deduction'?", "options": ["A deduction everyone gets without needing receipts", "A deduction for students only", "A tax on standard products", "A fee for filing taxes"], "correct": 0, "explanation": "A flat amount that reduces your taxable income automatically! ✅"},
        {"question": "What's the difference between a tax credit and a tax deduction?", "options": ["Credit reduces tax directly, deduction reduces taxable income", "Deduction is better than credit", "Credit is for loans, deduction is for salary", "There is no difference"], "correct": 0, "explanation": "Credits are the ultimate win because they cut your tax bill directly! ✂️"},
        {"question": "What is 'Form 16'?", "options": ["A form for opening a bank account", "A certificate showing your salary and taxes deducted", "A form to apply for a credit card", "A type of tax for 16-year-olds"], "correct": 1, "explanation": "Your employer gives you this to help you file your taxes! 📄"},
        {"question": "Why is a PAN card important for taxes?", "options": ["It's a cool-looking card", "It's your unique ID for all tax-related transactions", "It gives you discounts on shopping", "It's needed for social media"], "correct": 1, "explanation": "Permanent Account Number - essential for your financial identity! 🆔"},
        {"question": "What is 'tax evasion'?", "options": ["Illegally not paying your taxes", "Legally reducing your taxes", "A type of tax for travelers", "Paying taxes early"], "correct": 0, "explanation": "Tax evasion is illegal and definitely not the vibe! 🚫"},
        {"question": "What is 'tax avoidance'?", "options": ["Illegally hiding money", "Legally using tax laws to reduce your tax bill", "Ignoring your tax notices", "A type of tax for avoiding work"], "correct": 1, "explanation": "Avoidance is smart and legal. We love a tax-savvy pro! 🧠"},
        {"question": "What are 'indirect taxes'?", "options": ["Taxes you pay directly to the government", "Taxes included in the price of goods and services", "Taxes on your secret income", "Taxes you pay to your friends"], "correct": 1, "explanation": "Like GST, you pay it when you buy things! 🛍️"},
        {"question": "What is 'excise duty'?", "options": ["A tax on imported goods", "A tax on goods produced within the country", "A tax on your daily exercise", "A fee for government employees"], "correct": 1, "explanation": "Tax on manufacturing items like fuel or tobacco! ⛽"},
        {"question": "What is 'customs duty'?", "options": ["A tax on things you make at home", "A tax on goods imported or exported from the country", "A fee for being a customer", "A type of tax for weddings"], "correct": 1, "explanation": "Paid at the border for those international vibes! ✈️"},
        {"question": "What is 'corporate tax'?", "options": ["Tax on your personal salary", "Tax on the profits of a company", "Tax for working in an office", "A fee for starting a business"], "correct": 1, "explanation": "Companies have to pay their share too! 🏢"},
        {"question": "What's the difference between short-term and long-term capital gains?", "options": ["The length of time you held the asset before selling", "The amount of profit you made", "The type of asset you sold", "The bank you used"], "correct": 0, "explanation": "Holding for longer usually means lower tax rates. Patience slays! ⏳"},
        {"question": "What are 'tax-free bonds'?", "options": ["Bonds that are free to buy", "Bonds where the interest earned is not taxed", "Bonds for people who don't pay taxes", "A type of glue for tax forms"], "correct": 1, "explanation": "A great way to grow your bag without the tax drama! 📜"},
        {"question": "What is 'Section 80C' in India?", "options": ["A section of the stock market", "A section of the tax law allowing deductions up to ₹1.5 lakh", "A type of bank account", "A penalty for late filing"], "correct": 1, "explanation": "The most popular way to save tax by investing! 💰"},
        {"question": "What is 'Section 80D'?", "options": ["A deduction for education loans", "A deduction for health insurance premiums", "A tax on dividends", "A fee for digital transactions"], "correct": 1, "explanation": "Stay healthy and save tax at the same time! 🏥"},
        {"question": "What is 'HRA'?", "options": ["House Rent Allowance", "High Return Asset", "Health Risk Assessment", "Home Record Account"], "correct": 0, "explanation": "A portion of your salary to cover rent, which can be tax-exempt! 🏠"},
        {"question": "What is 'professional tax'?", "options": ["A tax on professional athletes only", "A small tax on salaried employees in some states", "A fee for being an expert", "A tax on professional equipment"], "correct": 1, "explanation": "A state-level tax on your profession! 💼"},
        {"question": "What is 'advance tax'?", "options": ["Paying taxes for the next 10 years", "Paying your taxes in installments during the year", "A type of high-tech tax system", "A tax for advanced investors"], "correct": 1, "explanation": "Pay as you earn to avoid interest penalties! 💸"},
        {"question": "What is a 'tax refund'?", "options": ["A gift from the government", "When the government gives back excess tax you paid", "A discount on your next tax bill", "Money you have to pay back"], "correct": 1, "explanation": "That sweet moment when the extra tax comes back home! 📥"},
        {"question": "What is 'wealth tax'?", "options": ["A tax on being rich", "A tax on the value of your assets (historically used)", "A way to build wealth", "A fee for financial advice"], "correct": 1, "explanation": "A tax on the net wealth you hold, though now abolished in many places! 💎"}
    ]
}

def finance_quiz():
    if not st.session_state.logged_in:
        st.error("Friend, login first! 🫖")
        return
    init_quiz_db()
    st.title(" Financial Knowledge Check")
    
    # Initialize session state for quiz
    if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
    if 'questions_answered' not in st.session_state: st.session_state.questions_answered = 0
    if 'quiz_complete' not in st.session_state: st.session_state.quiz_complete = False
    if 'selected_category' not in st.session_state: st.session_state.selected_category = None
    if 'current_quiz_questions' not in st.session_state: st.session_state.current_quiz_questions = []

    if not st.session_state.selected_category:
        st.subheader("Pick your category! ✨")
        categories = list(quiz_questions.keys())
        cols = st.columns(len(categories))
        for i, category in enumerate(categories):
            if cols[i].button(f"{category} ", key=f"cat_{category}"):
                # Randomly select 10 questions from the category
                all_cat_questions = quiz_questions[category]
                st.session_state.current_quiz_questions = random.sample(all_cat_questions, min(10, len(all_cat_questions)))
                st.session_state.selected_category = category
                st.session_state.quiz_score = 0
                st.session_state.questions_answered = 0
                st.session_state.quiz_complete = False
                st.rerun()
    elif not st.session_state.quiz_complete:
        category = st.session_state.selected_category
        questions = st.session_state.current_quiz_questions
        
        if st.session_state.questions_answered < len(questions):
            q_data = questions[st.session_state.questions_answered]
            st.markdown(f"### Question {st.session_state.questions_answered + 1} of {len(questions)}")
            st.markdown(f"**{q_data['question']}**")
            
            # Use radio for options to avoid instant rerun on button click before showing explanation
            options_with_none = ["Select an option..."] + q_data['options']
            choice = st.radio("Choose the correct vibe:", options_with_none, key=f"q_{st.session_state.questions_answered}")
            
            if choice != "Select an option...":
                selected_idx = q_data['options'].index(choice)
                if st.button("Submit Answer"):
                    if selected_idx == q_data['correct']:
                        st.success("Absolute Legend! ✨")
                        st.session_state.quiz_score += 1
                    else:
                        st.error("Not quite! 🧐")
                    
                    st.info(q_data['explanation'])
                    st.session_state.questions_answered += 1
                    
                    if st.session_state.questions_answered < len(questions):
                        if st.button("Next Question"):
                            st.rerun()
                    else:
                        st.session_state.quiz_complete = True
                        save_score(st.session_state.username, st.session_state.quiz_score, len(questions), category)
                        st.rerun()
    else:
        st.balloons()
        st.success(f"Final Score: {st.session_state.quiz_score}/{len(st.session_state.current_quiz_questions)}")
        
        # Calculate percentage
        percentage = (st.session_state.quiz_score / len(st.session_state.current_quiz_questions)) * 100
        
        if percentage == 100:
            st.markdown("### � TOTAL LEGEND! You're a financial icon! �")
        elif percentage >= 70:
            st.markdown("### ✨ Good vibes! You're getting that bag! ✨")
        elif percentage >= 40:
            st.markdown("### 📈 Getting there! Keep building that empire! 📈")
        else:
            st.markdown("### ☕ Time to study the facts! ☕")
            
        if st.button("New Category"):
            st.session_state.selected_category = None
            st.session_state.quiz_score = 0
            st.session_state.questions_answered = 0
            st.session_state.quiz_complete = False
            st.session_state.current_quiz_questions = []
            st.rerun()

# --- Investment Vibes Section ---
def fetch_ticker_data(tickers):
    if not tickers:
        return []
    
    data = []
    try:
        # Download 2 days of data for all tickers at once for efficiency
        # We use group_by='ticker' to get a multi-index DataFrame
        df_all = yf.download(tickers, period="2d", interval="1d", group_by='ticker', progress=False)
        
        for ticker in tickers:
            try:
                # Handle single vs multiple tickers in download result
                if len(tickers) == 1:
                    df = df_all
                else:
                    df = df_all[ticker]
                
                if not df.empty and len(df) >= 1:
                    # Current price is the last Close
                    current_price = df['Close'].iloc[-1]
                    
                    # Previous close
                    if len(df) >= 2:
                        prev_close = df['Close'].iloc[-2]
                    else:
                        # Fallback if only 1 day is available
                        prev_close = df['Open'].iloc[-1]
                    
                    if pd.notna(current_price) and pd.notna(prev_close):
                        change = current_price - prev_close
                        percent_change = (change / prev_close) * 100
                        
                        # Determine currency symbol
                        currency = "₹" if ticker.endswith('.NS') else "$"
                        
                        data.append({
                            "Symbol": ticker,
                            "Price": f"{currency}{current_price:,.2f}",
                            "Change": f"{'+' if change > 0 else ''}{change:,.2f}",
                            "Change %": f"{'+' if change > 0 else ''}{percent_change:,.2f}%",
                            "Status": "🚀" if change > 0 else "📉"
                        })
            except Exception as e:
                # Log error internally or skip
                continue
    except Exception as e:
        # If bulk download fails, try individual tickers as fallback
        for ticker in tickers:
            try:
                # Use a slightly different method for individual tickers if needed
                t = yf.Ticker(ticker)
                # fast_info is a lightweight way to get current data in newer yfinance
                try:
                    current_price = t.fast_info.last_price
                    prev_close = t.fast_info.previous_close
                except:
                    # History fallback
                    df = t.history(period="2d", interval="1d", progress=False)
                    if not df.empty:
                        current_price = df['Close'].iloc[-1]
                        prev_close = df['Close'].iloc[-2] if len(df) >= 2 else df['Open'].iloc[-1]
                    else:
                        continue
                
                if pd.notna(current_price) and pd.notna(prev_close):
                    change = current_price - prev_close
                    percent_change = (change / prev_close) * 100
                    currency = "₹" if ticker.endswith('.NS') else "$"
                    data.append({
                        "Symbol": ticker,
                        "Price": f"{currency}{current_price:,.2f}",
                        "Change": f"{'+' if change > 0 else ''}{change:,.2f}",
                        "Change %": f"{'+' if change > 0 else ''}{percent_change:,.2f}%",
                        "Status": "🚀" if change > 0 else "📉"
                    })
            except:
                continue
                
    return data

def investment_vibes():
    if not st.session_state.get('logged_in', False):
        st.error("Friend, login first! 🫖")
        return
    
    st.title("✨ Investment Vibes Check ✨")
    st.markdown("### Because we're not just saving, we're building an empire! �")
    
    st.info("Investments are like your daily routine - the earlier you start, the better you'll look in 20 years! 💆‍♂️")
    
    # Live data toggle
    live_mode = st.toggle("Enable Live Mode (Auto-updates every 10s) 🔥", value=False)
    
    # Placeholder for live data
    live_placeholder = st.empty()
    
    # Tickers to track
    stock_tickers = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT", "RELIANCE.NS", "TCS.NS"]
    crypto_tickers = ["BTC-USD", "ETH-USD", "DOGE-USD", "SOL-USD"]
    
    def display_data():
        with live_placeholder.container():
            tab1, tab2 = st.tabs(["Stock Market 📈", "Crypto Market 🚀"])
            
            with tab1:
                st.header("Real-time Stocks �")
                stock_data = fetch_ticker_data(stock_tickers)
                if stock_data:
                    df_stocks = pd.DataFrame(stock_data)
                    st.dataframe(df_stocks.style.applymap(
                        lambda x: 'color: #00ff00' if '+' in str(x) else 'color: #ff3b5c' if '-' in str(x) else '',
                        subset=['Change', 'Change %']
                    ), use_container_width=True)
                else:
                    st.warning("Fetching live stock talk... 🫖")
            
            with tab2:
                st.header("Real-time Crypto 🚀")
                crypto_data = fetch_ticker_data(crypto_tickers)
                if crypto_data:
                    df_crypto = pd.DataFrame(crypto_data)
                    st.dataframe(df_crypto.style.applymap(
                        lambda x: 'color: #00ff00' if '+' in str(x) else 'color: #ff3b5c' if '-' in str(x) else '',
                        subset=['Change', 'Change %']
                    ), use_container_width=True)
                else:
                    st.warning("Fetching live crypto vibes... 🌊")
            
            st.markdown(f"*Last updated: {datetime.now().strftime('%H:%M:%S')}*")

    if live_mode:
        # Loop for live updates
        while live_mode:
            display_data()
            time.sleep(10)
            st.rerun()
    else:
        # Single display
        display_data()
        if st.button("Refresh Vibes 🔄"):
            st.rerun()

    st.markdown("---")
    st.header("Which Investor Are You? 🧠")
    risk_profile = st.radio("Market dips? 📉", ["Panic! (Low)", "Wait and see (Mid)", "Buy the dip! (High)"])
    if "Panic" in risk_profile: st.write("Safety First Legend! 🛡️")
    elif "Wait" in risk_profile: st.write("Balanced Pro! ⚖️")
    else: st.write("Risk-Taking Icon! 🚀")
