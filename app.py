'''import streamlit as st
from email_classifier import fetch_and_classify_emails, CATEGORY_PRIORITY, summarize_emails

st.set_page_config(page_title="AI-Powered Email Assistant", layout="wide")
st.title("📬 AI-Powered Email Assistant")

# Input for email credentials
email_id = st.text_input("Enter your Gmail address")
password = st.text_input("Enter your app password (not Gmail password)", type="password")

# Fetch & display emails
if st.button("Fetch Today's Emails"):
    if email_id and password:
        with st.spinner("Fetching and classifying emails..."):
            classified_emails = fetch_and_classify_emails(email_id, password)

        for category in CATEGORY_PRIORITY:
            emails = classified_emails.get(category, [])
            if emails:
                st.subheader(f"📂 {category} ({len(emails)} email{'s' if len(emails) != 1 else ''})")
                for email_data in emails:
                    with st.expander(f"✉️ {email_data['subject']}"):
                        st.markdown(f"**From:** {email_data['from']}")
                        st.markdown(f"**Date:** {email_data['date']}")
                        st.markdown(f"**Time:** {email_data['time']}")
                        st.markdown("---")
                        st.markdown(email_data['body'])
    else:
        st.warning("Please enter both your email and app password.")'''


import streamlit as st
from email_classifier import get_today_date, extract_body, classify_email, fetch_and_classify_emails, CATEGORY_PRIORITY, summarize_emails

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="AI-Powered Email Assistant", layout="wide")

# Custom CSS for new frontend design
st.markdown("""
    <style>
    /* General styling */
    .stApp {
        background-color: #1E1E2F;
        color: #E0E0E0;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        font-size: 2.3em;
        color: #00D4B4;
        text-align: center;
        margin: 20px 0;
        text-shadow: 0 0 10px rgba(0, 212, 180, 0.5);
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #252545;
        padding: 20px;
    }
    .stTextInput > div > div > input {
        background-color: #2E2E4A;
        color: #E0E0E0;
        border: 1px solid #00D4B4;
        border-radius: 5px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00D4B4, #0078D4);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        width: 100%;
        font-weight: bold;
    }
    /* Email card styling */
    .email-card {
        background: linear-gradient(135deg, #2E2E4A, #353564);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .email-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 212, 180, 0.3);
    }
    /* Category expander */
    .stExpander {
        background-color: #252545;
        border: 1px solid #00D4B4;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .stExpander > div > div {
        color: #00D4B4;
        font-size: 1.4em;
        font-weight: bold;
    }
    /* Summary dashboard */
    .summary-dashboard {
        background-color: #252545;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #0078D4;
    }
    .summary-item {
        color: #E0E0E0;
        font-size: 0.95em;
        margin: 5px 0;
    }
    .summary-item strong {
        color: #00D4B4;
    }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown('<div class="main-title">📬 AI-Powered Email Assistant</div>', unsafe_allow_html=True)

# Sidebar for input credentials
with st.sidebar:
    st.header("🔐 Email Credentials")
    email_id = st.text_input("Gmail Address", placeholder="example@gmail.com", key="email_id", help="Enter your Gmail address")
    password = st.text_input("App Password", type="password", placeholder="App-specific password", key="password", help="Generate an app password from Google Account settings")
    if st.button("Fetch Today's Emails"):
        if email_id and password:
            with st.spinner("Fetching and classifying emails..."):
                classified_emails = fetch_and_classify_emails(email_id, password)
        else:
            st.warning("Please enter both your email and app password.")
    else:
        classified_emails = None

# Main content: Display emails and summaries
if classified_emails:
    # Summary dashboard
    st.markdown('<div class="summary-dashboard">', unsafe_allow_html=True)
    st.subheader("📊 Email Summary")
    summaries = summarize_emails(classified_emails)
    for category, summary in summaries.items():
        st.markdown(f'<div class="summary-item"><strong>{category}</strong>: {summary}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Classified emails
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
                        st.markdown(email_data['body'])
                        st.markdown('</div>', unsafe_allow_html=True)
