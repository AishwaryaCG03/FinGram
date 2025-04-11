import streamlit as st
import random
from auth import save_engagement, get_engagement_counts, get_comments
import urllib.parse

def get_social_share_links(caption, hashtags=None):
    if hashtags is None:
        hashtags = ["FinTok", "MoneyMoves", "RichGirlEra", "FinanceCheck"]
    
    # Encode the caption and hashtags for URLs
    encoded_caption = urllib.parse.quote(caption)
    encoded_hashtags = urllib.parse.quote(" ".join(f"#{tag}" for tag in hashtags))
    
    # Create sharing links for different platforms
    whatsapp_link = f"https://api.whatsapp.com/send?text={encoded_caption}%20{encoded_hashtags}"
    twitter_link = f"https://twitter.com/intent/tweet?text={encoded_caption}&hashtags={','.join(hashtags)}"
    linkedin_link = f"https://www.linkedin.com/sharing/share-offsite/?url=https://fingram.com&title={encoded_caption}"
    instagram_story_link = "instagram://story-camera"  # Opens Instagram story camera
    
    return {
        "WhatsApp": whatsapp_link,
        "Twitter": twitter_link,
        "LinkedIn": linkedin_link,
        "Instagram": instagram_story_link
    }

def meme_gallery():
    if not st.session_state.logged_in:
        st.error("Bestie, you need to login first to see the tea! 🫖")
        return
    
    st.title("💅 Financial Memes That Hit Different")
    st.markdown("### Because learning about money doesn't have to give boring vibes")
    
    # Meme categories with captions
    meme_categories = {
        "Savings": [
            "Me looking at my bank account after saying 'treat yourself' too many times 👀",
            "My savings account watching me buy another iced coffee ☕",
            "That moment when your emergency fund is looking thicker than your ex 💅"
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
                    eng_col1, eng_col2, eng_col3, eng_col4 = st.columns(4)
                    
                    with eng_col1:
                        if st.button(f"❤️ {likes}", key=f"like_{category}_{i}"):
                            save_engagement(st.session_state.username, category, i, "like")
                            st.rerun()
                    
                    with eng_col2:
                        if st.button(f"💬 {comments_count}", key=f"comment_btn_{category}_{i}"):
                            st.session_state[f"show_comments_{category}_{i}"] = True
                    
                    with eng_col3:
                        # Share dropdown
                        share_links = get_social_share_links(caption)
                        share_platform = st.selectbox(
                            "Share on",
                            ["Share 🔄"] + list(share_links.keys()),
                            key=f"share_select_{category}_{i}"
                        )
                        
                        if share_platform != "Share 🔄":
                            st.markdown(f"[Share on {share_platform}]({share_links[share_platform]})")
                            save_engagement(st.session_state.username, category, i, "share")
                            st.success(f"Opening {share_platform} to share! 🔥")
                    
                    # Comments section
                    if st.session_state.get(f"show_comments_{category}_{i}", False):
                        with st.expander("💭 Comments", expanded=True):
                            comment = st.text_input("Drop your thoughts bestie 💅", key=f"comment_input_{category}_{i}")
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
        meme_caption = st.text_input("Meme Caption (Make it viral) ✨")
    with col2:
        uploaded_file = st.file_uploader("Drop Your Meme Here 🔥", type=["jpg", "png", "gif"])
    
    if st.button("Submit That Heat 🚀"):
        if meme_caption and uploaded_file:
            st.success("Meme submitted! You're basically a content creator now 💅")
            
            # Show sharing options for the uploaded meme
            st.subheader("Share Your Creation 🚀")
            share_links = get_social_share_links(meme_caption)
            share_cols = st.columns(len(share_links))
            
            for col, (platform, link) in zip(share_cols, share_links.items()):
                with col:
                    st.markdown(f"[Share on {platform}]({link})")

    # Trending hashtags
    st.markdown("---")
    st.markdown("""
    ### Trending Hashtags 🔥
    #FinTok #MoneyMoves #RichGirlEra #InvestingCheck #SavingsGoals #BudgetingCheck
    """)

if __name__ == "__main__":
    meme_gallery() 