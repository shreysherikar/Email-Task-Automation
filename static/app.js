// Global state
let allTasks = [];
let filteredTasks = [];
let categoryChart = null;
let senderChart = null;

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing app...');
    initializeApp();
});

async function initializeApp() {
    console.log('Initializing app...');
    
    // Load dark mode preference
    loadDarkModePreference();
    
    // Set up event listeners
    setupEventListeners();
    
    // Fetch and display tasks
    await fetchTasks();
}

function setupEventListeners() {
    console.log('Setting up event listeners...');
    
    // Dark mode toggle
    const darkModeBtn = document.getElementById('darkModeToggle');
    if (darkModeBtn) {
        darkModeBtn.addEventListener('click', toggleDarkMode);
    }
    
    // Filters
    const categoryFilter = document.getElementById('categoryFilter');
    const statusFilter = document.getElementById('statusFilter');
    const urgencyFilter = document.getElementById('urgencyFilter');
    const clearBtn = document.getElementById('clearFilters');
    
    if (categoryFilter) categoryFilter.addEventListener('change', applyFilters);
    if (statusFilter) statusFilter.addEventListener('change', applyFilters);
    if (urgencyFilter) urgencyFilter.addEventListener('change', applyFilters);
    if (clearBtn) clearBtn.addEventListener('click', clearFilters);
}

// Fetch tasks from API
async function fetchTasks() {
    console.log('Fetching tasks from API...');
    
    try {
        const response = await fetch('/tasks');
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Data received:', data);
        
        if (data.success && data.tasks) {
            allTasks = data.tasks;
            filteredTasks = [...allTasks];
            console.log(`Loaded ${allTasks.length} tasks`);
            renderAll();
        } else {
            console.error('Invalid data format:', data);
            showError('Invalid data format received from server');
        }
    } catch (error) {
        console.error('Error fetching tasks:', error);
        showError('Error connecting to server: ' + error.message);
    }
}

// Render all components
function renderAll() {
    console.log('Rendering all components...');
    renderMetrics(filteredTasks);
    renderTasks(filteredTasks);
    renderCharts(filteredTasks);
}

// Render metrics
function renderMetrics(tasks) {
    const total = tasks.length;
    const pending = tasks.filter(t => t.status === 'pending').length;
    const completed = tasks.filter(t => t.status === 'done').length;
    const urgent = tasks.filter(t => t.category === 'Urgent').length;
    
    const totalEl = document.getElementById('totalTasks');
    const pendingEl = document.getElementById('pendingTasks');
    const completedEl = document.getElementById('completedTasks');
    const urgentEl = document.getElementById('urgentTasks');
    
    if (totalEl) totalEl.textContent = total;
    if (pendingEl) pendingEl.textContent = pending;
    if (completedEl) completedEl.textContent = completed;
    if (urgentEl) urgentEl.textContent = urgent;
    
    console.log(`Metrics: Total=${total}, Pending=${pending}, Completed=${completed}, Urgent=${urgent}`);
}

// Render tasks list
function renderTasks(tasks) {
    const tasksList = document.getElementById('tasksList');
    
    if (!tasksList) {
        console.error('tasksList element not found!');
        return;
    }
    
    if (tasks.length === 0) {
        tasksList.innerHTML = `
            <div class="empty-state">
                <h3>No tasks found</h3>
                <p>Try adjusting your filters or add new tasks via email ingestion</p>
            </div>
        `;
        return;
    }
    
    tasksList.innerHTML = tasks.map(task => createTaskCard(task)).join('');
    
    // Add event listeners to complete buttons
    tasks.forEach(task => {
        const btn = document.getElementById(`complete-${task.id}`);
        if (btn) {
            btn.addEventListener('click', () => completeTask(task.id));
        }
    });
    
    console.log(`Rendered ${tasks.length} tasks`);
}

// Create task card HTML
function createTaskCard(task) {
    const isDone = task.status === 'done';
    const dueDate = task.due_date ? new Date(task.due_date).toLocaleDateString() : 'No due date';
    
    return `
        <div class="task-card ${isDone ? 'done' : ''}" data-category="${escapeHtml(task.category)}">
            <div class="task-header">
                <div class="task-description">${escapeHtml(task.description)}</div>
            </div>
            <div class="task-meta">
                <span class="task-badge badge-category">${escapeHtml(task.category)}</span>
                <span class="task-badge badge-priority">${escapeHtml(task.priority)} Priority</span>
                <span class="task-badge badge-sender">📧 ${escapeHtml(task.sender)}</span>
                ${task.due_date ? `<span class="task-badge badge-date">📅 ${dueDate}</span>` : ''}
            </div>
            <div class="task-actions">
                <button 
                    id="complete-${task.id}" 
                    class="btn-complete" 
                    ${isDone ? 'disabled' : ''}
                >
                    ${isDone ? '✓ Completed' : 'Mark Complete'}
                </button>
            </div>
        </div>
    `;
}

// Complete task
async function completeTask(taskId) {
    try {
        const response = await fetch(`/tasks/complete/${taskId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update local state
            const task = allTasks.find(t => t.id === taskId);
            if (task) {
                task.status = 'done';
            }
            
            // Re-apply filters and re-render
            applyFilters();
            console.log(`Task ${taskId} marked as complete`);
        } else {
            console.error('Failed to complete task:', data.error);
            alert('Failed to complete task: ' + data.error);
        }
    } catch (error) {
        console.error('Error completing task:', error);
        alert('Error completing task');
    }
}

// Apply filters
function applyFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const statusFilter = document.getElementById('statusFilter');
    const urgencyFilter = document.getElementById('urgencyFilter');
    
    const categoryValue = categoryFilter ? categoryFilter.value : 'all';
    const statusValue = statusFilter ? statusFilter.value : 'all';
    const urgencyChecked = urgencyFilter ? urgencyFilter.checked : false;
    
    filteredTasks = allTasks.filter(task => {
        // Category filter
        if (categoryValue !== 'all' && task.category !== categoryValue) {
            return false;
        }
        
        // Status filter
        if (statusValue !== 'all' && task.status !== statusValue) {
            return false;
        }
        
        // Urgency filter
        if (urgencyChecked && task.category !== 'Urgent') {
            return false;
        }
        
        return true;
    });
    
    console.log(`Filtered to ${filteredTasks.length} tasks`);
    renderAll();
}

// Clear filters
function clearFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const statusFilter = document.getElementById('statusFilter');
    const urgencyFilter = document.getElementById('urgencyFilter');
    
    if (categoryFilter) categoryFilter.value = 'all';
    if (statusFilter) statusFilter.value = 'all';
    if (urgencyFilter) urgencyFilter.checked = false;
    
    filteredTasks = [...allTasks];
    renderAll();
}

// Render charts
function renderCharts(tasks) {
    renderPieChart(tasks);
    renderBarChart(tasks);
}

// Render pie chart (category distribution)
function renderPieChart(tasks) {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;
    
    // Count tasks by category
    const categoryCounts = {};
    tasks.forEach(task => {
        categoryCounts[task.category] = (categoryCounts[task.category] || 0) + 1;
    });
    
    const labels = Object.keys(categoryCounts);
    const data = Object.values(categoryCounts);
    
    // Destroy existing chart
    if (categoryChart) {
        categoryChart.destroy();
    }
    
    // Create new chart
    categoryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#A8B5FF',
                    '#E5A8FF',
                    '#FFD4A3',
                    '#FFB4B4',
                    '#A8E6CF'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Render bar chart (tasks per sender)
function renderBarChart(tasks) {
    const ctx = document.getElementById('senderChart');
    if (!ctx) return;
    
    // Count tasks by sender
    const senderCounts = {};
    tasks.forEach(task => {
        senderCounts[task.sender] = (senderCounts[task.sender] || 0) + 1;
    });
    
    // Sort by count and take top 10
    const sortedSenders = Object.entries(senderCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    const labels = sortedSenders.map(([sender]) => sender);
    const data = sortedSenders.map(([, count]) => count);
    
    // Destroy existing chart
    if (senderChart) {
        senderChart.destroy();
    }
    
    // Create new chart
    senderChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tasks',
                data: data,
                backgroundColor: '#A8B5FF'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Dark mode functions
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    saveDarkModePreference();
    
    // Update button icon
    const btn = document.getElementById('darkModeToggle');
    if (btn) {
        btn.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
    }
}

function loadDarkModePreference() {
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
        const btn = document.getElementById('darkModeToggle');
        if (btn) btn.textContent = '☀️';
    }
}

function saveDarkModePreference() {
    const darkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', darkMode);
}

// Utility functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showError(message) {
    const tasksList = document.getElementById('tasksList');
    if (tasksList) {
        tasksList.innerHTML = `
            <div class="empty-state">
                <h3>Error</h3>
                <p>${escapeHtml(message)}</p>
                <button onclick="location.reload()" class="btn-secondary">Reload Page</button>
            </div>
        `;
    }
    console.error(message);
}
