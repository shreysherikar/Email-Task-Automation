"""
Task Extractor Module
Uses LLM to extract actionable tasks from email content with categorization and metadata.
"""

import os
import json
import re
from typing import List, Dict, Optional
from datetime import datetime
from dateutil import parser as date_parser

# Make OpenAI optional - system works with fallback if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None


class TaskExtractor:
    """Extracts and classifies tasks from email content using LLM."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize the task extractor with OpenAI API."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("LLM_MODEL", "gpt-4")
        
        if not OPENAI_AVAILABLE:
            print("Info: OpenAI library not installed. Using fallback extraction mode.")
            print("      To enable LLM extraction: pip install openai")
            self.client = None
        elif not self.api_key:
            print("Warning: No OpenAI API key found. Using fallback extraction mode.")
            print("         Set OPENAI_API_KEY in .env file to enable LLM extraction.")
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("✓ OpenAI client initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")
                print("         Using fallback extraction mode instead.")
                self.client = None
    
    def extract_tasks_from_email(self, subject: str, body: str, sender: str) -> List[Dict]:
        """
        Main extraction method.
        Returns list of task dictionaries with all metadata.
        """
        # Build prompt for LLM
        prompt = self.build_extraction_prompt(subject, body)
        
        # Get LLM response
        try:
            if self.client is None:
                # Fallback: basic keyword extraction if no API key
                return self._fallback_extraction(subject, body, sender)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts actionable tasks from emails. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            llm_output = response.choices[0].message.content
            
            # Parse LLM response
            tasks = self.parse_llm_response(llm_output)
            
            # Enrich tasks with metadata
            enriched_tasks = []
            for task in tasks:
                enriched_task = self._enrich_task(task, subject, sender)
                enriched_tasks.append(enriched_task)
            
            return enriched_tasks
            
        except Exception as e:
            print(f"Error during LLM extraction: {e}")
            # Fallback to basic extraction
            return self._fallback_extraction(subject, body, sender)
    
    def build_extraction_prompt(self, subject: str, body: str) -> str:
        """Construct LLM prompt with instructions for task extraction."""
        prompt = f"""Extract all actionable tasks from the following email. For each task, provide:
- description: Clear description of what needs to be done
- category: One of [Work, Personal, Academic, Urgent, Low Priority]
- priority: One of [High, Medium, Low]
- due_date: Extract any mentioned dates in YYYY-MM-DD format, or null if none

Email Subject: {subject}

Email Body:
{body}

Respond ONLY with a JSON array of tasks in this exact format:
[
  {{
    "description": "task description",
    "category": "Work",
    "priority": "High",
    "due_date": "2025-12-10"
  }}
]

If no actionable tasks are found, return an empty array: []
"""
        return prompt
    
    def parse_llm_response(self, response: str) -> List[Dict]:
        """Parse LLM JSON response into structured task objects."""
        try:
            # Try to extract JSON from response
            # Sometimes LLM adds extra text, so we look for JSON array
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                tasks = json.loads(json_str)
                return tasks if isinstance(tasks, list) else []
            else:
                # Try parsing the whole response
                tasks = json.loads(response)
                return tasks if isinstance(tasks, list) else []
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Response was: {response[:200]}...")
            return []
    
    def _enrich_task(self, task: Dict, email_subject: str, sender: str) -> Dict:
        """Add additional metadata and validate task fields."""
        # Ensure required fields
        enriched = {
            "description": task.get("description", ""),
            "category": self.classify_category(task.get("description", ""), task.get("category")),
            "priority": task.get("priority", "Medium"),
            "due_date": task.get("due_date"),
            "sender": sender,
            "status": "pending",
            "source_email": {
                "subject": email_subject,
                "received_at": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        # Extract due date if not provided
        if not enriched["due_date"]:
            enriched["due_date"] = self.extract_due_date(enriched["description"])
        
        # Determine priority if not set properly
        enriched["priority"] = self.determine_priority(
            enriched["description"], 
            enriched["category"]
        )
        
        return enriched
    
    def classify_category(self, task_text: str, suggested_category: Optional[str] = None) -> str:
        """
        Determine category: Work, Personal, Academic, Urgent, Low Priority.
        Check for urgency indicators first.
        """
        task_lower = task_text.lower()
        
        # Check for urgency indicators (takes precedence)
        urgency_keywords = ['urgent', 'asap', 'critical', 'emergency', 'immediately', 'now']
        if any(keyword in task_lower for keyword in urgency_keywords):
            return "Urgent"
        
        # Use suggested category if valid
        valid_categories = ["Work", "Personal", "Academic", "Urgent", "Low Priority"]
        if suggested_category in valid_categories:
            return suggested_category
        
        # Fallback: keyword-based classification
        if any(word in task_lower for word in ['meeting', 'report', 'project', 'client', 'presentation', 'deadline']):
            return "Work"
        elif any(word in task_lower for word in ['research', 'paper', 'study', 'assignment', 'thesis', 'course']):
            return "Academic"
        elif any(word in task_lower for word in ['family', 'personal', 'home', 'grocery', 'appointment']):
            return "Personal"
        elif any(word in task_lower for word in ['later', 'sometime', 'eventually', 'when possible']):
            return "Low Priority"
        else:
            return "Work"  # Default
    
    def extract_due_date(self, task_text: str) -> Optional[str]:
        """Extract and normalize due date from task text."""
        try:
            # Common date patterns
            date_patterns = [
                r'by (\w+ \d+)',
                r'due (\w+ \d+)',
                r'on (\w+ \d+)',
                r'(\d{4}-\d{2}-\d{2})',
                r'(\d{1,2}/\d{1,2}/\d{4})',
                r'(tomorrow|today|next week|next month)'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, task_text, re.IGNORECASE)
                if match:
                    date_str = match.group(1)
                    # Try to parse the date
                    try:
                        parsed_date = date_parser.parse(date_str, fuzzy=True)
                        return parsed_date.strftime("%Y-%m-%d")
                    except:
                        continue
            
            return None
        except Exception as e:
            print(f"Error extracting due date: {e}")
            return None
    
    def determine_priority(self, task_text: str, category: str) -> str:
        """Determine priority level: High, Medium, Low."""
        task_lower = task_text.lower()
        
        # High priority indicators
        high_priority_keywords = ['urgent', 'asap', 'critical', 'important', 'priority', 'immediately']
        if any(keyword in task_lower for keyword in high_priority_keywords):
            return "High"
        
        # Urgent category always gets high priority
        if category == "Urgent":
            return "High"
        
        # Low priority indicators
        low_priority_keywords = ['later', 'sometime', 'eventually', 'when possible', 'optional']
        if any(keyword in task_lower for keyword in low_priority_keywords):
            return "Low"
        
        # Default to medium
        return "Medium"
    
    def _fallback_extraction(self, subject: str, body: str, sender: str) -> List[Dict]:
        """
        Basic keyword-based extraction when LLM is unavailable.
        Looks for action verbs and creates simple tasks.
        """
        print("Using fallback extraction (no LLM)")
        
        # Combine subject and body
        text = f"{subject}\n{body}"
        
        # Look for sentences with action verbs
        action_verbs = ['complete', 'finish', 'submit', 'prepare', 'review', 'send', 'create', 
                       'update', 'fix', 'schedule', 'call', 'email', 'meet', 'discuss']
        
        tasks = []
        sentences = text.split('.')
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(verb in sentence.lower() for verb in action_verbs) and len(sentence) > 10:
                task = {
                    "description": sentence,
                    "category": self.classify_category(sentence),
                    "priority": self.determine_priority(sentence, ""),
                    "due_date": self.extract_due_date(sentence),
                    "sender": sender,
                    "status": "pending",
                    "source_email": {
                        "subject": subject,
                        "received_at": datetime.utcnow().isoformat() + "Z"
                    }
                }
                tasks.append(task)
        
        return tasks[:5]  # Limit to 5 tasks in fallback mode


# Convenience function
def extract_tasks(subject: str, body: str, sender: str, api_key: Optional[str] = None) -> List[Dict]:
    """Extract tasks from email using default extractor."""
    extractor = TaskExtractor(api_key=api_key)
    return extractor.extract_tasks_from_email(subject, body, sender)
