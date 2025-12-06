"""Simple test without external dependencies."""

import sys
import os

# Test the core logic without OpenAI
print("=== Testing Task Extractor Core Logic ===\n")

# Test category classification logic
def classify_category_test(task_text):
    task_lower = task_text.lower()
    urgency_keywords = ['urgent', 'asap', 'critical', 'emergency', 'immediately', 'now']
    if any(keyword in task_lower for keyword in urgency_keywords):
        return "Urgent"
    if any(word in task_lower for word in ['meeting', 'report', 'project', 'client', 'presentation']):
        return "Work"
    elif any(word in task_lower for word in ['research', 'paper', 'study', 'assignment']):
        return "Academic"
    elif any(word in task_lower for word in ['family', 'personal', 'home', 'grocery']):
        return "Personal"
    elif any(word in task_lower for word in ['later', 'sometime', 'eventually']):
        return "Low Priority"
    return "Work"

# Test priority determination
def determine_priority_test(task_text, category):
    task_lower = task_text.lower()
    high_priority_keywords = ['urgent', 'asap', 'critical', 'important', 'priority', 'immediately']
    if any(keyword in task_lower for keyword in high_priority_keywords):
        return "High"
    if category == "Urgent":
        return "High"
    low_priority_keywords = ['later', 'sometime', 'eventually', 'when possible', 'optional']
    if any(keyword in task_lower for keyword in low_priority_keywords):
        return "Low"
    return "Medium"

print("Test 1: Category Classification")
test_cases = [
    ("URGENT: Server is down", "Urgent"),
    ("Complete research paper for class", "Academic"),
    ("Buy groceries for dinner", "Personal"),
    ("Prepare client presentation", "Work"),
    ("Maybe update the docs sometime", "Low Priority")
]

all_passed = True
for text, expected in test_cases:
    result = classify_category_test(text)
    status = "✓" if result == expected else "✗"
    if result != expected:
        all_passed = False
    print(f"{status} '{text[:40]}...' -> {result} (expected: {expected})")
print()

print("Test 2: Priority Determination")
priority_tests = [
    ("URGENT: Fix this now", "High"),
    ("Complete the report", "Medium"),
    ("Maybe do this later", "Low")
]

for text, expected in priority_tests:
    result = determine_priority_test(text, "Work")
    status = "✓" if result == expected else "✗"
    if result != expected:
        all_passed = False
    print(f"{status} '{text}' -> {result} (expected: {expected})")
print()

print("Test 3: Urgency Precedence")
urgent_text = "URGENT: Complete academic research paper"
category = classify_category_test(urgent_text)
priority = determine_priority_test(urgent_text, category)
print(f"✓ Text: '{urgent_text}'")
print(f"  Category: {category} (should be Urgent)")
print(f"  Priority: {priority} (should be High)")
urgent_correct = category == "Urgent" and priority == "High"
if not urgent_correct:
    all_passed = False
print()

if all_passed:
    print("=== All Core Logic Tests Passed ===")
else:
    print("=== Some Tests Failed ===")
    sys.exit(1)
