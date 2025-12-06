"""
Task Store Module
Handles file-based JSON storage for tasks with duplicate detection and CRUD operations.
"""

import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import shutil


class TaskStore:
    """Manages task persistence in JSON format."""
    
    def __init__(self, file_path: str = "data/tasks.json"):
        """Initialize the task store with specified file path."""
        self.file_path = file_path
        self.backup_path = f"{file_path}.backup"
        self.initialize_store()
    
    def initialize_store(self) -> None:
        """Create JSON file if it doesn't exist, with empty structure and sample data."""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            # Initialize with empty task list
            initial_data = {
                "tasks": [],
                "metadata": {
                    "last_updated": datetime.utcnow().isoformat() + "Z",
                    "total_tasks": 0
                }
            }
            self._write_json(initial_data)
            print(f"Initialized empty task store at {self.file_path}")
    
    def seed_sample_tasks(self) -> List[Dict]:
        """Create sample tasks with varied categories, priorities, and senders."""
        sample_tasks = [
            {
                "id": self.generate_task_id(),
                "description": "Complete Q4 financial report and submit to board",
                "category": "Work",
                "priority": "High",
                "due_date": "2025-12-15",
                "sender": "cfo@company.com",
                "status": "pending",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "source_email": {
                    "subject": "Q4 Report Due",
                    "received_at": datetime.utcnow().isoformat() + "Z"
                }
            },
            {
                "id": self.generate_task_id(),
                "description": "Review and approve team vacation requests for December",
                "category": "Work",
                "priority": "Medium",
                "due_date": "2025-12-10",
                "sender": "hr@company.com",
                "status": "pending",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "source_email": {
                    "subject": "Vacation Approvals Needed",
                    "received_at": datetime.utcnow().isoformat() + "Z"
                }
            },
            {
                "id": self.generate_task_id(),
                "description": "URGENT: Fix production server outage affecting customers",
                "category": "Urgent",
                "priority": "High",
                "due_date": "2025-12-06",
                "sender": "ops@company.com",
                "status": "pending",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "source_email": {
                    "subject": "CRITICAL: Production Down",
                    "received_at": datetime.utcnow().isoformat() + "Z"
                }
            },
            {
                "id": self.generate_task_id(),
                "description": "Buy groceries and prepare dinner for family gathering",
                "category": "Personal",
                "priority": "Medium",
                "due_date": "2025-12-08",
                "sender": "family@personal.com",
                "status": "pending",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "source_email": {
                    "subject": "Weekend Plans",
                    "received_at": datetime.utcnow().isoformat() + "Z"
                }
            },
            {
                "id": self.generate_task_id(),
                "description": "Submit research paper draft to advisor for feedback",
                "category": "Academic",
                "priority": "High",
                "due_date": "2025-12-12",
                "sender": "advisor@university.edu",
                "status": "pending",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "source_email": {
                    "subject": "Paper Deadline Reminder",
                    "received_at": datetime.utcnow().isoformat() + "Z"
                }
            },
            {
                "id": self.generate_task_id(),
                "description": "Schedule dentist appointment for annual checkup",
                "category": "Low Priority",
                "priority": "Low",
                "due_date": None,
                "sender": "dentist@clinic.com",
                "status": "pending",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "source_email": {
                    "subject": "Time for Your Checkup",
                    "received_at": datetime.utcnow().isoformat() + "Z"
                }
            },
            {
                "id": self.generate_task_id(),
                "description": "Prepare presentation slides for client meeting next week",
                "category": "Work",
                "priority": "High",
                "due_date": "2025-12-13",
                "sender": "manager@company.com",
                "status": "done",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "source_email": {
                    "subject": "Client Meeting Prep",
                    "received_at": datetime.utcnow().isoformat() + "Z"
                }
            }
        ]
        return sample_tasks
    
    def load_tasks(self) -> List[Dict]:
        """Read and parse tasks from JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("tasks", [])
        except FileNotFoundError:
            print(f"Task file not found at {self.file_path}, initializing...")
            self.initialize_store()
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            # Attempt recovery from backup
            if os.path.exists(self.backup_path):
                print("Attempting to recover from backup...")
                shutil.copy(self.backup_path, self.file_path)
                return self.load_tasks()
            return []
    
    def save_tasks(self, tasks: List[Dict]) -> None:
        """Write tasks to JSON file with proper formatting."""
        # Create backup before writing
        if os.path.exists(self.file_path):
            shutil.copy(self.file_path, self.backup_path)
        
        data = {
            "tasks": tasks,
            "metadata": {
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "total_tasks": len(tasks)
            }
        }
        self._write_json(data)
    
    def _write_json(self, data: Dict) -> None:
        """Write data to JSON file with formatting."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def generate_task_id(self) -> str:
        """Generate unique ID using UUID."""
        return str(uuid.uuid4())
    
    def add_task(self, task: Dict) -> bool:
        """
        Add new task with unique ID, check duplicates.
        Returns True if added, False if duplicate.
        """
        tasks = self.load_tasks()
        
        # Check for duplicates
        if self.is_duplicate(task, tasks):
            print(f"Duplicate task detected: {task.get('description', '')[:50]}...")
            return False
        
        # Assign unique ID if not present
        if 'id' not in task:
            task['id'] = self.generate_task_id()
        
        # Add created_at timestamp if not present
        if 'created_at' not in task:
            task['created_at'] = datetime.utcnow().isoformat() + "Z"
        
        # Ensure status is set
        if 'status' not in task:
            task['status'] = 'pending'
        
        tasks.append(task)
        self.save_tasks(tasks)
        print(f"Added task: {task['id']}")
        return True
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict]:
        """Retrieve specific task by ID."""
        tasks = self.load_tasks()
        for task in tasks:
            if task.get('id') == task_id:
                return task
        return None
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """
        Update task status (pending/done).
        Returns True if updated, False if task not found.
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.get('id') == task_id:
                task['status'] = status
                self.save_tasks(tasks)
                print(f"Updated task {task_id} status to {status}")
                return True
        print(f"Task not found: {task_id}")
        return False
    
    def is_duplicate(self, new_task: Dict, existing_tasks: List[Dict]) -> bool:
        """Compare normalized task descriptions to detect duplicates."""
        new_desc = self.normalize_text(new_task.get('description', ''))
        
        for existing_task in existing_tasks:
            existing_desc = self.normalize_text(existing_task.get('description', ''))
            if new_desc == existing_desc:
                return True
        return False
    
    def normalize_text(self, text: str) -> str:
        """Lowercase, strip whitespace, remove punctuation for comparison."""
        import string
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text


# Convenience functions for module-level access
_default_store = None

def get_store(file_path: str = "data/tasks.json") -> TaskStore:
    """Get or create the default task store instance."""
    global _default_store
    if _default_store is None:
        _default_store = TaskStore(file_path)
    return _default_store
