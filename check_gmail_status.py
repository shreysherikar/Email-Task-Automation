"""
Quick diagnostic script to check Gmail integration status
"""
import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv('GMAIL_USER', '')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')

print("=" * 60)
print("Gmail Integration Status Check")
print("=" * 60)
print()

# Check credentials
print("1. Checking credentials...")
if GMAIL_USER and GMAIL_APP_PASSWORD:
    print(f"   ✓ Gmail: {GMAIL_USER}")
    print(f"   ✓ App Password: {'*' * len(GMAIL_APP_PASSWORD)}")
else:
    print("   ✗ Missing credentials in .env file")
    exit(1)

# Try to connect
print()
print("2. Connecting to Gmail...")
try:
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    print("   ✓ Connected successfully!")
    
    # Check inbox
    print()
    print("3. Checking INBOX...")
    mail.select('INBOX')
    
    # Count unread emails
    status, unread = mail.search(None, 'UNSEEN')
    unread_count = len(unread[0].split()) if unread[0] else 0
    
    # Count all emails
    status, all_emails = mail.search(None, 'ALL')
    total_count = len(all_emails[0].split()) if all_emails[0] else 0
    
    print(f"   ✓ Total emails: {total_count}")
    print(f"   ✓ Unread emails: {unread_count}")
    
    if unread_count > 0:
        print()
        print(f"   📧 {unread_count} unread email(s) ready to process!")
        print("   → The Gmail integration script will process these on next check")
    else:
        print()
        print("   ℹ No unread emails found")
        print("   → Mark your test email as UNREAD in Gmail to process it")
    
    mail.close()
    mail.logout()
    
except Exception as e:
    print(f"   ✗ Connection failed: {e}")
    exit(1)

print()
print("=" * 60)
print("Status: All systems operational ✓")
print("=" * 60)
