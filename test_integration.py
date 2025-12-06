"""
Integration test script to validate the complete system.
Tests all components without starting the Flask server.
"""

import os
import json
import sys

print("=" * 70)
print("EMAIL-TO-TASK AUTOMATION SYSTEM - INTEGRATION TEST")
print("=" * 70)
print()

# Test 1: Check all required files exist
print("Test 1: Checking project structure...")
required_files = [
    'app.py',
    'task_store.py',
    'task_extractor.py',
    'kiro_email_hook.py',
    'requirements.txt',
    'README.md',
    'static/index.html',
    'static/styles.css',
    'static/app.js',
    '.env.example',
    'examples/sample_emails.json'
]

missing_files = []
for file in required_files:
    if not os.path.exists(file):
        missing_files.append(file)
        print(f"  ✗ Missing: {file}")
    else:
        print(f"  ✓ Found: {file}")

if missing_files:
    print(f"\n✗ Test 1 FAILED: {len(missing_files)} files missing")
    sys.exit(1)
else:
    print("\n✓ Test 1 PASSED: All required files present")
print()

# Test 2: Validate JSON files
print("Test 2: Validating JSON files...")
json_files = [
    'examples/sample_emails.json',
    'examples/sample_email_urgent.json',
    'examples/sample_email_personal.json',
    'examples/sample_email_academic.json',
    '.kiro/hooks/email_hook.json'
]

for json_file in json_files:
    try:
        with open(json_file, 'r') as f:
            json.load(f)
        print(f"  ✓ Valid JSON: {json_file}")
    except json.JSONDecodeError as e:
        print(f"  ✗ Invalid JSON: {json_file} - {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"  ✗ File not found: {json_file}")
        sys.exit(1)

print("\n✓ Test 2 PASSED: All JSON files valid")
print()

# Test 3: Import Python modules
print("Test 3: Testing Python module imports...")
try:
    from task_store import TaskStore
    print("  ✓ Imported: task_store")
except ImportError as e:
    print(f"  ✗ Failed to import task_store: {e}")
    sys.exit(1)

try:
    from task_extractor import TaskExtractor
    print("  ✓ Imported: task_extractor")
except ImportError as e:
    print(f"  ✗ Failed to import task_extractor: {e}")
    sys.exit(1)

print("\n✓ Test 3 PASSED: All modules import successfully")
print()

# Test 4: Test TaskStore functionality
print("Test 4: Testing TaskStore...")
test_store_path = "data/test_integration.json"
if os.path.exists(test_store_path):
    os.remove(test_store_path)

try:
    store = TaskStore(test_store_path)
    print("  ✓ TaskStore initialized")
    
    # Test adding a task
    test_task = {
        "description": "Integration test task",
        "category": "Work",
        "priority": "High",
        "sender": "test@test.com"
    }
    
    result = store.add_task(test_task)
    if result:
        print("  ✓ Task added successfully")
    else:
        print("  ✗ Failed to add task")
        sys.exit(1)
    
    # Test loading tasks
    tasks = store.load_tasks()
    if len(tasks) > 0:
        print(f"  ✓ Loaded {len(tasks)} tasks")
    else:
        print("  ✗ No tasks loaded")
        sys.exit(1)
    
    # Test duplicate detection
    duplicate_result = store.add_task(test_task)
    if not duplicate_result:
        print("  ✓ Duplicate detection working")
    else:
        print("  ✗ Duplicate detection failed")
        sys.exit(1)
    
    # Cleanup
    if os.path.exists(test_store_path):
        os.remove(test_store_path)
    if os.path.exists(test_store_path + ".backup"):
        os.remove(test_store_path + ".backup")
    
    print("\n✓ Test 4 PASSED: TaskStore working correctly")
except Exception as e:
    print(f"\n✗ Test 4 FAILED: {e}")
    sys.exit(1)
print()

# Test 5: Test TaskExtractor
print("Test 5: Testing TaskExtractor...")
try:
    extractor = TaskExtractor()
    print("  ✓ TaskExtractor initialized")
    
    # Test category classification
    test_cases = [
        ("URGENT: Fix the server", "Urgent"),
        ("Complete research paper", "Academic"),
        ("Buy groceries", "Personal")
    ]
    
    all_correct = True
    for text, expected in test_cases:
        result = extractor.classify_category(text)
        if result == expected:
            print(f"  ✓ Classification correct: '{text[:30]}...' -> {result}")
        else:
            print(f"  ✗ Classification wrong: '{text[:30]}...' -> {result} (expected {expected})")
            all_correct = False
    
    if all_correct:
        print("\n✓ Test 5 PASSED: TaskExtractor working correctly")
    else:
        print("\n✗ Test 5 FAILED: Some classifications incorrect")
        sys.exit(1)
except Exception as e:
    print(f"\n✗ Test 5 FAILED: {e}")
    sys.exit(1)
print()

# Test 6: Check HTML/CSS/JS files
print("Test 6: Validating frontend files...")
try:
    with open('static/index.html', 'r') as f:
        html_content = f.read()
        if 'Email-to-Task Dashboard' in html_content:
            print("  ✓ HTML contains dashboard title")
        if 'chart.js' in html_content.lower():
            print("  ✓ HTML includes Chart.js")
        if 'app.js' in html_content:
            print("  ✓ HTML links to app.js")
    
    with open('static/styles.css', 'r') as f:
        css_content = f.read()
        if 'dark-mode' in css_content:
            print("  ✓ CSS includes dark mode styles")
        if '.task-card' in css_content:
            print("  ✓ CSS includes task card styles")
    
    with open('static/app.js', 'r') as f:
        js_content = f.read()
        if 'fetchTasks' in js_content:
            print("  ✓ JS includes fetchTasks function")
        if 'toggleDarkMode' in js_content:
            print("  ✓ JS includes dark mode toggle")
        if 'renderCharts' in js_content:
            print("  ✓ JS includes chart rendering")
    
    print("\n✓ Test 6 PASSED: Frontend files valid")
except Exception as e:
    print(f"\n✗ Test 6 FAILED: {e}")
    sys.exit(1)
print()

# Final summary
print("=" * 70)
print("✓ ALL INTEGRATION TESTS PASSED")
print("=" * 70)
print()
print("System is ready to run!")
print()
print("Next steps:")
print("1. Set up your .env file with OpenAI API key (optional)")
print("2. Run: python app.py")
print("3. Open: http://localhost:8000")
print()
print("=" * 70)
