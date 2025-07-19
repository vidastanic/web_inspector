# Development Guide

This document provides detailed information for developers working on the WebChecker project.

## Project Structure

```
email_scraper/
├── pyproject.toml          # Poetry configuration and dependencies
├── README.md              # Main project documentation
├── DEVELOPMENT.md         # This development guide
├── pytest.ini            # Pytest configuration
├── test_installation.py  # Installation verification script
├── webchecker/           # Main package
│   ├── __init__.py       # Package initialization
│   ├── main.py          # Command line interface
│   ├── scraper.py       # Web scraping logic
│   ├── patterns.py      # Pattern matching
│   └── utils.py         # Utility functions
├── examples/             # Example scripts
│   ├── find_trademarks.py
│   └── custom_patterns.py
└── tests/               # Test suite
    ├── __init__.py
    ├── test_patterns.py
    └── test_utils.py
```

## Core Components

### 1. WebScraper (`webchecker/scraper.py`)
The main scraping engine that:
- Crawls websites following links within the same domain
- Discovers and follows sitemap.xml files
- Implements respectful crawling with configurable delays
- Handles session management and error recovery

**Key Features:**
- Breadth-first crawling with depth limits
- Sitemap discovery and parsing
- Robots.txt compliance (basic)
- Configurable rate limiting
- Session persistence for efficiency

### 2. PatternMatcher (`webchecker/patterns.py`)
Handles pattern matching and text extraction:
- Unicode character matching (™, ®, ©, etc.)
- Custom regex pattern support
- Context extraction (text before patterns)
- Specialized trademark pattern detection

**Key Features:**
- Flexible pattern matching with regex
- Context-aware extraction
- Built-in common symbol patterns
- Case-insensitive matching support

### 3. Command Line Interface (`webchecker/main.py`)
Provides a comprehensive CLI with:
- Argument parsing with argparse
- Multiple output formats
- Verbose logging options
- Configuration flexibility

### 4. Utilities (`webchecker/utils.py`)
Helper functions for:
- URL validation and parsing
- Text cleaning and normalization
- Logging setup
- File operations

## Development Workflow

### 1. Setup Development Environment

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Clone and setup the project
git clone <repository-url>
cd email_scraper

# Install dependencies
poetry install

# Install development dependencies
poetry install --with test

# Activate virtual environment
poetry shell
```

### 2. Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=webchecker

# Run specific test file
poetry run pytest tests/test_patterns.py

# Run with verbose output
poetry run pytest -v
```

### 3. Code Quality

```bash
# Install additional development tools
poetry add --group dev flake8 mypy black isort

# Run linting
poetry run flake8 webchecker/

# Run type checking
poetry run mypy webchecker/

# Format code
poetry run black webchecker/
poetry run isort webchecker/
```

### 4. Testing Installation

```bash
# Run the installation test
python test_installation.py
```

## Architecture Decisions

### 1. Modular Design
The project is designed with clear separation of concerns:
- **Scraper**: Handles web crawling and content extraction
- **Patterns**: Manages pattern matching logic
- **Utils**: Provides common utility functions
- **Main**: Orchestrates the application flow

### 2. Session Management
Uses `requests.Session()` for:
- Connection pooling
- Cookie persistence
- Header management
- Efficient resource usage

### 3. Respectful Crawling
Implements several best practices:
- Configurable delays between requests
- User agent identification
- Domain restriction (same-domain crawling)
- Error handling and recovery

### 4. Extensible Pattern Matching
Supports both simple character matching and complex regex patterns:
- Unicode character support
- Custom regex patterns
- Context extraction
- Built-in common patterns

## Next Steps for Development

### Phase 1: Core Improvements (High Priority)

#### 1. Enhanced Error Handling
```python
# Add retry logic with exponential backoff
class RetryHandler:
    def __init__(self, max_retries=3, backoff_factor=2):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def execute_with_retry(self, func, *args, **kwargs):
        # Implementation with exponential backoff
        pass
```

#### 2. Content Filtering
```python
# Add content filtering to ignore navigation/footers
class ContentFilter:
    def __init__(self):
        self.ignore_selectors = [
            'nav', 'footer', '.navigation', '.sidebar',
            '.advertisement', '.banner'
        ]
    
    def filter_content(self, soup):
        # Remove unwanted elements
        pass
```

#### 3. Export Formats
```python
# Add multiple export formats
class ResultExporter:
    def export_json(self, results, filename):
        # Export as JSON
        pass
    
    def export_csv(self, results, filename):
        # Export as CSV
        pass
    
    def export_xml(self, results, filename):
        # Export as XML
        pass
```

### Phase 2: Performance Enhancements (Medium Priority)

#### 1. Async Support
```python
import asyncio
import aiohttp

class AsyncWebScraper:
    async def scrape_site_async(self, start_url, pattern_matcher):
        # Async implementation for better performance
        pass
```

#### 2. Caching
```python
import pickle
import hashlib

class CacheManager:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = cache_dir
    
    def get_cache_key(self, url):
        return hashlib.md5(url.encode()).hexdigest()
    
    def get_cached_content(self, url):
        # Retrieve cached content
        pass
    
    def cache_content(self, url, content):
        # Cache content
        pass
```

#### 3. Rate Limiting
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_second=1):
        self.requests_per_second = requests_per_second
        self.last_request = defaultdict(float)
    
    def wait_if_needed(self, domain):
        # Implement rate limiting per domain
        pass
```

### Phase 3: Advanced Features (Low Priority)

#### 1. JavaScript Rendering
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class JavaScriptRenderer:
    def __init__(self):
        self.driver = None
    
    def setup_driver(self):
        # Setup headless Chrome
        pass
    
    def render_page(self, url):
        # Render JavaScript-heavy pages
        pass
```

#### 2. Database Integration
```python
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="results.db"):
        self.db_path = db_path
    
    def create_tables(self):
        # Create necessary tables
        pass
    
    def store_results(self, url, pattern, matches):
        # Store results in database
        pass
    
    def query_results(self, filters=None):
        # Query stored results
        pass
```

#### 3. Configuration Management
```python
import yaml
from dataclasses import dataclass

@dataclass
class ScraperConfig:
    max_pages: int = 50
    max_depth: int = 3
    timeout: int = 10
    delay: float = 1.0
    user_agent: str = "WebChecker/0.1.0"

class ConfigManager:
    def load_config(self, config_path):
        # Load configuration from YAML file
        pass
    
    def save_config(self, config, config_path):
        # Save configuration to YAML file
        pass
```

## Testing Strategy

### 1. Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Test edge cases and error conditions

### 2. Integration Tests
- Test component interactions
- Use mock HTTP servers for web scraping tests
- Test end-to-end workflows

### 3. Performance Tests
- Benchmark scraping speed
- Test memory usage
- Measure resource consumption

### 4. Example Test Structure
```python
import pytest
from unittest.mock import Mock, patch
from webchecker.scraper import WebScraper

class TestWebScraper:
    @pytest.fixture
    def mock_response(self):
        response = Mock()
        response.content = "<html><body>Test content™</body></html>"
        response.raise_for_status.return_value = None
        return response
    
    @patch('requests.Session.get')
    def test_scrape_page(self, mock_get, mock_response):
        mock_get.return_value = mock_response
        # Test implementation
        pass
```

## Contributing Guidelines

### 1. Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Keep functions small and focused

### 2. Testing Requirements
- Write tests for all new functionality
- Maintain test coverage above 80%
- Include both positive and negative test cases

### 3. Documentation
- Update README.md for user-facing changes
- Update this guide for architectural changes
- Include examples for new features

### 4. Pull Request Process
1. Create a feature branch
2. Implement changes with tests
3. Run the full test suite
4. Update documentation
5. Submit pull request with description

## Performance Considerations

### 1. Memory Usage
- Use generators for large result sets
- Implement pagination for database queries
- Clean up resources properly

### 2. Network Efficiency
- Implement connection pooling
- Use appropriate timeouts
- Handle rate limiting gracefully

### 3. Scalability
- Design for horizontal scaling
- Use async/await for I/O operations
- Implement caching strategies

## Security Considerations

### 1. Input Validation
- Validate all URLs before processing
- Sanitize user-provided patterns
- Handle malicious content safely

### 2. Rate Limiting
- Respect robots.txt files
- Implement configurable delays
- Monitor request frequency

### 3. Error Handling
- Don't expose sensitive information in errors
- Log security-relevant events
- Handle exceptions gracefully

## Monitoring and Logging

### 1. Logging Strategy
```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def log_scrape_event(self, url, status, duration, matches_count):
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'url': url,
            'status': status,
            'duration': duration,
            'matches_count': matches_count
        }
        self.logger.info(json.dumps(event))
```

### 2. Metrics Collection
- Track scraping success rates
- Monitor performance metrics
- Collect usage statistics

This development guide provides a comprehensive overview of the project structure, development workflow, and future enhancement plans. Use it as a reference for contributing to the project and understanding the codebase architecture. 