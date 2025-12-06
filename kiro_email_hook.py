"""
Kiro Hook for Email Processing
Automatically triggers when email arrives and sends to ingestion endpoint.
"""

import sys
import json
import requests
from typing import Dict, Optional


def validate_email_payload(payload: Dict) -> bool:
    """
    Ensure required fields are present: subject, body, sender.
    Returns True if valid, False otherwise.
    """
    required_fields = ['subject', 'body', 'sender']
    
    for field in required_fields:
        if field not in payload:
            print(f"Error: Missing required field '{field}' in email payload")
            return False
        
        if not payload[field] or not isinstance(payload[field], str):
            print(f"Error: Field '{field}' must be a non-empty string")
            return False
    
    return True


def send_to_ingestion_endpoint(payload: Dict, endpoint_url: str = "http://localhost:8000/ingest-email") -> Optional[Dict]:
    """
    POST email payload to Flask ingestion endpoint.
    Returns response data if successful, None otherwise.
    """
    try:
        print(f"Sending email to ingestion endpoint: {endpoint_url}")
        print(f"Subject: {payload['subject']}")
        print(f"Sender: {payload['sender']}")
        
        response = requests.post(
            endpoint_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success: {data.get('message', 'Email processed')}")
            print(f"  Tasks added: {data.get('added', 0)}")
            print(f"  Duplicates: {data.get('duplicates', 0)}")
            return data
        else:
            print(f"✗ Error: Server returned status {response.status_code}")
            print(f"  Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to Flask server")
        print("  Make sure the server is running on port 8000")
        return None
    except requests.exceptions.Timeout:
        print("✗ Error: Request timed out")
        return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None


def on_email_received(email_payload: Dict) -> bool:
    """
    Main hook entry point.
    Validates payload and triggers ingestion.
    Returns True if successful, False otherwise.
    """
    print("=" * 60)
    print("Kiro Email Hook Triggered")
    print("=" * 60)
    
    # Validate payload
    if not validate_email_payload(email_payload):
        print("✗ Validation failed")
        return False
    
    print("✓ Payload validated")
    
    # Send to ingestion endpoint
    result = send_to_ingestion_endpoint(email_payload)
    
    if result:
        print("✓ Email processing complete")
        return True
    else:
        print("✗ Email processing failed")
        return False


def main():
    """
    CLI entry point for testing the hook.
    Accepts JSON payload from stdin or command line argument.
    """
    if len(sys.argv) > 1:
        # Read from command line argument
        try:
            payload = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("Error: Invalid JSON in command line argument")
            sys.exit(1)
    else:
        # Read from stdin
        print("Reading email payload from stdin...")
        try:
            payload = json.load(sys.stdin)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in stdin")
            sys.exit(1)
    
    # Process email
    success = on_email_received(payload)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
