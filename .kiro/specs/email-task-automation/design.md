# Design Document: Email-to-Task Automation System

## Overview

The Email-to-Task Automation System is a Python Flask-based web application that automatically extracts actionable tasks from incoming emails using LLM-powered natural language processing. The system stores tasks in a file-based JSON database and presents them through a modern, interactive web dashboard with analytics capabilities. The architecture emphasizes simplicity, using no external databases and operating entirely within a virtual environment on port 8000.

The system consists of four primary components:
1. **Email Ingestion & Task Extraction**: Processes raw email text and extracts structured task data using LLM
2. **File-Based Storage**: Manages task persistence in JSON format with duplicate detection
3. **REST API Layer**: Provides endpoints for task management and email processing
4. **Web Dashboard**: Delivers an interactive UI with filtering, analytics, and visualizations

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│  Incoming Email │
│   (Raw Text)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│      Kiro Hook (Automation)         │
│  - Triggers on email arrival        │
│  - Validates payload                │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Flask Application (Port 8000)     │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Email Ingestion Endpoint    │  │
│  │  POST /ingest-email          │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │   LLM Task Extractor         │  │
│  │  - Parse email content       │  │
│  │  - Extract tasks             │  │
│  │  - Classify categories       │  │
│  │  - Detect dates/priorities   │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │   Task Store Manager         │  │
│  │  - Validate duplicates       │  │
│  │  - Assign unique IDs         │  │
│  │  - Write to JSON             │  │
│  └──────────┬───────────────────┘  │
│             │                       │
└─────────────┼───────────────────────┘
              │
              ▼
     ┌────────────────┐
     │ /data/tasks.json│
     │  (File Storage) │
     └────────┬────────┘
              │
              ▼
     ┌────────────────────────┐
     │   REST API Endpoints   │
     │  GET /                 │
     │  GET /tasks            │
     │  POST /tasks/complete  │
     └────────┬───────────────┘
              │
              ▼
     ┌────────────────────────┐
     │   Web Dashboard        │
     │  - Task lists          │
     │  - Filters             │
     │  - Analytics charts    │
     │  - Dark mode           │
     └────────────────────────┘
```

### Component Interaction Flow

1. **Email Arrival**: Raw email text (subject + body) arrives via POST to `/ingest-email`
2. **LLM Processing**: Task Extractor sends email to LLM with structured prompt requesting task extraction
3. **Task Structuring**: LLM response is parsed into structured task objects with fields: description, category, priority, due_date, sender
4. **Duplicate Detection**: Task Store compares new tasks against existing tasks using normalized text matching
5. **Persistence**: Valid tasks are assigned unique IDs and appended to `/data/tasks.json`
6. **Dashboard Refresh**: Frontend polls `/tasks` endpoint or uses manual refresh to display updated task list
7. **User Actions**: Users can filter, complete tasks, and view analytics through the dashboard

## Components and Interfaces

### 1. Flask Application (`app.py`)

**Responsibilities:**
- Initialize Flask server on port 8000
- Define REST API routes
- Serve static dashboard HTML/CSS/JS
- Coordinate between Task Extractor and Task Store

**Key Methods:**
```python
def init_app() -> Flask
    # Initialize Flask app, configure routes, ensure data directory exists

def index() -> str
    # Serve dashboard HTML (GET /)

def get_tasks() -> Response
    # Return all tasks as JSON (GET /tasks)

def ingest_email() -> Response
    # Process incoming email, extract tasks (POST /ingest-email)
    # Expected payload: {"subject": str, "body": str, "sender": str}

def complete_task(task_id: str) -> Response
    # Mark task as done (POST /tasks/complete/<id>)
```

### 2. Task Extractor (`task_extractor.py`)

**Responsibilities:**
- Interface with LLM API for task extraction
- Parse and structure LLM responses
- Classify tasks into categories
- Extract metadata (dates, priorities, sender info)

**Key Methods:**
```python
def extract_tasks_from_email(subject: str, body: str, sender: str) -> List[Dict]
    # Main extraction method
    # Returns list of task dictionaries

def build_extraction_prompt(subject: str, body: str) -> str
    # Construct LLM prompt with instructions for task extraction

def parse_llm_response(response: str) -> List[Dict]
    # Parse LLM JSON response into structured task objects

def classify_category(task_text: str) -> str
    # Determine category: Work, Personal, Academic, Urgent, Low Priority

def extract_due_date(task_text: str) -> Optional[str]
    # Extract and normalize due date from task text

def determine_priority(task_text: str, category: str) -> str
    # Determine priority level: High, Medium, Low
```

**LLM Integration:**
- Use OpenAI API or similar LLM service
- Prompt engineering for consistent JSON output
- Fallback handling for malformed responses

### 3. Task Store (`task_store.py`)

**Responsibilities:**
- Manage JSON file operations
- Ensure data integrity
- Detect and prevent duplicates
- Provide CRUD operations for tasks

**Key Methods:**
```python
def initialize_store(file_path: str = "/data/tasks.json") -> None
    # Create JSON file if not exists, seed with sample data

def load_tasks() -> List[Dict]
    # Read and parse tasks from JSON file

def save_tasks(tasks: List[Dict]) -> None
    # Write tasks to JSON file with proper formatting

def add_task(task: Dict) -> bool
    # Add new task with unique ID, check duplicates
    # Returns True if added, False if duplicate

def is_duplicate(new_task: Dict, existing_tasks: List[Dict]) -> bool
    # Compare normalized task descriptions

def normalize_text(text: str) -> str
    # Lowercase, strip whitespace, remove punctuation for comparison

def get_task_by_id(task_id: str) -> Optional[Dict]
    # Retrieve specific task

def update_task_status(task_id: str, status: str) -> bool
    # Update task status (pending/done)

def generate_task_id() -> str
    # Generate unique ID using UUID or timestamp
```

### 4. Web Dashboard (`static/index.html`, `static/app.js`, `static/styles.css`)

**Responsibilities:**
- Render task lists with filtering
- Display analytics charts
- Handle user interactions
- Provide dark mode toggle

**Key Components:**

**HTML Structure:**
```html
- Header with title and dark mode toggle
- Metrics section (category counts, urgency counts)
- Filter controls (category, urgency, status)
- Task list container
- Charts container (pie chart, bar chart)
```

**JavaScript Functions:**
```javascript
async function fetchTasks()
    // GET /tasks and update UI

function renderTasks(tasks, filters)
    // Display filtered task list

function renderMetrics(tasks)
    // Calculate and display counts

function renderPieChart(tasks)
    // Category distribution using Chart.js

function renderBarChart(tasks)
    // Tasks per sender using Chart.js

function applyFilters()
    // Filter tasks by category/urgency/status

async function completeTask(taskId)
    // POST /tasks/complete/<id>

function toggleDarkMode()
    // Switch between light/dark themes
```

**Styling:**
- Modern, clean design with card-based layout
- Responsive grid for task cards
- Color-coded categories
- Dark mode with CSS variables

### 5. Kiro Hook Script (`kiro_email_hook.py`)

**Responsibilities:**
- Trigger on email arrival event
- Validate email payload structure
- Call Flask ingestion endpoint
- Log processing results

**Key Methods:**
```python
def on_email_received(email_payload: Dict) -> None
    # Main hook entry point
    # Validates payload and triggers ingestion

def validate_email_payload(payload: Dict) -> bool
    # Ensure required fields present: subject, body, sender

def send_to_ingestion_endpoint(payload: Dict) -> Response
    # POST to http://localhost:8000/ingest-email
```

## Data Models

### Task Object

```python
{
    "id": str,              # Unique identifier (UUID)
    "description": str,     # Task description extracted from email
    "category": str,        # One of: Work, Personal, Academic, Urgent, Low Priority
    "priority": str,        # One of: High, Medium, Low
    "due_date": str | None, # ISO format date string or None
    "sender": str,          # Email sender address or name
    "status": str,          # One of: pending, done
    "created_at": str,      # ISO format timestamp
    "source_email": {       # Optional: original email metadata
        "subject": str,
        "received_at": str
    }
}
```

### Email Payload (Ingestion Input)

```python
{
    "subject": str,         # Email subject line
    "body": str,            # Email body content
    "sender": str           # Sender email address
}
```

### Tasks JSON File Structure

```json
{
    "tasks": [
        {
            "id": "uuid-string",
            "description": "Complete project report",
            "category": "Work",
            "priority": "High",
            "due_date": "2025-12-10",
            "sender": "boss@company.com",
            "status": "pending",
            "created_at": "2025-12-05T10:30:00Z"
        }
    ],
    "metadata": {
        "last_updated": "2025-12-05T10:30:00Z",
        "total_tasks": 1
    }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After analyzing all acceptance criteria, I identified several redundant properties that can be consolidated:
- Task field validation properties (3.3, 4.3) → Combined into single property
- Status update properties (6.1, 6.2) → Combined into round-trip property
- Metrics properties (5.1, 5.2, 5.3, 5.4) → Consolidated into metrics accuracy property
- Filtering properties (9.1, 9.2, 9.3) → Generalized into single filtering property
- Duplicate detection (3.4, 3.5) → Combined into single property

### Testable Correctness Properties

**Property 1: Task extraction completeness**
*For any* email containing identifiable tasks, the Task Extractor should extract all actionable tasks present in the email content.
**Validates: Requirements 1.2**

**Property 2: Due date extraction accuracy**
*For any* email containing date expressions, the Task Extractor should correctly identify and normalize due dates into ISO format.
**Validates: Requirements 1.3**

**Property 3: Priority detection consistency**
*For any* task text containing priority indicators (urgent, high, low, ASAP, etc.), the Task Extractor should assign the appropriate priority level.
**Validates: Requirements 1.4**

**Property 4: Sender association preservation**
*For any* email with sender information, all extracted tasks should be associated with the correct sender identifier.
**Validates: Requirements 1.5**

**Property 5: Category classification validity**
*For any* extracted task, the Task Extractor should assign exactly one category from the valid set: Work, Personal, Academic, Urgent, or Low Priority.
**Validates: Requirements 2.1**

**Property 6: Urgency precedence**
*For any* task containing urgency indicators (urgent, ASAP, critical, emergency), the Task Extractor should assign the Urgent category regardless of other content.
**Validates: Requirements 2.3**

**Property 7: Category persistence**
*For any* task with an assigned category, storing and retrieving the task should preserve the category value unchanged.
**Validates: Requirements 2.4**

**Property 8: Unique ID assignment**
*For any* set of tasks added to the Task Store, each task should receive a unique identifier that differs from all other task IDs.
**Validates: Requirements 3.2**

**Property 9: Required fields completeness**
*For any* task stored in the Task Store, the task object should contain all required fields: id, description, category, priority, due_date, sender, status, and created_at.
**Validates: Requirements 3.3, 4.3**

**Property 10: Duplicate rejection**
*For any* task that matches an existing task's normalized description, the Task Store should reject the duplicate and maintain only the original task.
**Validates: Requirements 3.4, 3.5**

**Property 11: Normalization equivalence**
*For any* two task descriptions that differ only in whitespace, capitalization, or punctuation, the normalization function should produce identical normalized strings.
**Validates: Requirements 3.5**

**Property 12: Status update round-trip**
*For any* task marked as complete, reading the task from storage should reflect the updated status as "done".
**Validates: Requirements 6.1, 6.2**

**Property 13: Metrics accuracy**
*For any* set of tasks, the calculated metrics (category counts, urgency counts, sender counts) should exactly match the actual distribution in the task set.
**Validates: Requirements 5.1, 5.2, 5.4**

**Property 14: Chart data correctness**
*For any* set of tasks, the data structures generated for pie charts and bar charts should accurately represent the task distribution without loss or duplication.
**Validates: Requirements 5.3, 5.4**

**Property 15: Metrics update consistency**
*For any* task set, after adding or removing tasks, the metrics should update to reflect the new task set accurately.
**Validates: Requirements 5.5**

**Property 16: Filter correctness**
*For any* task set and any filter criteria (category, urgency, status), the filtered results should contain only tasks matching the criteria and should include all matching tasks.
**Validates: Requirements 9.1, 9.2, 9.3**

**Property 17: Filtered metrics accuracy**
*For any* task set with applied filters, the displayed metrics should reflect only the filtered tasks, not the complete task set.
**Validates: Requirements 9.4**

**Property 18: Filter reset completeness**
*For any* task set with active filters, clearing all filters should result in displaying the complete unfiltered task set.
**Validates: Requirements 9.5**

**Property 19: Hook payload extraction**
*For any* valid email payload received by the Kiro Hook, the hook should correctly extract subject, body, and sender fields.
**Validates: Requirements 7.2**

**Property 20: Hook task persistence**
*For any* tasks extracted by the Task Extractor via the Kiro Hook, all tasks should be successfully written to the Task Store.
**Validates: Requirements 7.4**

**Property 21: Hook duplicate validation**
*For any* duplicate tasks in the Kiro Hook processing flow, the hook should prevent duplicate storage before writing to the Task Store.
**Validates: Requirements 7.5**

**Property 22: API task retrieval completeness**
*For any* set of tasks in the Task Store, a GET request to /tasks should return all stored tasks without omission or duplication.
**Validates: Requirements 8.3**

**Property 23: API completion endpoint correctness**
*For any* valid task ID, a POST request to /tasks/complete/<id> should update that specific task's status to "done".
**Validates: Requirements 8.4**

**Property 24: API ingestion endpoint processing**
*For any* valid email payload sent to POST /ingest-email, the endpoint should extract tasks and store them in the Task Store.
**Validates: Requirements 8.5**

### Example-Based Test Cases

**Example 1: Store initialization**
When the Flask Application starts with no existing /data/tasks.json file, the Task Store should create the file with an empty tasks array and metadata.
**Validates: Requirements 3.1**

**Example 2: Dashboard HTML serving**
When a GET request is made to the root path (/), the Flask Application should return valid HTML containing the dashboard structure.
**Validates: Requirements 4.1, 8.2**

**Example 3: Dashboard sections presence**
When the Dashboard HTML is rendered, it should contain identifiable sections for: All Tasks, Category Filters, Urgent Tasks, and Completed vs Pending toggle.
**Validates: Requirements 4.2**

**Example 4: Dark mode toggle**
When dark mode is enabled via the toggle, the Dashboard should apply dark theme CSS classes to the body element.
**Validates: Requirements 4.4**

**Example 5: Port configuration**
When the Flask Application starts, it should bind to and listen on port 8000.
**Validates: Requirements 8.1**

**Example 6: Sample data seeding**
When the Task Store initializes for the first time, it should create at least 3 sample tasks with varied categories, priorities, and senders.
**Validates: Requirements 10.2, 10.4**

## Error Handling

### LLM API Failures

**Scenario**: LLM API is unavailable or returns errors
**Handling**:
- Implement retry logic with exponential backoff (3 attempts)
- Log detailed error information
- Return graceful error response to user: "Unable to process email at this time. Please try again later."
- Store failed email payload in `/data/failed_emails.json` for manual review

### Malformed LLM Responses

**Scenario**: LLM returns non-JSON or incomplete data
**Handling**:
- Validate LLM response structure before parsing
- Attempt to extract partial task data if possible
- Log malformed response for debugging
- Return partial results with warning flag
- Fallback to basic keyword extraction if LLM parsing fails completely

### File System Errors

**Scenario**: Unable to read/write `/data/tasks.json`
**Handling**:
- Check file permissions on startup
- Create `/data` directory if missing
- Implement file locking to prevent concurrent write conflicts
- Maintain in-memory backup of tasks
- Return HTTP 500 with descriptive error message
- Log file system errors with full stack trace

### Duplicate Task Detection Edge Cases

**Scenario**: Tasks are similar but not identical
**Handling**:
- Use configurable similarity threshold (default: 90% match)
- Allow manual override via API parameter: `force_add=true`
- Log near-duplicates for user review
- Provide UI indication when similar tasks exist

### Invalid Email Payloads

**Scenario**: Missing required fields (subject, body, sender)
**Handling**:
- Validate payload structure before processing
- Return HTTP 400 with specific field errors
- Log invalid payloads for debugging
- Provide clear error messages: "Missing required field: {field_name}"

### Task Completion Errors

**Scenario**: Attempting to complete non-existent task ID
**Handling**:
- Validate task ID exists before update
- Return HTTP 404 with message: "Task not found: {task_id}"
- Log invalid task ID attempts
- Suggest valid task IDs in error response

### JSON Parsing Errors

**Scenario**: Corrupted `/data/tasks.json` file
**Handling**:
- Implement JSON validation on load
- Create backup file before each write: `/data/tasks.json.backup`
- Attempt to recover from backup if main file is corrupted
- If recovery fails, initialize with empty task list and log data loss
- Notify user of data recovery attempt

### Rate Limiting

**Scenario**: Too many LLM API requests
**Handling**:
- Implement request queuing with max queue size
- Return HTTP 429 when queue is full
- Provide estimated wait time in response
- Cache LLM responses for identical email content (1 hour TTL)

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples, edge cases, and error conditions for individual components. The testing framework will be **pytest** for Python backend components and **Jest** for JavaScript frontend components.

**Backend Unit Tests** (`tests/test_*.py`):
- `test_task_store.py`: File operations, duplicate detection, CRUD operations
- `test_task_extractor.py`: LLM prompt construction, response parsing, category classification
- `test_app.py`: Flask route handlers, request validation, response formatting
- `test_kiro_hook.py`: Payload validation, endpoint calling, error handling

**Frontend Unit Tests** (`static/tests/test_*.js`):
- `test_filters.js`: Filter logic, category matching, status filtering
- `test_metrics.js`: Count calculations, chart data generation
- `test_ui.js`: DOM manipulation, event handlers, dark mode toggle

**Key Unit Test Examples**:
- Empty email body returns empty task list
- Malformed JSON in tasks.json triggers recovery from backup
- Completing non-existent task returns 404
- Duplicate task with identical description is rejected
- Task with "URGENT" keyword gets Urgent category
- Normalized text removes punctuation and whitespace correctly

### Property-Based Testing

Property-based tests will verify universal properties that should hold across all inputs using **Hypothesis** for Python. Each property test will run a minimum of 100 iterations with randomly generated inputs.

**Property Test Configuration**:
```python
from hypothesis import given, settings
import hypothesis.strategies as st

@settings(max_examples=100)
@given(st.text(), st.text(), st.emails())
def test_property(subject, body, sender):
    # Test implementation
    pass
```

**Property Test Tagging**:
Each property-based test MUST include a comment explicitly referencing the correctness property from this design document:

```python
# Feature: email-task-automation, Property 1: Task extraction completeness
@settings(max_examples=100)
def test_task_extraction_completeness():
    # Test that all tasks in email are extracted
    pass
```

**Property Test Coverage**:
- **Property 1-6**: Task extraction and classification properties
- **Property 7-12**: Storage and persistence properties
- **Property 13-18**: Metrics and filtering properties
- **Property 19-24**: API and hook integration properties

**Test Data Generators**:
```python
# Email content generator
@st.composite
def email_with_tasks(draw):
    num_tasks = draw(st.integers(min_value=1, max_value=10))
    tasks = [draw(st.text(min_size=10)) for _ in range(num_tasks)]
    subject = draw(st.text(min_size=5))
    body = "\n".join(tasks)
    sender = draw(st.emails())
    return {"subject": subject, "body": body, "sender": sender}

# Task generator
@st.composite
def valid_task(draw):
    return {
        "description": draw(st.text(min_size=10)),
        "category": draw(st.sampled_from(["Work", "Personal", "Academic", "Urgent", "Low Priority"])),
        "priority": draw(st.sampled_from(["High", "Medium", "Low"])),
        "sender": draw(st.emails())
    }
```

### Integration Testing

Integration tests will verify end-to-end workflows:
- Email ingestion → Task extraction → Storage → Dashboard display
- Task completion → Storage update → Dashboard refresh
- Kiro hook trigger → API call → Task creation

### Test Execution

**Running Tests**:
```bash
# Backend unit tests
pytest tests/ -v

# Backend property tests
pytest tests/property_tests/ -v --hypothesis-show-statistics

# Frontend tests
npm test

# All tests
pytest tests/ && npm test
```

**Coverage Requirements**:
- Minimum 80% code coverage for backend
- All correctness properties must have corresponding property tests
- All API endpoints must have integration tests

## Deployment and Configuration

### Virtual Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies (`requirements.txt`)

```
flask==3.0.0
openai==1.3.0
python-dateutil==2.8.2
hypothesis==6.92.0
pytest==7.4.3
requests==2.31.0
```

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_PORT=8000
TASK_STORE_PATH=/data/tasks.json
LLM_MODEL=gpt-4
```

### Running the Application

```bash
# Start Flask server
python app.py

# Access dashboard
http://localhost:8000

# Test email ingestion
curl -X POST http://localhost:8000/ingest-email \
  -H "Content-Type: application/json" \
  -d '{"subject":"Meeting tomorrow","body":"Prepare slides for client presentation","sender":"boss@company.com"}'
```

### Kiro Hook Configuration

The Kiro hook should be configured to trigger on email arrival events. Configuration file: `.kiro/hooks/email_hook.json`

```json
{
  "name": "Email Task Extraction",
  "trigger": "email_received",
  "script": "kiro_email_hook.py",
  "enabled": true
}
```

## Future Enhancements

1. **Email Integration**: Direct IMAP/Gmail API integration for automatic email fetching
2. **Task Editing**: UI for editing task details after extraction
3. **Recurring Tasks**: Support for recurring task patterns
4. **Notifications**: Email/push notifications for upcoming due dates
5. **Multi-user Support**: User authentication and task ownership
6. **Advanced Analytics**: Trend analysis, completion rates, time tracking
7. **Export Functionality**: Export tasks to CSV, PDF, or calendar formats
8. **Mobile Responsive**: Full mobile UI optimization
9. **Task Dependencies**: Link related tasks and track dependencies
10. **AI Suggestions**: LLM-powered task prioritization and scheduling recommendations
