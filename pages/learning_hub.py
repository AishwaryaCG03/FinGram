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
    if hashtags is None: hashtags = ["FinTok", "MoneyMoves", "RichGirlEra", "FinanceCheck"]
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
        st.error("Bestie, login first! 🫖")
        return
    st.title("💅 Financial Memes That Hit Different")
    meme_categories = {
        "Savings": ["Me looking at my bank account after saying 'treat yourself' 👀", "My savings account watching me buy another iced coffee ☕", "That moment when your emergency fund is looking thicker than your ex 💅"],
        "Investing": ["Stock market be like: 📈📉 and I be like: 🙃", "Me pretending to understand crypto while buying the dip 🤡", "When someone says they're investing in their 401k: 'It's giving responsible' ✨"],
        "Budgeting": ["My budget: exists\nMe: I pretend I do not see it 👩‍🦯", "When you make a budget but forget about existing ✌️", "That moment when you realize adulting requires actual money management 😭"]
    }
    tabs = st.tabs(list(meme_categories.keys()))
    for tab, (category, captions) in zip(tabs, meme_categories.items()):
        with tab:
            st.header(f"{category} Memes 🔥")
            cols = st.columns(2)
            for i, caption in enumerate(captions):
                with cols[i % 2]:
                    st.markdown(f"### {caption}")
                    st.markdown("*[Meme placeholder]*")
                    likes, comments_count, shares = get_engagement_counts(category, i)
                    eng_col1, eng_col2, eng_col3 = st.columns(3)
                    with eng_col1:
                        if st.button(f"❤️ {likes}", key=f"like_{category}_{i}"):
                            save_engagement(st.session_state.username, category, i, "like")
                            st.rerun()
                    with eng_col2:
                        if st.button(f"💬 {comments_count}", key=f"comment_btn_{category}_{i}"):
                            st.session_state[f"show_comments_{category}_{i}"] = True
                    with eng_col3:
                        share_links = get_social_share_links(caption)
                        share_platform = st.selectbox("Share", ["Share 🔄"] + list(share_links.keys()), key=f"share_select_{category}_{i}")
                        if share_platform != "Share 🔄":
                            st.markdown(f"[Share on {share_platform}]({share_links[share_platform]})")
                            save_engagement(st.session_state.username, category, i, "share")
                    if st.session_state.get(f"show_comments_{category}_{i}", False):
                        with st.expander("💭 Comments", expanded=True):
                            comment = st.text_input("Thoughts? 💅", key=f"comment_input_{category}_{i}")
                            if st.button("Post 🚀", key=f"post_comment_{category}_{i}"):
                                save_engagement(st.session_state.username, category, i, "comment", comment)
                                st.rerun()
                            for user, text in get_comments(category, i): st.markdown(f"**{user}**: {text}")

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
    "Budgeting": [{"question": "What's giving 'main character energy' in a 50/30/20 budget rule?", "options": ["50% needs, 30% wants, 20% savings", "50% wants, 30% savings, 20% needs", "50% savings, 30% needs, 20% wants", "50% vibes, 30% aesthetic, 20% reality"], "correct": 0, "explanation": "50% for needs, 30% for wants, and 20% for savings! 💅"}, {"question": "Emergency fund should cover how many months?", "options": ["1 month", "3-6 months", "12 months", "0 months"], "correct": 1, "explanation": "3-6 months is giving responsible queen energy! 👑"}],
    "Investing": [{"question": "Which investment is giving 'long-term relationship' vibes?", "options": ["Day trading", "Index funds", "Penny stocks", "Friend's startup"], "correct": 1, "explanation": "Index funds are stable and reliable! 💍"}]
}

def finance_quiz():
    if not st.session_state.logged_in:
        st.error("Bestie, login first! 🫖")
        return
    init_quiz_db()
    st.title(" Financial Knowledge Check")
    if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
    if 'questions_answered' not in st.session_state: st.session_state.questions_answered = 0
    if 'quiz_complete' not in st.session_state: st.session_state.quiz_complete = False
    if 'selected_category' not in st.session_state: st.session_state.selected_category = None
    if not st.session_state.selected_category:
        categories = list(quiz_questions.keys())
        cols = st.columns(len(categories))
        for i, category in enumerate(categories):
            if cols[i].button(f"{category} ", key=f"cat_{category}"):
                st.session_state.selected_category, st.session_state.quiz_score, st.session_state.questions_answered, st.session_state.quiz_complete = category, 0, 0, False
                st.rerun()
    elif not st.session_state.quiz_complete:
        category = st.session_state.selected_category
        questions = quiz_questions[category]
        if st.session_state.questions_answered < len(questions):
            q_data = questions[st.session_state.questions_answered]
            st.markdown(f"**{q_data['question']}**")
            cols = st.columns(2)
            selected = None
            for i, opt in enumerate(q_data['options']):
                if cols[i % 2].button(opt, key=f"opt_{i}"): selected = i
            if selected is not None:
                if selected == q_data['correct']:
                    st.success("Yasss queen! ✨")
                    st.session_state.quiz_score += 1
                else: st.error("Not the serve bestie! 💁‍♀️")
                st.info(q_data['explanation'])
                st.session_state.questions_answered += 1
                if st.session_state.questions_answered < len(questions):
                    if st.button("Next Question"): st.rerun()
                else:
                    st.session_state.quiz_complete = True
                    save_score(st.session_state.username, st.session_state.quiz_score, len(questions), category)
                    st.rerun()
    else:
        st.success(f"Score: {st.session_state.quiz_score}/{len(quiz_questions[st.session_state.selected_category])}")
        if st.button("New Category"): st.session_state.selected_category, st.session_state.quiz_score, st.session_state.questions_answered, st.session_state.quiz_complete = None, 0, 0, False; st.rerun()

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
        st.error("Bestie, login first! 🫖")
        return
    
    st.title("✨ Investment Vibes Check ✨")
    st.markdown("### Because we're not just saving, we're building an empire! 💅")
    
    st.info("Investments are like your skincare routine - the earlier you start, the better you'll look in 20 years! 💆‍♀️")
    
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
                st.header("Real-time Stocks 💅")
                stock_data = fetch_ticker_data(stock_tickers)
                if stock_data:
                    df_stocks = pd.DataFrame(stock_data)
                    st.dataframe(df_stocks.style.applymap(
                        lambda x: 'color: #00ff00' if '+' in str(x) else 'color: #ff3b5c' if '-' in str(x) else '',
                        subset=['Change', 'Change %']
                    ), use_container_width=True)
                else:
                    st.warning("Fetching live stock tea... 🫖")
            
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
    if "Panic" in risk_profile: st.write("Safety First Queen! 🛡️")
    elif "Wait" in risk_profile: st.write("Balanced Bestie! ⚖️")
    else: st.write("Risk-Taking Icon! 🚀")
