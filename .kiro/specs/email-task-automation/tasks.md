# Implementation Plan: Email-to-Task Automation System

- [x] 1. Set up project structure and dependencies


  - Create directory structure: `/data`, `/static`, `/tests`, `/tests/property_tests`
  - Create `requirements.txt` with Flask, OpenAI, Hypothesis, pytest, requests, python-dateutil
  - Create `.env` file template for API keys and configuration
  - Create virtual environment setup instructions
  - _Requirements: 8.6_

- [x] 2. Implement Task Store with file-based JSON storage


  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 2.1 Create task_store.py with core storage functions


  - Implement `initialize_store()` to create /data/tasks.json with empty structure
  - Implement `load_tasks()` to read and parse JSON file
  - Implement `save_tasks()` to write tasks with proper formatting
  - Implement `generate_task_id()` using UUID
  - Implement `add_task()` with duplicate checking
  - Implement `get_task_by_id()` for task retrieval
  - Implement `update_task_status()` for marking tasks complete
  - _Requirements: 3.1, 3.2, 6.1, 6.2_

- [x] 2.2 Implement duplicate detection with text normalization

  - Implement `normalize_text()` to lowercase, strip whitespace, remove punctuation
  - Implement `is_duplicate()` to compare normalized descriptions
  - _Requirements: 3.4, 3.5_

- [x] 2.3 Add sample data seeding


  - Create `seed_sample_tasks()` function with 5+ varied sample tasks
  - Include tasks with different categories, priorities, senders, and due dates
  - Call seeding during store initialization
  - _Requirements: 10.2, 10.4_

- [ ]* 2.4 Write property test for unique ID assignment
  - **Property 8: Unique ID assignment**
  - **Validates: Requirements 3.2**

- [ ]* 2.5 Write property test for required fields completeness
  - **Property 9: Required fields completeness**
  - **Validates: Requirements 3.3**

- [ ]* 2.6 Write property test for duplicate rejection
  - **Property 10: Duplicate rejection**
  - **Validates: Requirements 3.4**

- [ ]* 2.7 Write property test for normalization equivalence
  - **Property 11: Normalization equivalence**
  - **Validates: Requirements 3.5**

- [ ]* 2.8 Write property test for status update round-trip
  - **Property 12: Status update round-trip**
  - **Validates: Requirements 6.1, 6.2**

- [x] 3. Implement LLM-powered Task Extractor


  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.3_

- [x] 3.1 Create task_extractor.py with LLM integration


  - Implement `extract_tasks_from_email()` as main entry point
  - Implement `build_extraction_prompt()` with structured instructions for LLM
  - Configure OpenAI API client with error handling
  - _Requirements: 1.1, 1.2_

- [x] 3.2 Implement LLM response parsing

  - Implement `parse_llm_response()` to extract JSON from LLM output
  - Add validation for required task fields
  - Handle malformed responses with fallback logic
  - _Requirements: 1.2_

- [x] 3.3 Implement metadata extraction functions

  - Implement `extract_due_date()` using dateutil parser
  - Implement `determine_priority()` based on keywords (urgent, ASAP, high, low)
  - Implement `classify_category()` for Work, Personal, Academic, Urgent, Low Priority
  - _Requirements: 1.3, 1.4, 2.1_

- [x] 3.4 Implement urgency detection with precedence

  - Add urgency keyword detection (urgent, ASAP, critical, emergency)
  - Override category to "Urgent" when urgency indicators found
  - _Requirements: 2.3_

- [ ]* 3.5 Write property test for task extraction completeness
  - **Property 1: Task extraction completeness**
  - **Validates: Requirements 1.2**

- [ ]* 3.6 Write property test for due date extraction accuracy
  - **Property 2: Due date extraction accuracy**
  - **Validates: Requirements 1.3**

- [ ]* 3.7 Write property test for priority detection consistency
  - **Property 3: Priority detection consistency**
  - **Validates: Requirements 1.4**

- [ ]* 3.8 Write property test for sender association preservation
  - **Property 4: Sender association preservation**
  - **Validates: Requirements 1.5**

- [ ]* 3.9 Write property test for category classification validity
  - **Property 5: Category classification validity**
  - **Validates: Requirements 2.1**

- [ ]* 3.10 Write property test for urgency precedence
  - **Property 6: Urgency precedence**
  - **Validates: Requirements 2.3**

- [ ]* 3.11 Write property test for category persistence
  - **Property 7: Category persistence**
  - **Validates: Requirements 2.4**

- [x] 4. Build Flask application with REST API endpoints


  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 4.1 Create app.py with Flask initialization


  - Initialize Flask app
  - Configure port 8000
  - Set up CORS if needed
  - Initialize Task Store on startup
  - _Requirements: 8.1_

- [x] 4.2 Implement GET / endpoint for dashboard

  - Serve static HTML file from /static/index.html
  - _Requirements: 8.2, 4.1_

- [x] 4.3 Implement GET /tasks endpoint

  - Return all tasks from Task Store as JSON
  - Include proper error handling
  - _Requirements: 8.3_

- [x] 4.4 Implement POST /tasks/complete/<id> endpoint

  - Validate task ID exists
  - Update task status to "done"
  - Return updated task or error
  - _Requirements: 8.4, 6.1_

- [x] 4.5 Implement POST /ingest-email endpoint

  - Validate payload contains subject, body, sender
  - Call Task Extractor with email content
  - Store extracted tasks via Task Store
  - Return extraction results
  - _Requirements: 8.5, 1.1_

- [x] 4.6 Add error handling for all endpoints

  - Implement try-catch blocks with appropriate HTTP status codes
  - Log errors with stack traces
  - Return user-friendly error messages
  - _Requirements: All error handling scenarios_

- [ ]* 4.7 Write property test for API task retrieval completeness
  - **Property 22: API task retrieval completeness**
  - **Validates: Requirements 8.3**

- [ ]* 4.8 Write property test for API completion endpoint correctness
  - **Property 23: API completion endpoint correctness**
  - **Validates: Requirements 8.4**

- [ ]* 4.9 Write property test for API ingestion endpoint processing
  - **Property 24: API ingestion endpoint processing**
  - **Validates: Requirements 8.5**

- [x] 5. Create web dashboard with HTML, CSS, and JavaScript


  - _Requirements: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4, 5.5, 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 5.1 Create static/index.html with dashboard structure


  - Add header with title and dark mode toggle
  - Add metrics section for category and urgency counts
  - Add filter controls (category dropdown, urgency toggle, status toggle)
  - Add task list container with card layout
  - Add charts container for pie and bar charts
  - Include Chart.js library via CDN
  - _Requirements: 4.1, 4.2_

- [x] 5.2 Create static/styles.css with modern styling


  - Implement clean, modern design with card-based layout
  - Add CSS variables for light and dark themes
  - Style task cards with color-coded categories
  - Make layout responsive with CSS Grid/Flexbox
  - Add dark mode styles
  - _Requirements: 4.4_

- [x] 5.3 Create static/app.js with core functionality


  - Implement `fetchTasks()` to GET /tasks
  - Implement `renderTasks()` to display task cards
  - Implement `renderMetrics()` to calculate and display counts
  - Call fetchTasks() on page load
  - _Requirements: 4.3, 5.1, 5.2_

- [x] 5.4 Implement filtering functionality

  - Implement `applyFilters()` to filter by category, urgency, status
  - Add event listeners to filter controls
  - Update task display when filters change
  - Implement filter reset functionality
  - _Requirements: 9.1, 9.2, 9.3, 9.5_

- [x] 5.5 Implement metrics and charts with Chart.js

  - Implement `renderPieChart()` for category distribution
  - Implement `renderBarChart()` for tasks per sender
  - Update charts when filters applied
  - Destroy and recreate charts on data change
  - _Requirements: 5.3, 5.4, 9.4_

- [x] 5.6 Implement task completion functionality

  - Implement `completeTask()` to POST /tasks/complete/<id>
  - Add "Mark Complete" button to each task card
  - Update UI after successful completion
  - Add visual distinction for completed tasks
  - _Requirements: 6.1, 6.3, 6.4_

- [x] 5.7 Implement dark mode toggle

  - Add toggle button in header
  - Implement `toggleDarkMode()` to switch themes
  - Save preference to localStorage
  - Load saved preference on page load
  - _Requirements: 4.4_

- [ ]* 5.8 Write property test for metrics accuracy
  - **Property 13: Metrics accuracy**
  - **Validates: Requirements 5.1, 5.2**

- [ ]* 5.9 Write property test for chart data correctness
  - **Property 14: Chart data correctness**
  - **Validates: Requirements 5.3, 5.4**

- [ ]* 5.10 Write property test for metrics update consistency
  - **Property 15: Metrics update consistency**
  - **Validates: Requirements 5.5**

- [ ]* 5.11 Write property test for filter correctness
  - **Property 16: Filter correctness**
  - **Validates: Requirements 9.1, 9.2, 9.3**

- [ ]* 5.12 Write property test for filtered metrics accuracy
  - **Property 17: Filtered metrics accuracy**
  - **Validates: Requirements 9.4**

- [ ]* 5.13 Write property test for filter reset completeness
  - **Property 18: Filter reset completeness**
  - **Validates: Requirements 9.5**

- [x] 6. Implement Kiro Hook for automated email processing


  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 6.1 Create kiro_email_hook.py script


  - Implement `on_email_received()` as main entry point
  - Implement `validate_email_payload()` to check required fields
  - Implement `send_to_ingestion_endpoint()` to POST to /ingest-email
  - Add error handling and logging
  - _Requirements: 7.2, 7.3, 7.4, 7.5_

- [x] 6.2 Create Kiro hook configuration


  - Create `.kiro/hooks/email_hook.json` configuration file
  - Set trigger to email_received event
  - Enable hook by default
  - _Requirements: 7.1_

- [ ]* 6.3 Write property test for hook payload extraction
  - **Property 19: Hook payload extraction**
  - **Validates: Requirements 7.2**

- [ ]* 6.4 Write property test for hook task persistence
  - **Property 20: Hook task persistence**
  - **Validates: Requirements 7.4**

- [ ]* 6.5 Write property test for hook duplicate validation
  - **Property 21: Hook duplicate validation**
  - **Validates: Requirements 7.5**

- [x] 7. Create documentation and setup instructions


  - _Requirements: 10.1, 10.3_

- [x] 7.1 Create README.md with comprehensive documentation


  - Add project overview and features
  - Add setup instructions (virtual environment, dependencies)
  - Add configuration instructions (API keys, environment variables)
  - Add usage instructions (starting server, accessing dashboard)
  - Add API endpoint documentation with examples
  - Add Kiro hook setup instructions
  - Add troubleshooting section
  - _Requirements: 10.1, 10.3_

- [x] 7.2 Create example email payloads for testing


  - Create `examples/sample_emails.json` with 5+ varied email examples
  - Include emails with different task types, urgency levels, and formats
  - Add curl commands for testing ingestion endpoint
  - _Requirements: 10.1_

- [x] 8. Final integration and testing checkpoint



  - Start Flask application and verify it runs on port 8000
  - Test dashboard loads and displays sample tasks
  - Test email ingestion via curl with sample payloads
  - Test task completion functionality
  - Test filtering and metrics
  - Test dark mode toggle
  - Verify all endpoints return appropriate responses
  - Ensure all tests pass, ask the user if questions arise
  - _Requirements: All requirements_
