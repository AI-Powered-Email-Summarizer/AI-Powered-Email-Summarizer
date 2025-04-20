import streamlit as st
from fetch_emails import get_unread_emails
from classify_email import classify_email
from summarize_email import summarize_email
from generate_reply import generate_ai_response
from send_email import send_email

st.set_page_config(layout="wide")
st.sidebar.title("📧 Options")
option = st.sidebar.radio("Choose an option", ["Classify", "Summarize", "Auto-reply"])

email_list = get_unread_emails()
email_subjects = [f"{email['sender']} - {email['subject']}" for email in email_list]
selected_index = st.selectbox("Select an unread email:", range(len(email_subjects)), format_func=lambda x: email_subjects[x])

if selected_index is not None:
    selected_email = email_list[selected_index]
    st.subheader("Selected Email")
    st.write(f"**From:** {selected_email['sender']}")
    st.write(f"**Subject:** {selected_email['subject']}")

    if option == "Classify":
        if st.button("Classify Email"):
            classification = classify_email(selected_email["subject"])
            st.success(f"📌 Email Category: **{classification}**")

    elif option == "Summarize":
        if st.button("Summarize Email"):
            summary = summarize_email(selected_email["subject"])
            st.info(f"📌 Email Summary: {summary}")

    elif option == "Auto-reply":
        if "reply_content" not in st.session_state:
            st.session_state["reply_content"] = ""

        if st.button("Generate Reply"):
            st.session_state["reply_content"] = generate_ai_response(selected_email["subject"])

        reply_content = st.text_area("Generated Reply:", st.session_state["reply_content"], height=150)

        if st.button("Send Reply"):
            sender = "your_email@gmail.com"
            to = selected_email["sender"]
            subject = f"Re: {selected_email['subject']}"

            status = send_email(sender, to, subject, reply_content)
            st.success(status)

        if st.button("Don't Send"):
            st.warning("Reply not sent.")

else:
    st.warning("No unread emails found!")
