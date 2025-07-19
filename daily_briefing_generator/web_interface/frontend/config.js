/**
 * Daily Briefing Agent - Configuration
 * ====================================
 * 
 * Environment-specific configuration for the Daily Briefing Agent.
 * Update these settings based on your deployment environment.
 */

// Environment detection
const isLocalhost = window.location.hostname === 'localhost' || 
                   window.location.hostname === '127.0.0.1' || 
                   window.location.hostname === '';

const isGitHubPages = window.location.hostname.includes('github.io');

// API Configuration
const API_CONFIG = {
    // Local development
    local: {
        baseUrl: 'https://multi-agent-orchestrator.onrender.com',  // Temporarily using Render for testing
        apiBase: '/api/v1'
    },
    
    // GitHub Pages with external API
    production: {
        // Update this URL to your actual API endpoint
        // Options:
        // 1. Deploy backend to Heroku, Railway, Render, etc.
        // 2. Use Netlify Functions, Vercel API Routes
        // 3. Use a serverless provider like AWS Lambda
        baseUrl: 'https://multi-agent-orchestrator.onrender.com',  // Replace with your actual Render URL
        apiBase: '/api/v1'
    }
};

// Select configuration based on environment
const currentConfig = isLocalhost ? API_CONFIG.local : API_CONFIG.production;

// Export configuration
window.BRIEFING_CONFIG = {
    API_BASE_URL: currentConfig.baseUrl,
    API_BASE: currentConfig.apiBase,
    BRIEFING_ENDPOINT: `${currentConfig.baseUrl}${currentConfig.apiBase}/briefing`,
    
    // Feature flags
    ENABLE_HISTORY: true,
    ENABLE_DARK_MODE: true,
    ENABLE_API_DOCS: true,
    
    // UI Configuration
    MAX_HISTORY_ITEMS: 50,
    AUTO_SAVE_HISTORY: true,
    
    // Debug mode (only for localhost)
    DEBUG_MODE: isLocalhost
};

// Log configuration (only in development)
if (window.BRIEFING_CONFIG.DEBUG_MODE) {
    console.log('🔧 Briefing Config:', window.BRIEFING_CONFIG);
}
