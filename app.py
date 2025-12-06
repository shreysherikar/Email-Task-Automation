"""
Flask Application for Email-to-Task Automation System
Provides REST API endpoints for task management and email ingestion.
"""

import os
from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from task_store import TaskStore
from task_extractor import TaskExtractor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Initialize components
task_store = TaskStore()
task_extractor = TaskExtractor()

# Configuration
PORT = int(os.getenv('FLASK_PORT', 8000))


@app.route('/')
def index():
    """Serve dashboard HTML (GET /)"""
    try:
        return send_from_directory('static', 'index.html')
    except Exception as e:
        return jsonify({"error": "Dashboard not found", "details": str(e)}), 404


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    try:
        return send_from_directory('static', filename)
    except Exception as e:
        return jsonify({"error": "File not found", "details": str(e)}), 404


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks as JSON (GET /tasks)"""
    try:
        tasks = task_store.load_tasks()
        return jsonify({
            "success": True,
            "tasks": tasks,
            "count": len(tasks)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to load tasks",
            "details": str(e)
        }), 500


@app.route('/tasks/complete/<task_id>', methods=['POST'])
def complete_task(task_id):
    """Mark task as done (POST /tasks/complete/<id>)"""
    try:
        # Validate task exists
        task = task_store.get_task_by_id(task_id)
        if not task:
            return jsonify({
                "success": False,
                "error": f"Task not found: {task_id}"
            }), 404
        
        # Update status
        success = task_store.update_task_status(task_id, 'done')
        
        if success:
            updated_task = task_store.get_task_by_id(task_id)
            return jsonify({
                "success": True,
                "message": "Task marked as complete",
                "task": updated_task
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Failed to update task status"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Error completing task",
            "details": str(e)
        }), 500


@app.route('/ingest-email', methods=['POST'])
def ingest_email():
    """
    Process incoming email and extract tasks (POST /ingest-email)
    Expected payload: {"subject": str, "body": str, "sender": str}
    """
    try:
        # Validate payload
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON payload provided"
            }), 400
        
        # Check required fields
        required_fields = ['subject', 'body', 'sender']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        subject = data['subject']
        body = data['body']
        sender = data['sender']
        
        # Extract tasks using LLM
        print(f"Processing email from {sender}: {subject}")
        extracted_tasks = task_extractor.extract_tasks_from_email(subject, body, sender)
        
        # Store tasks (with duplicate checking)
        added_tasks = []
        duplicate_tasks = []
        
        for task in extracted_tasks:
            if task_store.add_task(task):
                added_tasks.append(task)
            else:
                duplicate_tasks.append(task.get('description', 'Unknown'))
        
        return jsonify({
            "success": True,
            "message": f"Processed email and extracted {len(extracted_tasks)} tasks",
            "added": len(added_tasks),
            "duplicates": len(duplicate_tasks),
            "tasks": added_tasks,
            "duplicate_descriptions": duplicate_tasks
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Error processing email",
            "details": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Email-to-Task Automation",
        "version": "1.0.0"
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("=" * 50)
    print("Email-to-Task Automation System")
    print("=" * 50)
    print(f"Starting Flask server on port {PORT}...")
    print(f"Dashboard: http://localhost:{PORT}")
    print(f"API Endpoints:")
    print(f"  GET  /tasks - List all tasks")
    print(f"  POST /tasks/complete/<id> - Mark task complete")
    print(f"  POST /ingest-email - Process email")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=PORT, debug=True)
