import streamlit as st
import hashlib
import sqlite3
import os

# Initialize database
def init_db():
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT,
                  email TEXT UNIQUE)''')
    
    # Create engagement table for likes, comments, shares
    c.execute('''CREATE TABLE IF NOT EXISTS engagement
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  meme_category TEXT,
                  meme_index INTEGER,
                  engagement_type TEXT,
                  comment_text TEXT,
                  FOREIGN KEY (username) REFERENCES users(username))''')
    
    conn.commit()
    conn.close()

# Hash password
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Check login credentials
def check_login(username, password):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    hashed_pw = hash_password(password)
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashed_pw))
    result = c.fetchone()
    conn.close()
    
    return result is not None

# Register new user
def register_user(username, password, email):
    try:
        conn = sqlite3.connect('genz_finance.db')
        c = conn.cursor()
        
        hashed_pw = hash_password(password)
        c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                 (username, hashed_pw, email))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Save engagement (likes, comments, shares)
def save_engagement(username, meme_category, meme_index, engagement_type, comment_text=None):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO engagement 
                 (username, meme_category, meme_index, engagement_type, comment_text)
                 VALUES (?, ?, ?, ?, ?)''',
              (username, meme_category, meme_index, engagement_type, comment_text))
    
    conn.commit()
    conn.close()

# Get engagement counts
def get_engagement_counts(meme_category, meme_index):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    likes = c.execute('''SELECT COUNT(*) FROM engagement 
                        WHERE meme_category=? AND meme_index=? AND engagement_type='like' ''',
                     (meme_category, meme_index)).fetchone()[0]
    
    comments = c.execute('''SELECT COUNT(*) FROM engagement 
                           WHERE meme_category=? AND meme_index=? AND engagement_type='comment' ''',
                        (meme_category, meme_index)).fetchone()[0]
    
    shares = c.execute('''SELECT COUNT(*) FROM engagement 
                         WHERE meme_category=? AND meme_index=? AND engagement_type='share' ''',
                      (meme_category, meme_index)).fetchone()[0]
    
    conn.close()
    return likes, comments, shares

# Get comments for a meme
def get_comments(meme_category, meme_index):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    comments = c.execute('''SELECT username, comment_text FROM engagement 
                           WHERE meme_category=? AND meme_index=? AND engagement_type='comment'
                           ORDER BY id DESC''',
                        (meme_category, meme_index)).fetchall()
    
    conn.close()
    return comments

# Initialize session state
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None

# Login page
def login_page():
    st.title("✨ Welcome to FinGram ✨")
    st.markdown("### Secure the bag by logging in first bestie! ")
    
    tab1, tab2 = st.tabs(["Login 🔑", "Sign Up 📝"])
    
    with tab1:
        username = st.text_input("Username (spill the tea) ☕")
        password = st.text_input("Password (keep it secret bestie) 🤫", type="password")
        
        if st.button("Login "):
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Welcome back bestie! Time to get that bread! 🍞")
                st.rerun()
            else:
                st.error("Wrong credentials bestie! Try again! 😭")
    
    with tab2:
        new_username = st.text_input("Pick a username that slays 💁‍♀️")
        new_password = st.text_input("Create a password (make it strong like your coffee) ☕", type="password")
        email = st.text_input("Drop your email (we won't spam, we're not toxic) 📧")
        
        if st.button("Sign Up ✨"):
            if register_user(new_username, new_password, email):
                st.success("You're in bestie! Login to start your financial journey! 🚀")
            else:
                st.error("Username or email already exists! Try being more original bestie! ") 