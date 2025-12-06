"""
Gmail Integration Script
Automatically fetches emails from Gmail and sends them to the task extraction API.
100% FREE - Uses Gmail's built-in IMAP access.
"""

import imaplib
import email
from email.header import decode_header
import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GMAIL_USER = os.getenv('GMAIL_USER', '')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')
API_URL = os.getenv('API_URL', 'http://localhost:8000/ingest-email')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 60))  # Check every 60 seconds
IMAP_SERVER = 'imap.gmail.com'

# Track processed emails
processed_emails = set()


def connect_to_gmail():
    """Connect to Gmail using IMAP."""
    try:
        print(f"Connecting to Gmail ({GMAIL_USER})...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        print("✓ Connected to Gmail successfully!")
        return mail
    except Exception as e:
        print(f"✗ Failed to connect to Gmail: {e}")
        return None


def decode_email_subject(subject):
    """Decode email subject handling different encodings."""
    if subject is None:
        return "No Subject"
    
    decoded_parts = decode_header(subject)
    decoded_subject = ""
    
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                decoded_subject += part.decode(encoding or 'utf-8')
            except:
                decoded_subject += part.decode('utf-8', errors='ignore')
        else:
            decoded_subject += part
    
    return decoded_subject


def get_email_body(msg):
    """Extract email body from message."""
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode()
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode()
        except:
            body = str(msg.get_payload())
    
    return body.strip()


def send_to_api(subject, body, sender):
    """Send email data to the task extraction API."""
    try:
        payload = {
            "subject": subject,
            "body": body,
            "sender": sender
        }
        
        response = requests.post(API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Processed: {data.get('added', 0)} tasks added, {data.get('duplicates', 0)} duplicates")
            return True
        else:
            print(f"  ✗ API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ✗ Failed to send to API: {e}")
        return False


def process_emails(mail, folder='INBOX', filter_unread=True):
    """Process emails from specified folder."""
    try:
        # Select mailbox
        mail.select(folder)
        
        # Search for emails
        if filter_unread:
            status, messages = mail.search(None, 'UNSEEN')
        else:
            status, messages = mail.search(None, 'ALL')
        
        email_ids = messages[0].split()
        
        if not email_ids:
            return 0
        
        print(f"\nFound {len(email_ids)} new email(s) in {folder}")
        
        processed_count = 0
        
        for email_id in email_ids:
            # Skip if already processed
            if email_id in processed_emails:
                continue
            
            try:
                # Fetch email
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        # Parse email
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Extract details
                        subject = decode_email_subject(msg['subject'])
                        sender = msg['from']
                        body = get_email_body(msg)
                        
                        print(f"\n📧 Processing: {subject[:50]}...")
                        print(f"   From: {sender}")
                        
                        # Send to API
                        if send_to_api(subject, body, sender):
                            processed_count += 1
                            processed_emails.add(email_id)
                        
            except Exception as e:
                print(f"  ✗ Error processing email: {e}")
                continue
        
        return processed_count
        
    except Exception as e:
        print(f"✗ Error accessing mailbox: {e}")
        return 0


def main():
    """Main loop - continuously check for new emails."""
    print("=" * 60)
    print("Gmail Integration for Email-to-Task System")
    print("=" * 60)
    print()
    
    # Validate configuration
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("✗ Error: Gmail credentials not configured!")
        print()
        print("Please set up your credentials in .env file:")
        print("  GMAIL_USER=your.email@gmail.com")
        print("  GMAIL_APP_PASSWORD=your_app_password")
        print()
        print("See GMAIL_SETUP.md for instructions on getting an App Password")
        return
    
    print(f"Configuration:")
    print(f"  Gmail: {GMAIL_USER}")
    print(f"  API: {API_URL}")
    print(f"  Check interval: {CHECK_INTERVAL} seconds")
    print()
    
    # Connect to Gmail
    mail = connect_to_gmail()
    if not mail:
        return
    
    print()
    print("✓ Monitoring Gmail for new emails...")
    print("  Press Ctrl+C to stop")
    print()
    
    try:
        while True:
            try:
                # Process new emails
                count = process_emails(mail, folder='INBOX', filter_unread=True)
                
                if count > 0:
                    print(f"\n✓ Processed {count} email(s)")
                
                # Wait before next check
                time.sleep(CHECK_INTERVAL)
                
            except imaplib.IMAP4.abort:
                # Connection lost, reconnect
                print("\n⚠ Connection lost, reconnecting...")
                mail = connect_to_gmail()
                if not mail:
                    print("✗ Failed to reconnect. Exiting.")
                    break
                    
    except KeyboardInterrupt:
        print("\n\n✓ Stopped monitoring Gmail")
        print("=" * 60)
    
    finally:
        try:
            mail.close()
            mail.logout()
        except:
            pass


if __name__ == '__main__':
    main()
