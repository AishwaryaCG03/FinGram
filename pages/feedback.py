import streamlit as st
from datetime import datetime

def feedback_form():
    if not st.session_state.logged_in:
        st.error("Bestie, you need to login first to give feedback! 🫖")
        return
    
    st.title("💅 Feedback Form")
    st.markdown("### Spill the tea on your experience bestie! ✨")
    
    with st.form("feedback_form"):
        st.subheader("How's the vibe? 🌟")
        rating = st.slider(
            "Rate your experience",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Not it, 5 = Absolutely slayed!",
            format="%d ⭐"
        )
        
        st.subheader("What's the tea? 🫖")
        feedback_text = st.text_area(
            "Tell us what you think",
            placeholder="Spill the tea bestie! What's working and what's not? 💅",
            help="Your feedback helps us serve better!",
            max_chars=500
        )
        
        st.subheader("What's next? 💭")
        feature_request = st.text_area(
            "Feature requests",
            placeholder="What features would make this app even more iconic? ✨",
            help="Help us level up!",
            max_chars=300
        )
        
        submit = st.form_submit_button("Submit Feedback Bestie! 💅")
        
        if submit:
            if feedback_text or feature_request:
                st.success("Thanks for the feedback bestie! You're literally the best! ✨")
                st.balloons()
            else:
                st.error("Bestie, give us some tea to work with! 💁‍♀️")

if __name__ == "__main__":
    feedback_form() 