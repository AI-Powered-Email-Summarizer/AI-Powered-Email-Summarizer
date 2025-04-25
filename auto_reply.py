import imaplib
import smtplib
import email
from email.message import EmailMessage
from email.header import decode_header
from datetime import datetime
import re

EMAIL = "aryaidamle@gmail.com"
PASSWORD = "ifqp awne izox oxss"

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

REPLY_KEYWORDS = ["help", "urgent", "issue", "problem", "support", "question"]
BLACKLIST_SENDERS = ["noreply", "do-not-reply", "news", "mailer", "no-reply", "notification", "updates"]

def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ["angry", "upset", "frustrated", "disappointed"]):
        return "angry"
    elif any(word in text for word in ["thank", "appreciate", "grateful"]):
        return "grateful"
    elif any(word in text for word in ["confused", "help", "how do i", "stuck"]):
        return "confused"
    else:
        return "neutral"

def generate_auto_reply(emotion):
    if emotion == "angry":
        return "We’re truly sorry to hear that you’re upset. Our team is looking into this and will get back to you shortly."
    elif emotion == "grateful":
        return "You're very welcome! We’re glad we could help. Let us know if there's anything else we can do."
    elif emotion == "confused":
        return "Thanks for reaching out. We’ll guide you as soon as possible. Hang tight!"
    else:
        return "Thanks for your message. Our support team will respond to you shortly."

def send_reply(to_email, subject, reply_message):
    msg = EmailMessage()
    msg["Subject"] = f"Re: {subject}"
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg.set_content(reply_message)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)
        print(f"✅ Replied to: {to_email}")

def is_blacklisted(sender_email):
    return any(bad in sender_email.lower() for bad in BLACKLIST_SENDERS)

def contains_keywords(text):
    text = text.lower()
    return any(keyword in text for keyword in REPLY_KEYWORDS)

def is_email_from_today(email_date):
    try:
        parsed_date = datetime.strptime(email_date[:31], '%a, %d %b %Y %H:%M:%S %z')
        return parsed_date.date() == datetime.now().date()
    except Exception as e:
        print("⚠️ Could not parse date:", email_date)
        return False

def auto_reply_today_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    result, data = mail.search(None, 'ALL')
    mail_ids = data[0].split()

    today_replied_count = 0

    for mail_id in reversed(mail_ids):  # Latest emails first
        result, msg_data = mail.fetch(mail_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode(errors="ignore")

        from_email = email.utils.parseaddr(msg.get("From"))[1]

        email_date = msg.get("Date")
        if not is_email_from_today(email_date):
            print(f"📅 Stopped: Email from {from_email} is not from today.")
            break  # ⛔ Stop the script here once today's emails are done

        if is_blacklisted(from_email):
            print(f"🚫 Skipped (blacklisted): {from_email}")
            continue

        # Extract body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                    try:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
                    except:
                        continue
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        combined_text = f"{subject} {body}".lower()

        if not contains_keywords(combined_text):
            print(f"📭 Skipped (no keywords): {from_email}")
            continue

        emotion = detect_emotion(combined_text)
        reply_msg = generate_auto_reply(emotion)

        send_reply(from_email, subject, reply_msg)
        today_replied_count += 1

    mail.logout()
    print(f"\n🔚 Finished. Total replies sent today: {today_replied_count}")

if __name__ == "__main__":
    auto_reply_today_emails()
