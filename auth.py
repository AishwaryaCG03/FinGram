import streamlit as st
import bcrypt
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
    
    # Check if is_user_meme column exists in engagement table
    c.execute("PRAGMA table_info(engagement)")
    columns = [column[1] for column in c.fetchall()]
    if 'is_user_meme' not in columns:
        c.execute("ALTER TABLE engagement ADD COLUMN is_user_meme INTEGER DEFAULT 0")
    
    # Create user_memes table
    c.execute('''CREATE TABLE IF NOT EXISTS user_memes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  category TEXT,
                  caption TEXT,
                  image_path TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY (username) REFERENCES users(username))''')
    
    conn.commit()
    conn.close()

# Hash password using bcrypt
def hash_password(password):
    # Salt is automatically generated and embedded in the hash
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Check login credentials
def check_login(username, password):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    c.execute('SELECT password FROM users WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        stored_hash = result[0]
        # Check if the password matches the stored hash
        try:
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        except ValueError:
            # Fallback for old SHA-256 hashes if any exist during transition
            import hashlib
            old_hash = hashlib.sha256(str.encode(password)).hexdigest()
            return old_hash == stored_hash
            
    return False

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
def save_engagement(username, meme_category, meme_index, engagement_type, comment_text=None, is_user_meme=0):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO engagement 
                 (username, meme_category, meme_index, engagement_type, comment_text, is_user_meme)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (username, meme_category, meme_index, engagement_type, comment_text, is_user_meme))
    
    conn.commit()
    conn.close()

# Get engagement counts
def get_engagement_counts(meme_category, meme_index, is_user_meme=0):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    likes = c.execute('''SELECT COUNT(*) FROM engagement 
                        WHERE meme_category=? AND meme_index=? AND engagement_type='like' AND is_user_meme=? ''',
                     (meme_category, meme_index, is_user_meme)).fetchone()[0]
    
    comments = c.execute('''SELECT COUNT(*) FROM engagement 
                           WHERE meme_category=? AND meme_index=? AND engagement_type='comment' AND is_user_meme=? ''',
                        (meme_category, meme_index, is_user_meme)).fetchone()[0]
    
    shares = c.execute('''SELECT COUNT(*) FROM engagement 
                         WHERE meme_category=? AND meme_index=? AND engagement_type='share' AND is_user_meme=? ''',
                      (meme_category, meme_index, is_user_meme)).fetchone()[0]
    
    conn.close()
    return likes, comments, shares

# Get comments for a meme
def get_comments(meme_category, meme_index, is_user_meme=0):
    conn = sqlite3.connect('genz_finance.db')
    c = conn.cursor()
    
    comments = c.execute('''SELECT username, comment_text FROM engagement 
                           WHERE meme_category=? AND meme_index=? AND engagement_type='comment' AND is_user_meme=?
                           ORDER BY id DESC''',
                        (meme_category, meme_index, is_user_meme)).fetchall()
    
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
    st.markdown("### Secure the bag by logging in first! ")
    
    tab1, tab2 = st.tabs(["Login 🔑", "Sign Up 📝"])
    
    with tab1:
        username = st.text_input("Username (share the vibes) ☕")
        password = st.text_input("Password (keep it secret) 🤫", type="password")
        
        if st.button("Login "):
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Welcome back! Time to get that bread! 🍞")
                st.rerun()
            else:
                st.error("Wrong credentials! Try again! 😭")
    
    with tab2:
        new_username = st.text_input("Pick a username that's iconic 🔥")
        new_password = st.text_input("Create a password (make it strong like your coffee) ☕", type="password")
        email = st.text_input("Drop your email (we won't spam, we're not toxic) 📧")
        
        if st.button("Sign Up ✨"):
            if register_user(new_username, new_password, email):
                st.success("You're in! Login to start your financial journey! 🚀")
            else:
                st.error("Username or email already exists! Try being more original! 🧐") 