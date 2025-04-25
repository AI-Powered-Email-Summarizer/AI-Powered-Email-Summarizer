import sqlite3
from datetime import datetime, timedelta
import time

# Function to convert datetime to string
def datetime_to_str(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# Function to convert string to datetime
def str_to_datetime(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')

# Setup the SQLite database to store email content
def create_db():
    conn = sqlite3.connect('email_db.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            email_id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_email TEXT,
            to_email TEXT,
            subject TEXT,
            body TEXT,
            created_at TIMESTAMP,
            is_sent BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

# Function to save the email to the database
def save_email(from_email, to_email, subject, body):
    conn = sqlite3.connect('email_db.db')
    cursor = conn.cursor()
    
    # Insert the email details with datetime as string
    created_at = datetime_to_str(datetime.now())
    cursor.execute('''
        INSERT INTO emails (from_email, to_email, subject, body, created_at, is_sent)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (from_email, to_email, subject, body, created_at, False))
    
    conn.commit()
    email_id = cursor.lastrowid  # Get the ID of the inserted email
    conn.close()
    return email_id

# Function to update the email content in the database (if edited)
def edit_email(email_id, new_body):
    conn = sqlite3.connect('email_db.db')
    cursor = conn.cursor()
    
    # Update the email with new body and refresh the created_at timestamp
    new_created_at = datetime_to_str(datetime.now())
    cursor.execute('''
        UPDATE emails SET body = ?, created_at = ? WHERE email_id = ?
    ''', (new_body, new_created_at, email_id))
    
    conn.commit()
    conn.close()

# Function to send the email using SMTP
def send_email(subject, body, from_email, to_email, password):
    # Sending email logic remains the same as before
    pass

# Function to automatically send the email after 10 minutes
def auto_send_email(email_id, from_email, password):
    conn = sqlite3.connect('email_db.db')
    cursor = conn.cursor()
    
    # Fetch the email data from the database
    cursor.execute('''
        SELECT from_email, to_email, subject, body, created_at, is_sent 
        FROM emails WHERE email_id = ?
    ''', (email_id,))
    
    email = cursor.fetchone()
    if email:
        from_email, to_email, subject, body, created_at, is_sent = email
        if is_sent:
            print("Email already sent.")
            return
        
        # Convert the stored created_at string back to datetime
        created_at = str_to_datetime(created_at)
        
        # Check if the email is within the 10-minute window
        time_diff = datetime.now() - created_at
        if time_diff <= timedelta(minutes=10):
            # Send the email with the current content
            send_email(subject, body, from_email, to_email, password)
            
            # Mark the email as sent
            cursor.execute('''
                UPDATE emails SET is_sent = ? WHERE email_id = ?
            ''', (True, email_id))
            conn.commit()
        else:
            print("The email time window has expired.")
    
    conn.close()

# Example usage
if __name__ == "__main__":
    create_db()
    
    # Sending initial email
    from_email = "aryaidamle@gmail.com"
    to_email = "aparnajdamle@gmail.com"
    subject = "Test Email"
    body = "This is the original email content."
    password = "ifqp awne izox oxss"
    
    # Step 1: Save the email in the database
    email_id = save_email(from_email, to_email, subject, body)
    
    # Simulate a user editing the email after some time
    time.sleep(5)  # Wait for 5 seconds before editing (simulate user editing)
    
    # Step 2: Edit the email content (e.g., user wants to update the body)
    new_body = "This is the edited email content."
    edit_email(email_id, new_body)
    
    # Step 3: Automatically send the email after 10 minutes (or when time expires)
    auto_send_email(email_id, from_email, password)
