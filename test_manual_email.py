"""
Manually test email ingestion without waiting for Gmail
"""
import requests
import json

# Your test email data
email_data = {
    "subject": "AWS KIRO WEEK-2 SUBMISSION DUE - 07-12-2025 [URGENT] Testing the website",
    "body": """
    This is a test email for the task automation system.
    
    Tasks to complete:
    - Submit AWS KIRO Week-2 assignment by December 7, 2025
    - Test the email-to-task website functionality
    - Verify Gmail integration is working correctly
    """,
    "sender": "shreyasherikar18@gmail.com"
}

print("Sending test email to API...")
print(f"Subject: {email_data['subject']}")
print()

try:
    response = requests.post(
        'http://localhost:8000/ingest-email',
        json=email_data,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Success!")
        print(f"  Added: {result.get('added', 0)} tasks")
        print(f"  Duplicates: {result.get('duplicates', 0)} tasks")
        print()
        print("Tasks extracted:")
        for task in result.get('tasks', []):
            print(f"  - {task.get('description', 'N/A')[:80]}...")
            print(f"    Category: {task.get('category', 'N/A')}")
            print(f"    Priority: {task.get('priority', 'N/A')}")
            print()
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"✗ Failed: {e}")
    print()
    print("Make sure Flask server is running on port 8000!")
