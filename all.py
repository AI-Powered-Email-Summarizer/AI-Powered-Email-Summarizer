import streamlit as st
import imaplib
import email
from email.header import decode_header
import datetime
import pytz
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# Define categories and their priorities
CATEGORY_KEYWORDS = {
    "Work/Business": ["project", "deadline", "client", "team"],
    "E-commerce & Orders": ["order", "shipped", "delivered", "invoice"],
    "Healthcare & Medical": ["appointment", "prescription", "doctor", "lab"],
    "Education & Learning": ["course", "assignment", "exam", "grades"],
    "Finance & Banking": ["transaction", "account", "credit card", "bank"],
    "Travel & Hospitality": ["flight", "hotel", "booking", "itinerary"],
    "Technical Support": ["support", "issue", "bug", "error"],
    "Social Media Notifications": ["like", "comment", "follow", "tagged"],
    "Promotions": ["sale", "discount", "offer", "deal"],
    "Personal": ["family", "friend", "party", "wedding"]
}
CATEGORY_PRIORITY = list(CATEGORY_KEYWORDS.keys())

def get_today_date():
    return datetime.datetime.now(pytz.timezone('UTC')).date()

def extract_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode(errors="ignore")
            elif content_type == "text/html" and "attachment" not in content_disposition:
                html = part.get_payload(decode=True).decode(errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                return soup.get_text()
    else:
        content_type = msg.get_content_type()
        if content_type == "text/plain":
            return msg.get_payload(decode=True).decode(errors="ignore")
        elif content_type == "text/html":
            html = msg.get_payload(decode=True).decode(errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            return soup.get_text()
    return ""

def classify_email(subject, body):
    text = f"{subject} {body}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "Personal"

def fetch_and_classify_emails(email_user, email_pass):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(email_user, email_pass)
    imap.select("inbox")

    today = get_today_date()
    result, data = imap.search(None, "SINCE", today.strftime('%d-%b-%Y'))
    email_ids = data[0].split()

    emails = {category: [] for category in CATEGORY_PRIORITY}
    for eid in reversed(email_ids):
        result, msg_data = imap.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8', errors="ignore")
        from_ = msg.get("From")
        date = msg.get("Date")
        dt = email.utils.parsedate_to_datetime(date)
        body = extract_body(msg)
        category = classify_email(subject, body)

        if dt.date() == today:
            emails[category].append({
                "subject": subject,
                "from": from_,
                "date": dt.strftime('%Y-%m-%d'),
                "time": dt.strftime('%H:%M'),
                "body": body,
                "msg": msg
            })

    imap.logout()
    return emails

def summarize_emails(emails_by_category):
    summary = {}
    for category, emails in emails_by_category.items():
        summary[category] = f"{len(emails)} email{'s' if len(emails)!=1 else ''}"
    return summary

def send_reply(user_email, user_password, to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = "Re: " + subject
    msg["From"] = user_email
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(user_email, user_password)
    server.sendmail(user_email, to_email, msg.as_string())
    server.quit()

# ----------------- STREAMLIT UI -------------------

st.set_page_config(page_title="AI-Powered Email Assistant", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #BEE4F4; color: #000080; font-family: 'Segoe UI', sans-serif; }
    .main-title { font-size: 2.3em; color: #000080; text-align: center; margin: 20px 0; }
    .summary-dashboard { background-color: #252545; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #0078D4; }
    .summary-item strong { color: #000080; }
    .email-card { background: linear-gradient(135deg, #2E2E4A, #353564); border-radius: 8px; padding: 15px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📬 AI-Powered Email Assistant</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔐 Email Credentials")
    email_id = st.text_input("Gmail Address", placeholder="example@gmail.com")
    password = st.text_input("App Password", type="password")
    fetch_btn = st.button("Fetch & Classify Today's Emails")

if fetch_btn and email_id and password:
    with st.spinner("Fetching and classifying emails..."):
        classified_emails = fetch_and_classify_emails(email_id, password)
        summaries = summarize_emails(classified_emails)

    st.markdown('<div class="summary-dashboard">', unsafe_allow_html=True)
    st.subheader("📊 Email Summary")
    for cat, text in summaries.items():
        st.markdown(f'<div class="summary-item"><strong>{cat}</strong>: {text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("📥 Today's Emails")
    for category in CATEGORY_PRIORITY:
        emails = classified_emails.get(category, [])
        if emails:
            with st.expander(f"📂 {category} ({len(emails)})"):
                for idx, e in enumerate(emails):
                    st.markdown('<div class="email-card">', unsafe_allow_html=True)
                    st.markdown(f"**Subject:** {e['subject']}")
                    st.markdown(f"**From:** {e['from']}")
                    st.markdown(f"**Date:** {e['date']} | **Time:** {e['time']}")
                    st.markdown("---")
                    st.markdown(e['body'])

                    with st.form(key=f"reply_form_{category}_{idx}"):
                        reply = st.text_area("✍️ Your reply:", key=f"reply_text_{category}_{idx}")
                        submit = st.form_submit_button("Send Reply")
                        if submit and reply:
                            send_reply(email_id, password, e['from'], e['subject'], reply)
                            st.success("Reply sent!")
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Please enter credentials and click the button to fetch today's emails.")
