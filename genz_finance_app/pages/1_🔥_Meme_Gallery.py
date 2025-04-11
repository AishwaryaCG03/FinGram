import streamlit as st
import random
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from auth import save_engagement, get_engagement_counts, get_comments

st.set_page_config(
    page_title="Meme Gallery | FinGram",
    page_icon="🔥",
    layout="wide"
)

# Check login status
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Bestie, you need to login first to see the tea! 🫖")
    st.stop()

st.title(" Financial Memes That Hit Different")
st.markdown("### Because learning about money doesn't have to give boring vibes")

# Meme categories with captions
meme_categories = {
    "Savings": [
        "Me looking at my bank account after saying 'treat yourself' too many times 👀",
        "My savings account watching me buy another iced coffee ☕",
        "That moment when your emergency fund is looking thicker than your ex "
    ],
    "Investing": [
        "Stock market be like: 📈📉 and I be like: 🙃",
        "Me pretending to understand crypto while buying the dip 🤡",
        "When someone says they're investing in their 401k: 'It's giving responsible' ✨"
    ],
    "Budgeting": [
        "My budget: exists\nMe: I pretend I do not see it 👩‍🦯",
        "When you make a budget but forget about existing ✌️",
        "That moment when you realize adulting requires actual money management 😭"
    ]
}

# Create tabs for different meme categories
tabs = st.tabs(list(meme_categories.keys()))

for tab, (category, captions) in zip(tabs, meme_categories.items()):
    with tab:
        st.header(f"{category} Memes 🔥")
        
        # Create a 2-column layout for memes
        cols = st.columns(2)
        for i, caption in enumerate(captions):
            with cols[i % 2]:
                st.markdown(f"### {caption}")
                # Here you would normally display an image
                st.markdown("*[Meme placeholder - Add your spicy memes here]*")
                
                # Get current engagement counts
                likes, comments_count, shares = get_engagement_counts(category, i)
                
                # Engagement section
                eng_col1, eng_col2, eng_col3 = st.columns(3)
                
                with eng_col1:
                    if st.button(f"❤️ {likes}", key=f"like_{category}_{i}"):
                        save_engagement(st.session_state.username, category, i, "like")
                        st.rerun()
                
                with eng_col2:
                    if st.button(f"💬 {comments_count}", key=f"comment_btn_{category}_{i}"):
                        st.session_state[f"show_comments_{category}_{i}"] = True
                
                with eng_col3:
                    if st.button(f"🔄 {shares}", key=f"share_{category}_{i}"):
                        save_engagement(st.session_state.username, category, i, "share")
                        st.success("Shared with your besties! 🔥")
                        st.rerun()
                
                # Comments section
                if st.session_state.get(f"show_comments_{category}_{i}", False):
                    with st.expander("💭 Comments", expanded=True):
                        comment = st.text_input("Drop your thoughts bestie !!", key=f"comment_input_{category}_{i}")
                        if st.button("Post 🚀", key=f"post_comment_{category}_{i}"):
                            save_engagement(st.session_state.username, category, i, "comment", comment)
                            st.success("Comment posted! You're slaying! ✨")
                            st.rerun()
                        
                        # Display existing comments
                        comments = get_comments(category, i)
                        for username, comment_text in comments:
                            st.markdown(f"**{username}**: {comment_text}")

# Add a meme submission section
st.markdown("---")
st.header("📤 Submit Your Financial Meme")
st.markdown("Because your meme game is probably stronger than your investment portfolio (jk bestie)")

col1, col2 = st.columns(2)
with col1:
    st.text_input("Meme Caption (Make it viral) ✨")
with col2:
    st.file_uploader("Drop Your Meme Here 🔥", type=["jpg", "png", "gif"])

if st.button("Submit That Heat 🚀"):
    st.success("Meme submitted! You're basically a content creator now ")

# Trending hashtags
st.markdown("---")
st.markdown("""
### Trending Hashtags 🔥
#FinTok #MoneyMoves #RichGirlEra #InvestingCheck #SavingsGoals #BudgetingCheck
""") 