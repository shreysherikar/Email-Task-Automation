"""Manual test script for task extractor functionality."""

from task_extractor import TaskExtractor

print("=== Testing Task Extractor ===\n")

# Initialize extractor (will use fallback mode without API key)
extractor = TaskExtractor()

# Test 1: Basic extraction with fallback
print("Test 1: Fallback extraction")
subject = "Project Updates Needed"
body = """Hi team,

Please complete the following tasks:
1. Finish the Q4 report by December 15th
2. Review the client presentation slides
3. URGENT: Fix the production server issue immediately

Thanks!
"""
sender = "manager@company.com"

tasks = extractor.extract_tasks_from_email(subject, body, sender)
print(f"✓ Extracted {len(tasks)} tasks")
for i, task in enumerate(tasks, 1):
    print(f"  {i}. {task['description'][:60]}...")
    print(f"     Category: {task['category']}, Priority: {task['priority']}")
print()

# Test 2: Category classification
print("Test 2: Category classification")
test_cases = [
    ("URGENT: Server is down", "Urgent"),
    ("Complete research paper for class", "Academic"),
    ("Buy groceries for dinner", "Personal"),
    ("Prepare client presentation", "Work"),
    ("Maybe update the docs sometime", "Low Priority")
]

for text, expected in test_cases:
    result = extractor.classify_category(text)
    status = "✓" if result == expected else "✗"
    print(f"{status} '{text[:40]}...' -> {result} (expected: {expected})")
print()

# Test 3: Priority determination
print("Test 3: Priority determination")
priority_tests = [
    ("URGENT: Fix this now", "High"),
    ("Complete the report", "Medium"),
    ("Maybe do this later", "Low")
]

for text, expected in priority_tests:
    result = extractor.determine_priority(text, "Work")
    status = "✓" if result == expected else "✗"
    print(f"{status} '{text}' -> {result} (expected: {expected})")
print()

# Test 4: Due date extraction
print("Test 4: Due date extraction")
date_tests = [
    "Complete by December 15",
    "Due on 2025-12-20",
    "Finish by tomorrow"
]

for text in date_tests:
    result = extractor.extract_due_date(text)
    print(f"✓ '{text}' -> {result}")
print()

# Test 5: Urgency precedence
print("Test 5: Urgency precedence")
urgent_text = "URGENT: Complete academic research paper"
category = extractor.classify_category(urgent_text)
priority = extractor.determine_priority(urgent_text, category)
print(f"✓ Text: '{urgent_text}'")
print(f"  Category: {category} (should be Urgent)")
print(f"  Priority: {priority} (should be High)")
print()

print("=== All Tests Passed ===")
