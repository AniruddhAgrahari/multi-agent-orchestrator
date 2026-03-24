git add CLAUDE.md
git commit -m "docs: add comprehensive CLAUDE.md AI context file"
git pushgit add CLAUDE.md
git commit -m "docs: add comprehensive CLAUDE.md AI context file"
git push# CLAUDE.md - Multi-Agent Orchestrator Project Context

> **Last Updated:** 2026-03-24
> **Project:** Synoptic AI: Daily Briefing Agent
> **Version:** 1.0.0

This file provides comprehensive context about the multi-agent orchestrator project for AI assistants. It helps maintain consistency across different AI models and development sessions.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & System Design](#architecture--system-design)
3. [Directory Structure](#directory-structure)
4. [Code Patterns & Conventions](#code-patterns--conventions)
5. [Key Components Reference](#key-components-reference)
6. [Configuration & Environment](#configuration--environment)
7. [Development Workflows](#development-workflows)
8. [Testing Guidance](#testing-guidance)
9. [Common Issues & Solutions](#common-issues--solutions)
10. [Design Philosophy](#design-philosophy)
11. [What NOT to Do](#what-not-to-do)
12. [Quick Reference Commands](#quick-reference-commands)

---

## Project Overview

### What is This Project?

**Synoptic AI: Multi-Agent Orchestrator** is a production-ready AI-powered daily briefing generation system that orchestrates multiple specialized intelligent agents to deliver comprehensive executive-level briefings.

### Core Capabilities

- 🌤️ **Real-time Weather Data**: Location-aware weather briefings with business implications
- 📰 **Curated News Updates**: Multi-source news aggregation across categories (tech, business, health, sports)
- 🧠 **AI-Synthesized Insights**: Executive-level briefings combining weather + news with actionable recommendations
- 🔄 **Error Recovery**: Three-tier recovery system (master → agent → tool level)
- 🌐 **Web Interface**: Ultra-minimal dark/light mode frontend with history management

### Technology Stack

**Backend:**
- **Language**: Python 3.8+
- **Framework**: FastAPI (REST API)
- **Server**: Uvicorn (ASGI)
- **AI/ML**: Google Generative AI (Gemini Flash Lite)
- **Async**: asyncio, aiohttp
- **Config**: python-dotenv, Pydantic

**Frontend:**
- **Pure Vanilla JavaScript** (no frameworks)
- **HTML5/CSS3** with modern CSS Grid/Flexbox
- **Dark/Light Mode** with localStorage persistence
- **Responsive Design** (mobile-first)

**External APIs:**
- **Weather**: OpenWeatherMap API
- **News**: Multi-API system (NewsAPI, GNews, NewsData.io, MediaStack, Currents, WorldNews, NewsCatcher, RSS feeds)
- **AI**: Google AI Studio (Gemini)

**Deployment:**
- **Frontend**: GitHub Pages (https://AniruddhAgrahari.github.io/multi-agent-orchestrator/)
- **Backend**: Render.com (https://multi-agent-orchestrator.onrender.com)
- **CI/CD**: GitHub Actions

### Live Demo

🔗 **Production URL**: https://AniruddhAgrahari.github.io/multi-agent-orchestrator/

---

## Architecture & System Design

### Multi-Agent Architecture

The system follows a **hierarchical multi-agent pattern** with specialized agents coordinated by a master orchestrator:

```
┌─────────────────────────────────────────────────────┐
│              USER REQUEST                            │
│  "Morning briefing for Mumbai with tech news"       │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│           MASTER AGENT                               │
│  - Analyzes user intent                             │
│  - Extracts location & categories                   │
│  - Delegates to specialized agents                  │
│  - Synthesizes final briefing                       │
│  - Handles errors & recovery                        │
└──────────────┬───────────────────┬──────────────────┘
               │                   │
        ┌──────▼──────┐    ┌──────▼──────┐
        │   WEATHER   │    │    NEWS     │
        │    AGENT    │    │   AGENT     │
        │             │    │             │
        │ Location    │    │ Category    │
        │ Extraction  │    │ Detection   │
        │ Natural     │    │ Multi-API   │
        │ Language    │    │ Fallback    │
        └──────┬──────┘    └──────┬──────┘
               │                   │
        ┌──────▼──────┐    ┌──────▼──────┐
        │  WEATHER    │    │    NEWS     │
        │    TOOL     │    │    TOOL     │
        │             │    │             │
        │ OpenWeather │    │ 7 APIs +    │
        │ API         │    │ RSS Feeds   │
        └─────────────┘    └─────────────┘
```

### Three-Tier Output Format

**Every briefing must contain exactly three sections:**

1. **Detailed Weather Report** - Weather data with business/travel implications
2. **News Digest** - Category-organized news with business relevance
3. **Actionable Insights** - Recommendations based on weather + news correlation

⚠️ **CRITICAL**: No additional sections (no "OPENING", no "CLOSING", no "EXECUTIVE SUMMARY", no "OUTLOOK")

### Error Recovery Hierarchy

**Three-layer recovery system:**

1. **Master-Level Recovery** (`run_with_recovery()`)
   - 3 retry attempts with exponential backoff
   - Timeout: 30 seconds
   - Handles complete system failures

2. **Agent-Level Recovery** (`process_request_with_agent_recovery()`)
   - Individual agent timeouts: 15 seconds each
   - Partial briefings if one agent fails
   - Graceful degradation

3. **Tool-Level Recovery** (in news_tool.py)
   - Multi-API fallback chain
   - Broader search strategies
   - Fallback countries and categories

### Async-First Design

- **All I/O operations are async**: Never use synchronous requests
- **Concurrent execution**: `asyncio.gather()` for parallel API calls
- **Timeout handling**: Every async operation has explicit timeout
- **Error propagation**: Proper exception handling at every level

### Location-Aware Processing

- Extracts location from user query (city, country)
- Applies location to **both weather AND news**
- Regional news prioritization
- Country-specific search terms

**Example:**
```
User: "Morning briefing for Mumbai with tech news"
→ Weather: Mumbai weather data
→ News: India/Mumbai-specific tech news
→ Synthesis: Location-consistent insights
```

---

## Directory Structure

```
multi-agent-orchestrator/
├── daily_briefing_generator/          # Main application directory
│   │
│   ├── orchestrator/                  # Master orchestration
│   │   ├── master_agent.py           # MasterAgent - coordinates all agents
│   │   └── __init__.py
│   │
│   ├── agents/                        # Specialized AI agents
│   │   ├── news_agent.py             # NewsAgent - news curation
│   │   ├── weather_agent.py          # WeatherAgent - weather briefings
│   │   └── __init__.py
│   │
│   ├── tools/                         # External API integrations
│   │   ├── news_tool.py              # Multi-API news aggregator
│   │   ├── weather_tool.py           # OpenWeatherMap integration
│   │   ├── enhanced_news_tool.py     # Advanced multi-source news system
│   │   └── __init__.py
│   │
│   ├── config/                        # Configuration management
│   │   ├── settings.py               # Settings class with validation
│   │   └── __init__.py
│   │
│   ├── web_interface/                 # Web application
│   │   ├── backend/                   # FastAPI server
│   │   │   ├── app.py                # Main FastAPI application
│   │   │   └── routes/
│   │   │       ├── briefing.py       # Briefing API endpoints
│   │   │       └── health.py         # Health check endpoints
│   │   │
│   │   ├── frontend/                  # Static web interface
│   │   │   ├── index.html            # Main UI
│   │   │   ├── config.js             # Environment configuration
│   │   │   └── static/
│   │   │       ├── css/styles.css    # Styling (dark/light mode)
│   │   │       └── js/briefing.js    # Frontend logic
│   │   │
│   │   └── start_web_interface.py    # Server launcher script
│   │
│   └── main.py                        # CLI entry point
│
├── .github/workflows/                 # CI/CD
│   └── deploy.yml                    # GitHub Pages deployment
│
├── requirements.txt                   # Python dependencies
├── .env.template                     # Environment variable template
├── .env                              # Local environment variables (git-ignored)
├── README.md                         # Main documentation
├── CLAUDE.md                         # This file - AI assistant context
├── GITHUB_PAGES_DEPLOYMENT.md        # Deployment guide
├── MULTI_API_SETUP_GUIDE.md          # Multi-API news system setup
└── index.html                        # Root redirect page
```

### Entry Points

1. **CLI**: `daily_briefing_generator/main.py`
   - Single briefing: `python main.py`
   - Interactive mode: `python main.py --interactive`
   - Custom query: `python main.py "your query here"`

2. **Web Server**: `daily_briefing_generator/web_interface/backend/app.py`
   - Start server: `python web_interface/start_web_interface.py`
   - Or: `cd web_interface/backend && python app.py`

3. **Agent Testing**: Direct agent execution
   - `python agents/news_agent.py`
   - `python agents/weather_agent.py`
   - `python orchestrator/master_agent.py`

---

## Code Patterns & Conventions

### Naming Conventions

**Python Code:**
- **Functions/Methods**: `snake_case` (e.g., `get_weather_data`, `process_request`)
- **Classes**: `PascalCase` (e.g., `MasterAgent`, `NewsAgent`, `WeatherAgent`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `API_CONFIG`)
- **Private Methods**: Leading underscore (e.g., `_extract_value`, `_is_valid_article`)

**JavaScript Code:**
- **Variables/Functions**: `camelCase` (e.g., `briefingConfig`, `generateBriefing`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`, `MAX_HISTORY_ITEMS`)
- **Classes**: `PascalCase` (rarely used in this project)

### Async Patterns

**ALWAYS use async/await for I/O operations:**

```python
# ✅ CORRECT - Async I/O with timeout
async def get_news_briefing(self, user_request: str) -> str:
    try:
        response = await asyncio.wait_for(
            self.news_agent.get_news_briefing(news_request),
            timeout=15
        )
        return response
    except asyncio.TimeoutError:
        return fallback_response
```

```python
# ❌ WRONG - Synchronous I/O
def get_news_briefing(self, user_request: str) -> str:
    response = requests.get(url)  # Blocking!
    return response.json()
```

**Concurrent API Calls:**

```python
# ✅ CORRECT - Parallel execution
weather_task = asyncio.create_task(weather_agent.get_weather_briefing(request))
news_task = asyncio.create_task(news_agent.get_news_briefing(request))
weather_response, news_response = await asyncio.gather(weather_task, news_task)
```

**Timeout Requirements:**
- Agent-level operations: **15 seconds**
- Master-level operations: **30 seconds**
- Always use `asyncio.wait_for()` for timeout enforcement

### Error Handling Patterns

**Three-Layer Recovery Example:**

```python
# Layer 1: Master-level recovery (master_agent.py:417-445)
async def run_with_recovery(self, user_request: str) -> str:
    for attempt in range(self.max_retries):  # 3 retries
        try:
            response = await asyncio.wait_for(
                self.process_request(user_request),
                timeout=self.timeout_seconds  # 30s
            )
            return response
        except asyncio.TimeoutError:
            if attempt < self.max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
            return self._get_timeout_fallback(user_request)
```

```python
# Layer 2: Agent-level recovery (master_agent.py:484-501)
if needs_weather:
    try:
        weather_response = await asyncio.wait_for(
            self.weather_agent.get_weather_briefing(weather_request),
            timeout=15
        )
        responses.append(f"🌤️ **Weather Update:**\n{weather_response}")
    except Exception as e:
        logger.error(f"Weather agent failed: {str(e)}")
        failed_services.append("weather")
        responses.append(f"🌤️ **Weather Update:**\n⚠️ {self.fallback_responses['weather']}")
```

```python
# Layer 3: Tool-level fallback (news_tool.py:74-114)
# Strategy 1: Try enhanced NewsAPI search
result = await _fetch_with_enhanced_newsapi(query, country, category, max_articles)
if result.get("status") == "success" and result.get("articles"):
    return result

# Strategy 2: Try broader search terms
result = await _fetch_with_broader_search(query, country, category, max_articles)
if result.get("status") == "success" and result.get("articles"):
    return result

# Strategy 3: Try fallback countries
for fallback_country in fallback_countries:
    result = await _fetch_with_enhanced_newsapi(query, fallback_country, category, max_articles)
    if result.get("status") == "success" and result.get("articles"):
        return result
```

### Code Organization Principles

1. **One agent per file**: Each agent lives in its own module
2. **Separate tools from agents**: Tools handle external APIs, agents handle intelligence
3. **Config isolation**: Configuration in dedicated `config/` directory
4. **Route organization**: API routes grouped by functionality (briefing, health)
5. **No circular imports**: Clear dependency hierarchy (master → agents → tools)

### Import Patterns

```python
# Standard library imports first
import asyncio
import os
import sys
from typing import Dict, List, Any

# Third-party imports second
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, HTTPException

# Local imports last
from agents.weather_agent import WeatherAgent
from agents.news_agent import NewsAgent
from tools.news_tool import get_news_data
```

---

## Key Components Reference

### MasterAgent (orchestrator/master_agent.py)

**Purpose:** Elite orchestration agent that coordinates all sub-agents and synthesizes final briefings.

**Key Methods:**

```python
async def process_request(user_request: str) -> str
    """
    Main orchestration method.
    - Analyzes user request using Gemini AI
    - Extracts location and categories
    - Delegates to specialized agents
    - Synthesizes final three-section briefing

    Returns: Formatted briefing with exactly 3 sections
    """

async def run_with_recovery(user_request: str) -> str
    """
    Execute request with error recovery.
    - 3 retry attempts
    - Exponential backoff (2^attempt seconds)
    - Timeout: 30 seconds per attempt
    - Returns fallback response on total failure

    Returns: Briefing or fallback message
    """

async def process_request_with_agent_recovery(user_request: str) -> str
    """
    Execute with individual agent error handling.
    - Weather agent: 15s timeout with fallback
    - News agent: 15s timeout with fallback
    - Returns partial briefings if one agent fails

    Returns: Briefing with available data
    """

def _extract_value(text: str, key: str) -> str
    """Parse AI analysis responses (e.g., 'NEEDS_WEATHER: yes')"""
```

**Configuration:**
- **Model**: `gemini-flash-lite-latest`
- **Max Retries**: 3
- **Master Timeout**: 30 seconds
- **Agent Timeout**: 15 seconds

**System Instructions:**
- Located in `__init__()` method (lines 34-117)
- Defines delegation strategy
- Enforces three-section format
- Provides error recovery patterns

### NewsAgent (agents/news_agent.py)

**Purpose:** Specialized agent for curating and presenting news briefings.

**Key Methods:**

```python
async def get_news_briefing(user_request: str) -> str
    """
    Curate news based on user request.
    - Analyzes request for category, country, keywords
    - Fetches news data via multi-API tool
    - Generates professional news briefing
    - Falls back gracefully on API failures

    Returns: Curated news briefing
    """

async def _generate_fallback_response(user_request: str, category: str, country: str) -> str
    """Generate meaningful response when no articles available"""

def _format_articles_for_ai(articles: List[Dict]) -> str
    """Format articles for AI processing with content filtering"""
```

**Features:**
- **Category Detection**: technology, business, health, sports, entertainment, general
- **Country Preference**: Defaults to 'us', supports all NewsAPI countries
- **Content Filtering**: Removes invalid/removed articles
- **AI-Powered Synthesis**: Uses Gemini to create professional briefings

### WeatherAgent (agents/weather_agent.py)

**Purpose:** Specialized agent for weather briefings with contextual advice.

**Key Methods:**

```python
async def get_weather_briefing(user_request: str) -> str
    """
    Generate weather briefing from user request.
    - Extracts city and country from natural language
    - Fetches real-time weather data
    - Creates conversational briefing with advice

    Returns: Natural language weather briefing
    """
```

**Features:**
- **Location Extraction**: AI-powered city/country parsing
- **Contextual Advice**: Business and travel implications
- **Natural Language**: Conversational tone, not raw data

### NewsT tool (tools/news_tool.py)

**Purpose:** Multi-API news aggregation with robust fallback strategies.

**Key Functions:**

```python
async def get_news_data(
    query: str = "technology",
    country: str = "us",
    category: str = "general",
    max_articles: int = 5
) -> Dict[str, Any]
    """
    Fetch news from multiple sources.
    - Tries enhanced multi-API system first
    - Falls back to NewsAPI with multiple strategies
    - Filters invalid articles
    - Returns normalized article format
    """
```

**Multi-API Support:**
1. NewsAPI.org (primary)
2. GNews API (most reliable)
3. NewsData.io
4. MediaStack
5. Currents API
6. WorldNews API
7. NewsCatcher API
8. RSS feeds (fallback)

**Fallback Strategies:**
1. Enhanced NewsAPI search
2. Broader search terms
3. Fallback countries (us, in, gb, au, ca)
4. General category fallback

### API Routes (web_interface/backend/routes/)

**Briefing Routes (briefing.py):**

```python
POST /api/v1/briefing
    """
    Request body:
    {
        "query": "Morning briefing for Mumbai with tech news",
        "location": "Mumbai",  # Optional
        "categories": ["technology"],  # Optional
        "use_recovery": true  # Optional, default false
    }

    Response: Full briefing with 3 sections
    """

GET /api/v1/briefing/quick/{briefing_type}?location=London
    """
    Types: weather, news, business, technology, complete
    Quick briefings without custom queries
    """

GET /api/v1/briefing/templates
    """
    Returns available briefing templates and examples
    """
```

**Health Routes (health.py):**

```python
GET /api/v1/health
    """Returns API health status"""
```

---

## Configuration & Environment

### Required Environment Variables

```bash
# Required - Core functionality
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here
NEWS_API_KEY=your_newsapi_org_key_here

# Optional - Enhanced news coverage
GNEWS_API_KEY=your_gnews_api_key
NEWSDATA_API_KEY=your_newsdata_api_key
MEDIASTACK_API_KEY=your_mediastack_api_key
CURRENTS_API_KEY=your_currents_api_key
WORLDNEWS_API_KEY=your_worldnews_api_key
NEWSCATCHER_API_KEY=your_newscatcher_api_key

# Optional - Defaults
DEFAULT_LOCATION=New York, NY
DEFAULT_NEWS_TOPICS=technology,business
NEWS_COUNTRY=us
NEWS_LANGUAGE=en
MAX_NEWS_ARTICLES=5
```

### Settings Class (config/settings.py)

**Features:**
- Environment variable loading via python-dotenv
- Default values with fallbacks
- Validation methods
- Dynamic settings updates

**Usage Example:**

```python
from config.settings import Settings

settings = Settings()
print(settings.get_all_settings())

issues = settings.validate_settings()
if issues:
    print(f"Configuration issues: {issues}")
```

### API Key Setup

**Get API Keys:**
1. **Google AI**: https://makersuite.google.com/app/apikey
2. **OpenWeatherMap**: https://openweathermap.org/api
3. **NewsAPI**: https://newsapi.org/register
4. **Additional News APIs**: See `MULTI_API_SETUP_GUIDE.md`

**Configure Locally:**
```bash
cp .env.template .env
# Edit .env with your API keys
```

---

## Development Workflows

### Workflow 1: Adding a New Agent

**Step-by-Step Process:**

1. **Create new agent file** in `daily_briefing_generator/agents/`

```python
# agents/stock_agent.py
import asyncio
import os
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class StockAgent:
    def __init__(self):
        api_key = os.getenv("GOOGLE_AI_API_KEY")
        if not api_key:
            raise ValueError("Google AI API key not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-lite-latest')

    async def get_stock_briefing(self, user_request: str) -> str:
        """Generate stock market briefing"""
        # 1. Analyze request
        # 2. Fetch stock data (create tool if needed)
        # 3. Generate AI briefing
        return "Stock briefing here"
```

2. **Import in MasterAgent** (`orchestrator/master_agent.py`)

```python
from agents.stock_agent import StockAgent

class MasterAgent:
    def __init__(self):
        # ... existing code ...
        self.stock_agent = StockAgent()  # Add new agent
```

3. **Update system instructions** to mention new agent

4. **Add delegation logic** in `process_request()`:

```python
# Parse analysis for stock needs
needs_stocks = self._extract_value(analysis, "NEEDS_STOCKS:").lower() == "yes"

if needs_stocks:
    stock_response = await self.stock_agent.get_stock_briefing(user_request)
    responses.append(f"📈 **Stock Update:**\n{stock_response}")
```

5. **Add agent-specific error handling**:

```python
# In process_request_with_agent_recovery()
if needs_stocks:
    try:
        stock_response = await asyncio.wait_for(
            self.stock_agent.get_stock_briefing(stock_request),
            timeout=15
        )
        responses.append(f"📈 **Stock Update:**\n{stock_response}")
    except Exception as e:
        logger.error(f"Stock agent failed: {str(e)}")
        responses.append(f"📈 **Stock Update:**\n⚠️ Stock data temporarily unavailable")
```

6. **Test independently** before integration:

```bash
python agents/stock_agent.py
```

7. **Update this CLAUDE.md** with agent details

### Workflow 2: Adding a New API

**Step-by-Step Process:**

1. **Add API key** to `.env.template` and `.env`:

```bash
# .env.template
NEW_API_KEY=your_api_key_here
```

2. **Create or update tool** in `tools/` directory:

```python
# tools/new_api_tool.py
import asyncio
import aiohttp
import os
from typing import Dict, Any

async def fetch_from_new_api(
    param1: str,
    param2: str,
    timeout: int = 15
) -> Dict[str, Any]:
    """
    Fetch data from new API.

    Args:
        param1: Description
        param2: Description
        timeout: Request timeout in seconds

    Returns:
        Dict with data or error
    """
    api_key = os.getenv("NEW_API_KEY")
    if not api_key:
        return {"status": "error", "error": "API key not found"}

    url = "https://api.example.com/endpoint"
    params = {"key": api_key, "param1": param1, "param2": param2}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"status": "success", "data": data}
                elif response.status == 429:
                    return {"status": "error", "error": "Rate limit exceeded"}
                else:
                    return {"status": "error", "error": f"API returned {response.status}"}
    except asyncio.TimeoutError:
        return {"status": "error", "error": "Request timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
```

3. **Add rate limit handling**: Track requests, implement backoff

4. **Add to multi-API fallback chain** (if applicable):

```python
# In tools/news_tool.py or similar
result = await fetch_from_primary_api()
if result.get("status") == "error":
    result = await fetch_from_new_api()  # Fallback
```

5. **Test with rate limits and failures**:

```bash
python tools/new_api_tool.py
```

6. **Document in this file** and `MULTI_API_SETUP_GUIDE.md`

### Workflow 3: Debugging Strategies

**Agent-Level Debugging:**

```bash
# Test agents individually
python daily_briefing_generator/agents/news_agent.py
python daily_briefing_generator/agents/weather_agent.py
python daily_briefing_generator/orchestrator/master_agent.py
```

**Tool-Level Debugging:**

```bash
# Test tools individually
python daily_briefing_generator/tools/news_tool.py
python daily_briefing_generator/tools/weather_tool.py
```

**Common Issues Checklist:**

1. **Environment Variables**:
```bash
# Verify .env is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GOOGLE_AI_API_KEY')[:10] if os.getenv('GOOGLE_AI_API_KEY') else 'NOT FOUND')"
```

2. **API Rate Limits**:
   - Check console logs for 426/429 status codes
   - Use multi-API fallback system
   - Enable `use_recovery=true` parameter

3. **Timeouts**:
   - Check logs for timeout errors
   - Adjust timeouts in `master_agent.py` (lines 127, 426, 492, 511)
   - Consider network latency

4. **Location Extraction**:
   - Verify logs show extracted location
   - Check `_extract_value()` parsing
   - Test with explicit city names

5. **News Quality**:
   - Check article filtering in `news_tool.py:255-278`
   - Update `_is_valid_article()` logic
   - Adjust `invalid_indicators` list

**Enable Debug Logging:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Use Recovery Mode:**

```python
# In API requests
POST /api/v1/briefing
{
    "query": "your query",
    "use_recovery": true  # Enable all recovery mechanisms
}
```

### Workflow 4: Frontend Changes

**File Locations:**
- HTML: `daily_briefing_generator/web_interface/frontend/index.html`
- CSS: `daily_briefing_generator/web_interface/frontend/static/css/styles.css`
- JavaScript: `daily_briefing_generator/web_interface/frontend/static/js/briefing.js`
- Config: `daily_briefing_generator/web_interface/frontend/config.js`

**Making Changes:**

1. **Edit HTML/CSS/JS directly** (no build step required)

2. **Update cache-bust version** in `config.js`:

```javascript
// config.js
window.BRIEFING_CONFIG = {
    API_BASE_URL: 'https://multi-agent-orchestrator.onrender.com',
    VERSION: '3',  // Increment this to bust cache
    // ... other config
};
```

3. **Test dark/light mode toggle**:
   - Check localStorage persistence
   - Verify CSS variables update
   - Test on page reload

4. **Verify responsive design**:
   - Mobile (< 768px)
   - Tablet (768px - 1024px)
   - Desktop (> 1024px)

5. **Test history persistence**:
   - Generate briefing
   - Reload page
   - Verify history loads from localStorage

6. **No build step needed** - pure static files

**Dark/Light Mode Implementation:**

```css
/* styles.css - CSS variables pattern */
:root {
    --bg-primary: #ffffff;
    --text-primary: #000000;
    /* ... */
}

[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --text-primary: #ffffff;
    /* ... */
}
```

```javascript
// briefing.js - Toggle implementation
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}
```

---

## Testing Guidance

### Unit Testing

**Test agents individually:**

```bash
# News Agent
cd daily_briefing_generator
python agents/news_agent.py
# Expected: Fetches and displays news briefings

# Weather Agent
python agents/weather_agent.py
# Expected: Fetches and displays weather briefings

# Master Agent
python orchestrator/master_agent.py
# Expected: Runs comprehensive test suite
```

### Integration Testing

**Test via API:**

```bash
# Start server
python web_interface/start_web_interface.py

# Test in another terminal
curl -X POST "http://localhost:8000/api/v1/briefing" \
  -H "Content-Type: application/json" \
  -d '{"query": "Morning briefing for Mumbai with tech news"}'
```

**Test cases to verify:**

1. **Weather-only request**:
```json
{"query": "What's the weather in London?"}
```

2. **News-only request**:
```json
{"query": "Give me technology news"}
```

3. **Complete briefing**:
```json
{"query": "Complete morning briefing for New York with business news"}
```

4. **Location-specific**:
```json
{"query": "Delhi briefing with sports news"}
```

### Error Testing

**Test with invalid API keys:**

1. Temporarily set invalid key in `.env`
2. Run test
3. Verify fallback responses work
4. Check error messages are user-friendly

**Test network failures:**

```python
# Simulate timeout
import asyncio

async def test_timeout():
    try:
        await asyncio.wait_for(
            master_agent.process_request("test"),
            timeout=0.001  # Very short timeout
        )
    except asyncio.TimeoutError:
        print("Timeout handled correctly")
```

### Recovery Testing

**Test recovery system:**

```bash
# Use recovery parameter
curl -X POST "http://localhost:8000/api/v1/briefing" \
  -H "Content-Type: application/json" \
  -d '{"query": "Morning briefing", "use_recovery": true}'
```

**Verify:**
- Retries happen on failure
- Exponential backoff works
- Partial briefings returned when one agent fails
- Fallback messages are professional

### Frontend Testing

**Test in multiple browsers:**
- Chrome/Edge (Chromium)
- Firefox
- Safari (if on macOS)

**Test features:**
1. Generate briefing
2. Toggle dark/light mode
3. Check history loads
4. Clear history
5. Responsive design (resize window)
6. Copy briefing to clipboard

---

## Common Issues & Solutions

### Issue 1: API Rate Limits

**Symptoms:**
- HTTP 426 or 429 errors
- "Rate limit exceeded" messages
- Empty news results

**Solutions:**
1. Use multi-API fallback system (configure additional API keys)
2. Reduce `max_articles` parameter
3. Implement caching (not yet implemented)
4. Wait and retry (recovery system handles this)

**Prevention:**
```python
# In .env, add multiple API keys
GNEWS_API_KEY=...
NEWSDATA_API_KEY=...
MEDIASTACK_API_KEY=...
```

### Issue 2: Timeout Errors

**Symptoms:**
- `asyncio.TimeoutError` exceptions
- "Request timeout" messages
- Slow responses

**Solutions:**
1. Increase timeouts in `master_agent.py`:
```python
# Line 127: Agent timeout
timeout=20  # Increase from 15

# Line 426: Master timeout
timeout=45  # Increase from 30
```

2. Check network latency
3. Use recovery mode: `use_recovery=true`

### Issue 3: Location Extraction Fails

**Symptoms:**
- Generic news instead of location-specific
- Weather works but news is global
- Logs show "default" location

**Solutions:**
1. Use explicit city names: "Mumbai" not "here"
2. Check `_extract_value()` parsing in `master_agent.py:301-307`
3. Improve location parsing prompt in `master_agent.py:138-164`

**Debug:**
```python
# Add logging to see what's extracted
logger.info(f"Extracted location: {weather_location}, country: {location_country}")
```

### Issue 4: News Quality Issues

**Symptoms:**
- "[Removed]" articles appearing
- Very short/invalid articles
- Duplicate articles

**Solutions:**
1. Update filtering in `news_tool.py:255-278`:
```python
def _is_valid_article(article: Dict) -> bool:
    # Add more invalid indicators
    invalid_indicators = [
        "[Removed]", "removed", "unavailable",
        "access denied", "subscribe to read",
        "paywall", "premium content"  # Add these
    ]
```

2. Increase minimum content length:
```python
if len(title) < 20 or len(description) < 50:  # Stricter
    return False
```

### Issue 5: CORS Errors

**Symptoms:**
- Browser console: "CORS policy" errors
- OPTIONS requests failing with 405

**Solutions:**
1. Check CORS configuration in `app.py:57-63`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

2. Verify endpoint exists for OPTIONS method
3. Check that `allow_credentials=False` when using wildcard origin

### Issue 6: Environment Variables Not Loading

**Symptoms:**
- "API key not found" errors
- `ValueError` on agent initialization

**Solutions:**
1. Verify `.env` file exists in correct location
2. Check `load_dotenv()` is called:
```python
from dotenv import load_dotenv
load_dotenv()  # Call before accessing os.getenv()
```

3. Use absolute path if needed:
```python
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
```

4. Check environment variable names match exactly:
```bash
# Correct
GOOGLE_AI_API_KEY=...

# Wrong
GOOGLE_API_KEY=...  # Different name
```

---

## Design Philosophy

### Core Principles

1. **Executive-Quality Output**
   - Professional briefings, not raw data dumps
   - Executive-level language and insights
   - Business implications over feature lists
   - Actionable recommendations

2. **Reliability Over Perfection**
   - Graceful degradation always
   - Partial briefings better than no briefings
   - Multi-layer error recovery
   - User-friendly error messages

3. **User-Centric Design**
   - Natural language queries, no complex syntax
   - Intuitive web interface
   - No learning curve required
   - Mobile-first responsive design

4. **Minimal UI Philosophy**
   - Content-first, distraction-free
   - No unnecessary animations or decorations
   - Dark mode as default (eye-friendly)
   - Fast load times (< 1s)

5. **Performance First**
   - Async operations throughout
   - Parallel API calls where possible
   - Timeout enforcement
   - No blocking operations

6. **Extensibility**
   - Easy to add new agents
   - Easy to add new APIs
   - Clear separation of concerns
   - Minimal code coupling

### Key Design Decisions

**Why Three Sections?**
- Enforces consistent structure
- Easy to scan quickly
- Combines data + insights
- No fluff or filler content

**Why Multi-API System?**
- No single point of failure
- Better coverage across regions
- Rate limit resilience
- Quality through diversity

**Why No Database?**
- Stateless API is simpler
- No database maintenance
- Scales horizontally
- Frontend history via localStorage

**Why Vanilla JavaScript?**
- No build step complexity
- Faster load times
- Easier for contributors
- No framework lock-in

**Why FastAPI?**
- Modern async support
- Auto-generated docs (/docs)
- Type validation via Pydantic
- Fast and lightweight

---

## What NOT to Do

### ❌ Forbidden Patterns

**1. Synchronous I/O Operations**
```python
# ❌ NEVER DO THIS
import requests
response = requests.get(url)  # Blocking!
```

**2. Skip Error Handling**
```python
# ❌ NEVER DO THIS
async def get_data():
    return await api_call()  # No try/except!
```

**3. Add Heavy JavaScript Frameworks**
```html
<!-- ❌ NEVER DO THIS -->
<script src="react.js"></script>
<script src="vue.js"></script>
```

**4. Hardcode API Keys**
```python
# ❌ NEVER DO THIS
API_KEY = "sk-1234567890abcdef"  # Exposed!
```

**5. Skip Timeouts**
```python
# ❌ NEVER DO THIS
response = await self.model.generate_content_async(prompt)
# No timeout = can hang forever
```

**6. Remove Three-Section Format**
```python
# ❌ NEVER DO THIS
return f"""
{weather}
{news}
## Conclusion
## Outlook
"""  # Too many sections!
```

**7. Add Database Without Discussion**
```python
# ❌ NEVER DO THIS
import sqlite3
conn = sqlite3.connect('briefings.db')
# Stateless API is intentional design
```

**8. Use Mutable Default Arguments**
```python
# ❌ NEVER DO THIS
def get_news(categories=[]):  # Mutable default!
    categories.append("general")
```

**9. Ignore Naming Conventions**
```python
# ❌ NEVER DO THIS
def GetWeatherData():  # Should be snake_case
    pass
```

**10. Make Destructive Changes Without Confirmation**
```python
# ❌ NEVER DO THIS
os.remove(config_file)  # Always confirm first!
```

### ✅ Recommended Patterns

**1. Always Async I/O**
```python
# ✅ DO THIS
async with aiohttp.ClientSession() as session:
    async with session.get(url, timeout=15) as response:
        return await response.json()
```

**2. Comprehensive Error Handling**
```python
# ✅ DO THIS
try:
    result = await asyncio.wait_for(operation(), timeout=15)
    return result
except asyncio.TimeoutError:
    logger.error("Operation timeout")
    return fallback_response
except Exception as e:
    logger.error(f"Operation failed: {e}")
    return error_response
```

**3. Environment-Based Configuration**
```python
# ✅ DO THIS
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API key not found in environment")
```

**4. Clear Logging**
```python
# ✅ DO THIS
logger.info(f"Processing request: {user_request}")
logger.error(f"Weather agent failed: {str(e)}")
```

---

## Quick Reference Commands

### Development

```bash
# Start web server (development)
cd daily_briefing_generator
python web_interface/start_web_interface.py

# Start web server (production)
cd daily_briefing_generator/web_interface/backend
python app.py

# CLI single briefing
python main.py

# CLI interactive mode
python main.py --interactive

# CLI with custom query
python main.py "Morning briefing for Mumbai with tech news"
```

### Testing

```bash
# Test individual agents
python daily_briefing_generator/agents/news_agent.py
python daily_briefing_generator/agents/weather_agent.py
python daily_briefing_generator/orchestrator/master_agent.py

# Test API tools
python daily_briefing_generator/tools/news_tool.py
python daily_briefing_generator/tools/weather_tool.py

# Test web interface (manual)
curl -X POST "http://localhost:8000/api/v1/briefing" \
  -H "Content-Type: application/json" \
  -d '{"query": "test briefing"}'

# Health check
curl http://localhost:8000/api/v1/health
```

### API Endpoints

```bash
# Main briefing endpoint
POST http://localhost:8000/api/v1/briefing
Body: {"query": "your query", "use_recovery": true}

# Quick briefings
GET http://localhost:8000/api/v1/briefing/quick/weather?location=London
GET http://localhost:8000/api/v1/briefing/quick/technology

# Templates
GET http://localhost:8000/api/v1/briefing/templates

# Health check
GET http://localhost:8000/api/v1/health
```

### Git/Deployment

```bash
# Check status
git status

# Commit changes
git add .
git commit -m "description"

# Push to trigger deployment
git push origin master

# View deployment logs
# GitHub Pages: Check Actions tab on GitHub
# Render: Check Render dashboard
```

### Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.template .env
# Edit .env with your API keys

# Verify setup
python -c "from config.settings import Settings; s=Settings(); print(s.validate_settings())"
```

---

## Maintenance & Updates

### When to Update This File

- ✅ Adding new agents or tools
- ✅ Changing architecture patterns
- ✅ Adding new workflows or conventions
- ✅ Discovering common issues
- ✅ Updating API integrations
- ✅ Modifying configuration options
- ✅ Changing deployment procedures

### File Size Guideline

- **Target**: 600-800 lines (comprehensive but scannable)
- **Maximum**: 1000 lines
- **Review**: Quarterly for accuracy

### Version History

- **v1.0.0** (2026-03-24): Initial comprehensive context file

---

## Additional Resources

### Documentation Files

- `README.md` - Main project documentation
- `GITHUB_PAGES_DEPLOYMENT.md` - Frontend deployment guide
- `MULTI_API_SETUP_GUIDE.md` - Multi-API news system setup
- `.env.template` - Environment variable template

### External Links

- **Live Demo**: https://AniruddhAgrahari.github.io/multi-agent-orchestrator/
- **Backend API**: https://multi-agent-orchestrator.onrender.com
- **API Documentation**: https://multi-agent-orchestrator.onrender.com/docs

### Getting Help

If you encounter issues not covered in this guide:

1. Check the relevant section in this file
2. Review error logs for specific error messages
3. Test components individually (agents → tools)
4. Check API service status (Google AI, OpenWeatherMap, NewsAPI)
5. Verify environment variables are set correctly

---

**End of CLAUDE.md** - This file provides comprehensive context for AI assistants working on the multi-agent orchestrator project. Keep it updated as the project evolves!
