'''import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import streamlit as st
from datetime import datetime, timedelta

# Function to send email (using Gmail's SMTP setup)
def send_email(subject, body, from_email, to_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

# Simulating the email data (to track sent emails)
sent_emails = {}

# Function to store sent email information
def track_sent_email(email_id, subject, body):
    sent_emails[email_id] = {
        'subject': subject,
        'body': body,
        'timestamp': datetime.now()
    }

# Function to check if the email can be edited within the time window (15 minutes)
def can_edit_email(email_id):
    if email_id in sent_emails:
        send_time = sent_emails[email_id]['timestamp']
        time_window = timedelta(minutes=15)  # 15 minutes time window
        if datetime.now() - send_time <= time_window:
            return True
    return False

# Streamlit UI setup
st.set_page_config(page_title="AI-Powered Email Assistant", layout="wide")
st.title("📬 AI-Powered Email Assistant")

# Sidebar for email credentials and sending email
with st.sidebar:
    st.header("🔐 Email Credentials")
    email_id = st.text_input("Gmail Address", placeholder="example@gmail.com", key="email_id", help="Enter your Gmail address")
    password = st.text_input("App Password", type="password", placeholder="App-specific password", key="password", help="Generate an app password from Google Account settings")
    to_email = st.text_input("Recipient's Email", placeholder="recipient@example.com", help="Recipient's email address")
    subject = st.text_input("Subject", placeholder="Enter email subject")
    body = st.text_area("Body", placeholder="Enter email body", height=200)

    if st.button("Send Email"):
        if email_id and password and to_email and subject and body:
            with st.spinner("Sending email..."):
                success = send_email(subject, body, email_id, to_email, password)
                if success:
                    track_sent_email(to_email, subject, body)
                    st.success("Email sent successfully!")
                else:
                    st.error("Failed to send email.")
        else:
            st.warning("Please enter all the required details.")

# Display sent emails and allow editing if within the time window
st.subheader("Sent Emails")
for email_id, email_data in sent_emails.items():
    time_diff = datetime.now() - email_data['timestamp']
    editable = time_diff <= timedelta(minutes=15)

    st.markdown(f"**Subject**: {email_data['subject']}")
    st.markdown(f"**Body**: {email_data['body']}")
    st.markdown(f"**Sent On**: {email_data['timestamp']}")
    
    if editable:
        st.markdown("**This email can still be edited within the next 15 minutes.**")
        new_subject = st.text_input(f"Edit Subject for {email_data['subject']}", value=email_data['subject'])
        new_body = st.text_area(f"Edit Body for {email_data['subject']}", value=email_data['body'], height=200)

        if st.button(f"Resend Edited Email for {email_data['subject']}"):
            success = send_email(new_subject, new_body, email_id, to_email, password)
            if success:
                track_sent_email(to_email, new_subject, new_body)  # Update with new email data
                st.success(f"Email edited and resent: {new_subject}")
            else:
                st.error("Failed to resend the edited email.")
    else:
        st.markdown("**This email is no longer editable.**")'''



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import streamlit as st
from datetime import datetime, timedelta

# Function to send email (using Gmail's SMTP setup)
def send_email(subject, body, from_email, to_email, password, message_id=None, references=None):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if message_id:
        msg['Message-ID'] = message_id
        msg['In-Reply-To'] = message_id
        if references:
            msg['References'] = references
    
    try:
        # Debugging: Print the email content being sent
        print(f"Sending email to {to_email} with subject '{subject}'")
        
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        
        # Send email
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Email sent to {to_email} successfully.")
        return msg['Message-ID']  # Return Message-ID
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

# Function to store sent email information
sent_emails = {}

# Function to track sent email info
def track_sent_email(email_id, subject, body):
    message_id = None
    # Initially, store the message ID as None since it's the first time sending
    sent_emails[email_id] = {
        'subject': subject,
        'body': body,
        'timestamp': datetime.now(),
        'edit_count': 0,
        'message_id': message_id
    }

# Function to check if email can be edited within the time window
def can_edit_email(email_id):
    if email_id in sent_emails:
        send_time = sent_emails[email_id]['timestamp']
        time_window = timedelta(minutes=15)  # 15 minutes time window
        if datetime.now() - send_time <= time_window and sent_emails[email_id]['edit_count'] < 5:
            return True
    return False

# Streamlit UI setup
st.set_page_config(page_title="AI-Powered Email Assistant", layout="wide")
st.title("📬 AI-Powered Email Assistant")

# Sidebar for email credentials and sending email
with st.sidebar:
    st.header("🔐 Email Credentials")
    email_id = st.text_input("Gmail Address", placeholder="example@gmail.com", key="email_id", help="Enter your Gmail address")
    password = st.text_input("App Password", type="password", placeholder="App-specific password", key="password", help="Generate an app password from Google Account settings")
    to_email = st.text_input("Recipient's Email", placeholder="recipient@example.com", help="Recipient's email address")
    subject = st.text_input("Subject", placeholder="Enter email subject")
    body = st.text_area("Body", placeholder="Enter email body", height=200)

    if st.button("Send Email"):
        if email_id and password and to_email and subject and body:
            with st.spinner("Sending email..."):
                # Send the email and get the Message-ID
                message_id = send_email(subject, body, email_id, to_email, password)
                if message_id:
                    track_sent_email(to_email, subject, body)
                    sent_emails[to_email]['message_id'] = message_id  # Save Message-ID
                    st.success("Email sent successfully!")
                else:
                    st.error("Failed to send email.")
        else:
            st.warning("Please enter all the required details.")

# Display sent emails and allow editing if within the time window
st.subheader("Sent Emails")
for email_id, email_data in sent_emails.items():
    time_diff = datetime.now() - email_data['timestamp']
    editable = time_diff <= timedelta(minutes=15) and email_data['edit_count'] < 5

    st.markdown(f"**Subject**: {email_data['subject']}")
    st.markdown(f"**Body**: {email_data['body']}")
    st.markdown(f"**Sent On**: {email_data['timestamp']}")
    
    if editable:
        st.markdown("**This email can still be edited within the next 15 minutes (max 5 edits).**")
        new_subject = st.text_input(f"Edit Subject for {email_data['subject']}", value=email_data['subject'])
        new_body = st.text_area(f"Edit Body for {email_data['subject']}", value=email_data['body'], height=200)

        if st.button(f"Resend Edited Email for {email_data['subject']}"):
            # Resend with the same Message-ID to keep the thread intact
            success = send_email(new_subject, new_body, email_id, to_email, password, 
                                 message_id=email_data['message_id'], references=email_data['message_id'])
            if success:
                # Increment edit count and update with new subject and body
                sent_emails[email_id]['subject'] = new_subject
                sent_emails[email_id]['body'] = new_body
                sent_emails[email_id]['timestamp'] = datetime.now()
                sent_emails[email_id]['edit_count'] += 1  # Increment edit count
                st.success(f"Email edited and resent: {new_subject}")
            else:
                st.error("Failed to resend the edited email.")
    else:
        st.markdown("**This email is no longer editable (5 edits limit reached or time window expired).**")
