import streamlit as st
from email_classifier import (
    fetch_and_classify_emails,
    CATEGORY_PRIORITY
)
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyARiONAk_Ik7r6tshzQlGs2jcetW8xZw4M")  # Replace with your Gemini API key

# Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Set Streamlit page config
st.set_page_config(page_title="AI-Powered Email Assistant", layout="wide")
st.markdown("<h1>Welcome to the AI Email Assistant</h1>", unsafe_allow_html=True)
st.markdown('<div class="main-title">📬 AI-Powered Email Assistant</div>', unsafe_allow_html=True)

# Sidebar for credentials
with st.sidebar:
    st.header("🔐 Email Credentials")
    email_id = st.text_input("Gmail Address", placeholder="example@gmail.com", key="email_id")
    password = st.text_input("App Password", type="password", placeholder="App-specific password", key="password")
    if st.button("Fetch Today's Emails"):
        if email_id and password:
            with st.spinner("Fetching and classifying up to 50 emails..."):
                classified_emails = fetch_and_classify_emails(email_id, password)
        else:
            st.warning("Please enter both your email and app password.")
    else:
        classified_emails = None

# Function to summarize with Gemini
@st.cache_data(show_spinner=False)
def summarize_with_gemini(text):
    try:
        prompt = f"Summarize this email in 1-2 sentences:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "⚠️ Could not generate summary."

# Show emails (without body) + Gemini summary
if classified_emails:
    st.subheader("📥 Classified Emails")
    for category in CATEGORY_PRIORITY:
        emails = classified_emails.get(category, [])
        if emails:
            with st.expander(f"📂 {category} ({len(emails)} email{'s' if len(emails) != 1 else ''})", expanded=False):
                for email_data in emails:
                    with st.container():
                        st.markdown('<div class="email-card">', unsafe_allow_html=True)
                        st.markdown(f"**✉️ Subject:** {email_data['subject']}")
                        st.markdown(f"**From:** {email_data['from']}")
                        st.markdown(f"**Date:** {email_data['date']} | **Time:** {email_data['time']}")
                        st.markdown("---")
                        summary = summarize_with_gemini(email_data['body'])
                        st.markdown(f"✅ **Summary:** {summary}")
                        st.markdown('</div>', unsafe_allow_html=True)
