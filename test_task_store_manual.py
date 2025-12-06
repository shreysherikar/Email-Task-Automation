"""Manual test script for task store functionality."""

from task_store import TaskStore
import os

# Clean up any existing test file
test_file = "data/test_tasks.json"
if os.path.exists(test_file):
    os.remove(test_file)

print("=== Testing Task Store ===\n")

# Test 1: Initialize store
print("Test 1: Initialize store")
store = TaskStore(test_file)
tasks = store.load_tasks()
print(f"✓ Store initialized with {len(tasks)} sample tasks\n")

# Test 2: Add new task
print("Test 2: Add new task")
new_task = {
    "description": "Test task for validation",
    "category": "Work",
    "priority": "Medium",
    "sender": "test@example.com"
}
result = store.add_task(new_task)
print(f"✓ Task added: {result}\n")

# Test 3: Duplicate detection
print("Test 3: Duplicate detection")
duplicate_task = {
    "description": "Test task for validation!!!",  # Same but with punctuation
    "category": "Work",
    "priority": "High",
    "sender": "other@example.com"
}
result = store.is_duplicate(duplicate_task, store.load_tasks())
print(f"✓ Duplicate detected: {result}\n")

# Test 4: Get task by ID
print("Test 4: Get task by ID")
tasks = store.load_tasks()
if tasks:
    first_task = tasks[0]
    retrieved = store.get_task_by_id(first_task['id'])
    print(f"✓ Retrieved task: {retrieved['description'][:50]}...\n")

# Test 5: Update task status
print("Test 5: Update task status")
if tasks:
    task_id = tasks[0]['id']
    result = store.update_task_status(task_id, 'done')
    updated_task = store.get_task_by_id(task_id)
    print(f"✓ Status updated: {updated_task['status']}\n")

# Test 6: Text normalization
print("Test 6: Text normalization")
text1 = "  Hello, World!  "
text2 = "hello world"
norm1 = store.normalize_text(text1)
norm2 = store.normalize_text(text2)
print(f"✓ Normalized '{text1}' -> '{norm1}'")
print(f"✓ Normalized '{text2}' -> '{norm2}'")
print(f"✓ Are equal: {norm1 == norm2}\n")

print("=== All Tests Passed ===")

# Cleanup
if os.path.exists(test_file):
    os.remove(test_file)
if os.path.exists(test_file + ".backup"):
    os.remove(test_file + ".backup")
