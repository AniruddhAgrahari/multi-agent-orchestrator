/**
 * Daily Briefing Agent - Frontend JavaScript
 * ==========================================
 */

// Configuration (now loaded from config.js)
// These will be set after config.js loads
let API_BASE_URL = '';
let API_BASE = '';
let BRIEFING_ENDPOINT = '';

// Initialize configuration
function initializeConfig() {
    if (window.BRIEFING_CONFIG) {
        API_BASE_URL = window.BRIEFING_CONFIG.API_BASE_URL;
        API_BASE = window.BRIEFING_CONFIG.API_BASE;
        BRIEFING_ENDPOINT = window.BRIEFING_CONFIG.BRIEFING_ENDPOINT;
        
        if (window.BRIEFING_CONFIG.DEBUG_MODE) {
            console.log('🔧 API Configuration loaded:', {
                API_BASE_URL,
                API_BASE,
                BRIEFING_ENDPOINT
            });
        }
    } else {
        console.error('❌ BRIEFING_CONFIG not found. Make sure config.js is loaded.');
    }
}

// Global state
let currentBriefing = null;
let briefingHistory = [];
let currentHistoryId = null;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Daily Briefing Agent initialized');
    
    // Initialize configuration first
    initializeConfig();
    
    // Load saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    // Load briefing history
    loadBriefingHistory();
    
    // Add escape key handler for modal
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            hideLoading();
            closeSidebar();
        }
    });
    
    // Add click-outside-to-close for loading overlay
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.addEventListener('click', function(event) {
            if (event.target === this) {
                hideLoading();
            }
        });
    }
});

/**
 * Health check for API connectivity
 */
async function checkApiHealth() {
    if (!BRIEFING_ENDPOINT) {
        console.warn('⚠️ API endpoint not configured');
        return false;
    }
    
    try {
        const healthUrl = `${API_BASE_URL}/health`;
        const response = await fetch(healthUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            signal: AbortSignal.timeout(10000) // 10 second timeout
        });
        
        if (response.ok) {
            console.log('✅ API health check passed');
            return true;
        } else {
            console.warn('⚠️ API health check failed:', response.status);
            return false;
        }
    } catch (error) {
        console.warn('⚠️ API health check error:', error.message);
        return false;
    }
}

/**
 * Show API documentation
 */
function showApiDocs() {
    if (!API_BASE_URL) {
        showError('API endpoint not configured. Please check config.js');
        return;
    }
    
    const docsUrl = `${API_BASE_URL}/docs`;
    window.open(docsUrl, '_blank');
}

/**
 * Show health check status
 */
async function showHealthCheck() {
    const healthStatus = await checkApiHealth();
    const statusText = healthStatus ? 'API is healthy ✅' : 'API connection failed ❌';
    const statusClass = healthStatus ? 'success' : 'error';
    
    // Show status in a temporary notification
    showTemporaryNotification(statusText, statusClass);
}

/**
 * Show temporary notification
 */
function showTemporaryNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelectorAll('.temp-notification');
    existing.forEach(el => el.remove());
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `temp-notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        background: ${type === 'success' ? 'var(--success-color)' : 
                   type === 'error' ? 'var(--error-color)' : 
                   'var(--primary-color)'};
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}
async function generateBriefing() {
    console.log('🎯 generateBriefing() called');
    
    const queryElement = document.getElementById('briefingQuery');
    if (!queryElement) {
        alert('Error: Cannot find textarea element!');
        return;
    }
    
    const query = queryElement.value.trim();
    
    if (!query) {
        showToast('Please enter a briefing request', 'error');
        return;
    }
    
    console.log('📝 Query:', query);
    
    try {
        showLoading();
        
        // Step 1: Analyzing request
        updateLoadingStep(0, 'Analyzing your request...');
        await sleep(600);
        
        // Step 2: Gathering weather data
        updateLoadingStep(1, 'Gathering weather data...');
        await sleep(800);
        
        // Step 3: Collecting news updates
        updateLoadingStep(2, 'Collecting news updates...');
        await sleep(800);
        
        // Step 4: Making API call while showing "Synthesizing"
        updateLoadingStep(3, 'Synthesizing briefing...');
        
        const response = await fetch(BRIEFING_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        console.log('📡 Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Briefing generated successfully', data);
        
        // Mark all steps as completed
        updateLoadingStep(4, 'Briefing ready!');
        await sleep(800);
        
        hideLoading();
        
        // Handle different response formats
        if (data.success && data.content) {
            displayBriefing(data.content);
        } else if (data.briefing) {
            displayBriefing(data.briefing);
        } else {
            displayBriefing(data);
        }
        
        // Save to history
        saveBriefingToHistory(query, data.content || data.briefing || data);
        
        showToast('Briefing generated successfully!', 'success');
        
    } catch (error) {
        console.error('❌ Error generating briefing:', error);
        hideLoading();
        showToast(`Error: ${error.message}`, 'error');
    }
}

/**
 * Display briefing results
 */
function displayBriefing(data) {
    currentBriefing = data;
    
    const outputSection = document.getElementById('briefingOutput');
    const outputContent = document.getElementById('briefingContent');
    
    if (!outputSection || !outputContent) {
        console.error('Output elements not found');
        return;
    }
    
    // Handle different data formats
    let content = '';
    if (typeof data === 'string') {
        content = data;
    } else if (data && data.content) {
        content = data.content;
    } else if (data && data.briefing) {
        content = data.briefing;
    } else {
        content = String(data);
    }
    
    console.log('📄 Displaying content:', content.substring(0, 100) + '...');
    
    // Format content - convert markdown to HTML
    const formattedContent = formatBriefingContent(content);
    outputContent.innerHTML = formattedContent;
    
    // Show output section
    outputSection.style.display = 'flex';
    outputSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Format briefing content for better display
 */
function formatBriefingContent(content) {
    if (!content) return '';
    
    // Convert markdown-style formatting to HTML
    let formatted = content
        // Headers (## Header -> <h2>Header</h2>)
        .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
        // Bold text (**text** -> <strong>text</strong>)
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Bullet points (- item or * item -> <li>item</li>)
        .replace(/^[-*]\s+(.*?)$/gm, '<li>$1</li>')
        // Wrap consecutive list items in <ul> tags
        .replace(/(<li>.*?<\/li>\s*)+/gs, (match) => `<ul>${match}</ul>`)
        // Line breaks (double newlines become paragraph breaks)
        .replace(/\n\n/g, '</p><p>')
        // Single newlines become <br>
        .replace(/\n/g, '<br>');
    
    // Wrap content in paragraphs if it doesn't start with a header
    if (!formatted.startsWith('<h2>')) {
        formatted = '<p>' + formatted + '</p>';
    } else {
        // Add paragraph tags around content between headers
        formatted = formatted.replace(/(<\/h2>)(.*?)(?=<h2>|$)/gs, '$1<p>$2</p>');
    }
    
    // Clean up empty paragraphs
    formatted = formatted.replace(/<p><\/p>/g, '');
    formatted = formatted.replace(/<p>\s*<\/p>/g, '');
    
    return formatted;
}

/**
 * Loading Functions
 */
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

function updateLoadingStep(stepIndex, customText = null) {
    const steps = document.querySelectorAll('.step');
    const loadingText = document.getElementById('loadingText');
    
    // Update main loading text if provided
    if (customText && loadingText) {
        loadingText.textContent = customText;
    }
    
    // Update step highlighting
    steps.forEach((step, index) => {
        step.classList.remove('active', 'completed');
        
        if (stepIndex >= 4) {
            // All steps completed
            step.classList.add('completed');
        } else if (index < stepIndex) {
            // Previous steps are completed
            step.classList.add('completed');
        } else if (index === stepIndex) {
            // Current step is active
            step.classList.add('active');
        }
        // Future steps remain inactive
    });
}

// Helper function for delays
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Toast Notification Functions
 */
function showToast(message, type = 'success') {
    const toastId = type === 'error' ? 'errorToast' : 'successToast';
    const messageId = type === 'error' ? 'errorMessage' : 'successMessage';
    
    const toast = document.getElementById(toastId);
    const messageElement = document.getElementById(messageId);
    
    if (toast && messageElement) {
        messageElement.textContent = message;
        toast.style.display = 'flex';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            hideToast(toastId);
        }, 5000);
    }
}

function hideToast(toastId) {
    const toast = document.getElementById(toastId);
    if (toast) {
        toast.style.display = 'none';
    }
}

/**
 * Utility Functions
 */
function copyBriefing() {
    if (!currentBriefing) return;
    
    const content = currentBriefing.content || currentBriefing;
    navigator.clipboard.writeText(content).then(() => {
        showToast('Briefing copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Copy failed:', err);
        showToast('Failed to copy briefing', 'error');
    });
}

function downloadBriefing() {
    if (!currentBriefing) return;
    
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const filename = `daily-briefing-${timestamp}.txt`;
    
    const content = currentBriefing.content || currentBriefing;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast('Briefing downloaded successfully!', 'success');
}

/**
 * Theme Toggle Functions
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // Update the theme toggle icon
    const themeIcon = document.querySelector('.theme-icon');
    if (themeIcon) {
        themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
        themeIcon.classList.toggle('rotate', theme === 'dark');
    }
    
    console.log(`🎨 Theme switched to: ${theme}`);
}

/**
 * History Management Functions
 */

// Save briefing to history
function saveBriefingToHistory(query, content) {
    const briefing = {
        id: Date.now().toString(),
        title: generateBriefingTitle(query),
        query: query,
        content: content,
        timestamp: new Date().toISOString(),
        date: new Date().toLocaleDateString()
    };
    
    briefingHistory.unshift(briefing);
    
    // Keep only last 50 briefings
    if (briefingHistory.length > 50) {
        briefingHistory = briefingHistory.slice(0, 50);
    }
    
    // Save to localStorage
    localStorage.setItem('briefingHistory', JSON.stringify(briefingHistory));
    
    // Update UI
    renderHistoryList();
    
    // Set as current
    currentHistoryId = briefing.id;
    updateActiveHistoryItem();
    
    return briefing.id;
}

// Load briefing history from localStorage
function loadBriefingHistory() {
    try {
        const saved = localStorage.getItem('briefingHistory');
        if (saved) {
            briefingHistory = JSON.parse(saved);
        }
        renderHistoryList();
    } catch (error) {
        console.error('Error loading briefing history:', error);
        briefingHistory = [];
    }
}

// Generate a brief title from the query
function generateBriefingTitle(query) {
    if (!query) return 'Untitled Briefing';
    
    // Clean and truncate the query
    let title = query.trim();
    if (title.length > 60) {
        title = title.substring(0, 57) + '...';
    }
    
    // Capitalize first letter
    title = title.charAt(0).toUpperCase() + title.slice(1);
    
    return title;
}

// Render the history list
function renderHistoryList() {
    const historyList = document.getElementById('historyList');
    if (!historyList) return;
    
    if (briefingHistory.length === 0) {
        historyList.innerHTML = `
            <div style="padding: 2rem 1rem; text-align: center; color: var(--text-muted);">
                <p>No briefings yet</p>
                <p style="font-size: 0.85rem; margin-top: 0.5rem;">Your briefing history will appear here</p>
            </div>
        `;
        return;
    }
    
    historyList.innerHTML = briefingHistory.map(briefing => `
        <div class="history-item ${briefing.id === currentHistoryId ? 'active' : ''}" 
             onclick="loadBriefingFromHistory('${briefing.id}')"
             data-id="${briefing.id}">
            <button class="delete-btn" onclick="deleteBriefing(event, '${briefing.id}')" title="Delete briefing">
                ✕
            </button>
            <div class="title">${briefing.title}</div>
            <div class="date">${briefing.date}</div>
        </div>
    `).join('');
}

// Load a briefing from history
function loadBriefingFromHistory(briefingId) {
    const briefing = briefingHistory.find(b => b.id === briefingId);
    if (!briefing) return;
    
    // Update current state
    currentBriefing = briefing.content;
    currentHistoryId = briefingId;
    
    // Update UI
    document.getElementById('briefingQuery').value = briefing.query;
    displayBriefing(briefing.content);
    updateActiveHistoryItem();
    
    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
        closeSidebar();
    }
}

// Delete a briefing from history
function deleteBriefing(event, briefingId) {
    event.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this briefing?')) {
        return;
    }
    
    briefingHistory = briefingHistory.filter(b => b.id !== briefingId);
    localStorage.setItem('briefingHistory', JSON.stringify(briefingHistory));
    
    // If we deleted the current briefing, clear the display
    if (currentHistoryId === briefingId) {
        currentHistoryId = null;
        currentBriefing = null;
        document.getElementById('briefingQuery').value = '';
        const outputSection = document.getElementById('briefingOutput');
        if (outputSection) {
            outputSection.style.display = 'none';
        }
    }
    
    renderHistoryList();
    showToast('Briefing deleted', 'success');
}

// Update active history item styling
function updateActiveHistoryItem() {
    const historyItems = document.querySelectorAll('.history-item');
    historyItems.forEach(item => {
        item.classList.toggle('active', item.dataset.id === currentHistoryId);
    });
}

// Search history
function searchHistory(query) {
    const historyItems = document.querySelectorAll('.history-item');
    const searchTerm = query.toLowerCase().trim();
    
    historyItems.forEach(item => {
        const title = item.querySelector('.title').textContent.toLowerCase();
        const isMatch = title.includes(searchTerm);
        item.style.display = isMatch ? 'block' : 'none';
    });
}

// Create new briefing
function newBriefing() {
    currentBriefing = null;
    currentHistoryId = null;
    
    // Clear form and output
    document.getElementById('briefingQuery').value = '';
    const outputSection = document.getElementById('briefingOutput');
    if (outputSection) {
        outputSection.style.display = 'none';
    }
    
    // Update history UI
    updateActiveHistoryItem();
    
    // Focus on textarea
    document.getElementById('briefingQuery').focus();
    
    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
        closeSidebar();
    }
}

/**
 * Sidebar Functions
 */

// Toggle sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const contentWrapper = document.getElementById('contentWrapper');
    const backdrop = document.getElementById('sidebarBackdrop');
    
    const isOpen = sidebar.classList.contains('open');
    
    if (isOpen) {
        closeSidebar();
    } else {
        openSidebar();
    }
}

// Open sidebar
function openSidebar() {
    const sidebar = document.getElementById('sidebar');
    const contentWrapper = document.getElementById('contentWrapper');
    const backdrop = document.getElementById('sidebarBackdrop');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    
    sidebar.classList.add('open');
    sidebarToggle.classList.add('sidebar-open');
    
    if (window.innerWidth > 768) {
        contentWrapper.classList.add('sidebar-open');
    } else {
        backdrop.classList.add('active');
    }
}

// Close sidebar
function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const contentWrapper = document.getElementById('contentWrapper');
    const backdrop = document.getElementById('sidebarBackdrop');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    
    sidebar.classList.remove('open');
    contentWrapper.classList.remove('sidebar-open');
    backdrop.classList.remove('active');
    sidebarToggle.classList.remove('sidebar-open');
}

// Handle window resize
window.addEventListener('resize', function() {
    const sidebar = document.getElementById('sidebar');
    const contentWrapper = document.getElementById('contentWrapper');
    const backdrop = document.getElementById('sidebarBackdrop');
    
    if (window.innerWidth > 768) {
        backdrop.classList.remove('active');
        if (sidebar.classList.contains('open')) {
            contentWrapper.classList.add('sidebar-open');
        }
    } else {
        contentWrapper.classList.remove('sidebar-open');
        if (sidebar.classList.contains('open')) {
            backdrop.classList.add('active');
        }
    }
});
