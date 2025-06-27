/**
 * Daily Briefing Agent - Interactive Frontend (Fixed Version)
 * ==========================================
 * 
 * Professional JavaScript for the Daily Briefing Agent web interface.
 * Handles API communication, UI interactions, and real-time updates.
 */

// Configuration
const API_BASE = '/api/v1';
const ENDPOINTS = {
    briefing: `${API_BASE}/briefing`,
    quickBriefing: `${API_BASE}/briefing/quick`,
    templates: `${API_BASE}/briefing/templates`,
    health: `${API_BASE}/health`,
    healthDetailed: `${API_BASE}/health/detailed`
};

// Global state
let currentBriefing = null;
let systemStatus = null;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Daily Briefing Agent initialized');
    
    // Load initial data
    loadTemplates();
    checkSystemHealth();
    
    // Set up periodic health checks
    setInterval(checkSystemHealth, 30000); // Every 30 seconds
    
    // Add escape key handler for modals
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            hideLoading();
            closeModal('statusModal');
        }
    });
    
    // Add click-outside-to-close for loading overlay
    document.getElementById('loadingOverlay').addEventListener('click', function(event) {
        if (event.target === this) {
            hideLoading();
        }
    });
});

// Debug function to test button click
window.testButton = function() {
    console.log('🧪 Test button clicked!');
    alert('Button click is working!');
};

// Debug function to test generateBriefing
window.testGenerateBriefing = function() {
    console.log('🧪 Testing generateBriefing function...');
    document.getElementById('briefingQuery').value = 'Test briefing request';
    generateBriefing();
};

/**
 * Streamlined Briefing Generation - Fixed Version
 */
function generateBriefing() {
    alert('Generate briefing function called!');
    console.log('Generate briefing function called!');
    
    const textarea = document.getElementById('briefingQuery');
    if (!textarea) {
        alert('Textarea not found!');
        return;
    }
    
    const value = textarea.value.trim();
    if (!value) {
        alert('Please enter a briefing request');
        return;
    }
    
    alert('About to make API call with: ' + value);
    
    // Make the actual API call
    fetch('/api/v1/briefing', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: value,
            use_recovery: true
        })
    })
    .then(response => {
        alert('Got response with status: ' + response.status);
        return response.json();
    })
    .then(data => {
        alert('Got data: ' + JSON.stringify(data).substring(0, 100));
        if (data.success) {
            document.getElementById('outputContent').innerHTML = data.content;
            document.getElementById('resultsSection').style.display = 'block';
        }
    })
    .catch(error => {
        alert('Error: ' + error.message);
    });
}

/**
 * Display briefing results
 */
function displayBriefing(data) {
    currentBriefing = data;
    
    const resultsSection = document.getElementById('resultsSection');
    const outputMeta = document.getElementById('outputMeta');
    const outputContent = document.getElementById('outputContent');
    
    // Format metadata
    const metadata = data.metadata || {};
    const metaText = [
        `Query: ${metadata.query || data.query || 'N/A'}`,
        metadata.location ? `Location: ${metadata.location}` : '',
        metadata.categories ? `Categories: ${metadata.categories.join(', ')}` : '',
        metadata.recovery_enabled ? 'Error recovery: Enabled' : 'Error recovery: Disabled'
    ].filter(Boolean).join(' | ');
    
    outputMeta.textContent = metaText;
    
    // Format content with better readability
    const formattedContent = formatBriefingContent(data.content);
    outputContent.innerHTML = formattedContent;
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Format briefing content for better display
 */
function formatBriefingContent(content) {
    // Convert markdown-style formatting to HTML
    let formatted = content
        // Headers
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Line breaks
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    return `<p>${formatted}</p>`;
}

/**
 * Utility Functions
 */
function copyBriefing() {
    if (!currentBriefing) return;
    
    navigator.clipboard.writeText(currentBriefing.content).then(() => {
        showSuccess('Briefing copied to clipboard');
    }).catch(() => {
        showError('Failed to copy briefing');
    });
}

function downloadBriefing() {
    if (!currentBriefing) return;
    
    const blob = new Blob([currentBriefing.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `daily-briefing-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showSuccess('Briefing downloaded');
}

/**
 * Status and Health Functions
 */
function showHealthStatus() {
    if (!systemStatus) {
        showError('System status not available');
        return;
    }
    
    const modal = document.getElementById('statusModal');
    const statusContent = document.getElementById('statusContent');
    
    statusContent.innerHTML = `
        <div class="status-item">
            <strong>Status:</strong> 
            <span class="${systemStatus.status === 'healthy' ? 'status-healthy' : 'status-error'}">
                ${systemStatus.status}
            </span>
        </div>
        <div class="status-item">
            <strong>Uptime:</strong> ${Math.round(systemStatus.uptime / 60)} minutes
        </div>
        <div class="status-item">
            <strong>Version:</strong> ${systemStatus.version}
        </div>
    `;
    
    modal.style.display = 'flex';
}

async function checkSystemHealth() {
    try {
        const response = await fetch(ENDPOINTS.health);
        const data = await response.json();
        systemStatus = data;
        
        // Update status indicator if it exists
        const statusIndicator = document.querySelector('.status-indicator');
        if (statusIndicator) {
            statusIndicator.className = `status-indicator ${data.status === 'healthy' ? 'healthy' : 'error'}`;
        }
        
    } catch (error) {
        console.warn('Health check failed:', error);
        systemStatus = { status: 'error', error: error.message };
    }
}

/**
 * Template Management
 */
async function loadTemplates() {
    try {
        const response = await fetch(ENDPOINTS.templates);
        const data = await response.json();
        
        // Could populate template suggestions in the UI
        console.log('Templates loaded:', data);
        
    } catch (error) {
        console.warn('Failed to load templates:', error);
    }
}

/**
 * UI Helper Functions
 */
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'flex';
    
    // Reset loading steps
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        step.classList.toggle('active', index === 0);
    });
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'none';
}

function updateLoadingStep(stepIndex) {
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        step.classList.toggle('active', index === stepIndex);
    });
}

function showSuccess(message) {
    const toast = document.getElementById('successToast');
    const messageEl = document.getElementById('successMessage');
    
    messageEl.textContent = message;
    toast.style.display = 'flex';
    
    setTimeout(() => {
        hideToast('successToast');
    }, 5000);
}

function showError(message) {
    const toast = document.getElementById('errorToast');
    const messageEl = document.getElementById('errorMessage');
    
    messageEl.textContent = message;
    toast.style.display = 'flex';
    
    setTimeout(() => {
        hideToast('errorToast');
    }, 8000);
}

function hideToast(toastId) {
    const toast = document.getElementById(toastId);
    toast.style.display = 'none';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

function showApiDocs() {
    window.open('/docs', '_blank');
}
