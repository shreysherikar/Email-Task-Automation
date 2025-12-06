"""
Clean up task descriptions by removing excessive formatting and truncating long text.
"""
import json
import re

def clean_text(text):
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove carriage returns and normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove multiple consecutive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove excessive spaces
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(line for line in lines if line)
    
    return text.strip()

def truncate_description(desc, max_length=300):
    """Truncate description to reasonable length."""
    desc = clean_text(desc)
    if len(desc) > max_length:
        return desc[:max_length] + "..."
    return desc

# Load tasks
with open('data/tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Clean each task
for task in data['tasks']:
    task['description'] = truncate_description(task['description'])
    
    # Also clean subject
    if 'source_email' in task and 'subject' in task['source_email']:
        task['source_email']['subject'] = clean_text(task['source_email']['subject'])

# Save cleaned tasks
with open('data/tasks.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✓ Tasks cleaned successfully!")
print(f"  Total tasks: {len(data['tasks'])}")
