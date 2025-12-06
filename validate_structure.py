"""
Simple validation script that checks project structure without importing modules.
"""

import os
import json

print("=" * 70)
print("PROJECT STRUCTURE VALIDATION")
print("=" * 70)
print()

# Check all required files
print("Checking required files...")
required_files = {
    'Backend': [
        'app.py',
        'task_store.py',
        'task_extractor.py',
        'kiro_email_hook.py'
    ],
    'Frontend': [
        'static/index.html',
        'static/styles.css',
        'static/app.js'
    ],
    'Configuration': [
        'requirements.txt',
        '.env.example',
        '.gitignore'
    ],
    'Documentation': [
        'README.md',
        'examples/sample_emails.json',
        'examples/test_commands.txt'
    ],
    'Kiro': [
        '.kiro/hooks/email_hook.json'
    ]
}

all_present = True
for category, files in required_files.items():
    print(f"\n{category}:")
    for file in files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ MISSING: {file}")
            all_present = False

print()
if all_present:
    print("✓ All required files present!")
else:
    print("✗ Some files are missing")
    exit(1)

# Validate JSON files
print("\nValidating JSON files...")
json_files = [
    'examples/sample_emails.json',
    'examples/sample_email_urgent.json',
    'examples/sample_email_personal.json',
    'examples/sample_email_academic.json',
    '.kiro/hooks/email_hook.json'
]

all_valid = True
for json_file in json_files:
    try:
        with open(json_file, 'r') as f:
            json.load(f)
        print(f"  ✓ {json_file}")
    except Exception as e:
        print(f"  ✗ {json_file}: {e}")
        all_valid = False

print()
if all_valid:
    print("✓ All JSON files valid!")
else:
    print("✗ Some JSON files invalid")
    exit(1)

# Check file sizes (basic sanity check)
print("\nChecking file sizes...")
size_checks = {
    'app.py': 3000,
    'task_store.py': 3000,
    'task_extractor.py': 5000,
    'static/index.html': 1000,
    'static/styles.css': 3000,
    'static/app.js': 5000,
    'README.md': 3000
}

for file, min_size in size_checks.items():
    size = os.path.getsize(file)
    if size >= min_size:
        print(f"  ✓ {file}: {size} bytes")
    else:
        print(f"  ⚠ {file}: {size} bytes (expected at least {min_size})")

print()
print("=" * 70)
print("✓ PROJECT STRUCTURE VALIDATED SUCCESSFULLY")
print("=" * 70)
print()
print("Next steps:")
print("1. Run setup.bat to install dependencies")
print("2. Copy .env.example to .env and add your OpenAI API key")
print("3. Run: python app.py")
print("4. Open: http://localhost:8000")
print()
