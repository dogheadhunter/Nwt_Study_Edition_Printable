# GitHub Copilot Instructions for NWT Study Edition Printable

## Project Overview

This is a Python web scraping project designed to extract content from the JW.org Study Bible (New World Translation Study Edition). The project focuses on:

- Scraping Bible text, verses, and chapter content
- Extracting study notes, footnotes, and cross-references
- Parsing HTML content using BeautifulSoup4
- Storing structured data in JSON and CSV formats
- Providing a beginner-friendly codebase with comprehensive documentation

## Tech Stack

- **Python**: 3.8+ (primary language)
- **Web Scraping**: 
  - Playwright (via MCP tools) - **Recommended approach**
  - Selenium - Legacy fallback (being phased out)
- **HTML Parsing**: BeautifulSoup4, lxml, html5lib
- **HTTP Clients**: requests, aiohttp
- **Data Handling**: pandas
- **Testing**: pytest, pytest-asyncio
- **Environment**: python-dotenv

## Project Structure

```
Nwt_Study_Edition_Printable/
├── .github/                        # GitHub configuration
│   ├── copilot-instructions.md     # This file
│   └── agents/                     # Custom agent profiles
├── .vscode/                        # VS Code settings
│   ├── settings.json               # Editor and Copilot config
│   └── mcp.json                    # MCP server configuration
├── docs/                           # Documentation
│   ├── PLAYWRIGHT_USAGE.md         # Playwright MCP guide
│   ├── API_DOCUMENTATION.md        # Data models and patterns
│   ├── WEBPAGE_STRUCTURE.md        # HTML structure analysis
│   ├── GETTING_STARTED.md          # Setup guide
│   └── COPILOT_SETUP.md            # Copilot setup instructions
├── src/                            # Source code
│   ├── scrapers/                   # Web scraping modules
│   │   ├── playwright_scraper.py   # Playwright-based scraper
│   │   └── bible_scraper.py        # Selenium scraper (legacy)
│   ├── parsers/                    # HTML parsing
│   │   └── html_parser.py          # BeautifulSoup parser
│   ├── utils/                      # Utilities
│   │   └── storage.py              # Data storage helpers
│   └── config.py                   # Configuration and selectors
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   └── test_*.py                   # Test files
├── examples/                       # Example scripts
├── pytest.ini                      # Pytest configuration
└── requirements.txt                # Python dependencies
```

## Coding Standards

### Python Style
- **Follow PEP 8** for all Python code
- Use **4 spaces** for indentation (not tabs)
- Maximum line length: **88 characters** (Black formatter default)
- Use **Google-style docstrings** for all functions and classes
- Include **type hints** for function parameters and return values

### Docstring Format
```python
def scrape_chapter(book: str, chapter: int) -> Dict[str, Any]:
    """
    Scrape a Bible chapter from JW.org.
    
    Args:
        book: The book name (e.g., "Genesis")
        chapter: The chapter number (1-based)
        
    Returns:
        Dictionary containing verses, study notes, and metadata
        
    Raises:
        ValueError: If book or chapter is invalid
        HTTPError: If the webpage cannot be accessed
        
    Example:
        >>> data = scrape_chapter("Genesis", 1)
        >>> print(data['verses'][0]['text'])
    """
```

### Import Organization
```python
# Standard library imports
import json
import logging
from typing import Dict, List, Optional

# Third-party imports
import requests
from bs4 import BeautifulSoup

# Local imports
from src.config import SELECTORS, SCRAPING_CONFIG
from src.utils.storage import DataStorage
```

## Error Handling Patterns

### Always Use Try-Except Blocks
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    logger.error(f"Failed to fetch {url}: {e}")
    raise
```

### Validate Input Parameters
```python
def get_chapter(book: str, chapter: int) -> Dict:
    """Get chapter data with validation."""
    if not book or not isinstance(book, str):
        raise ValueError(f"Invalid book name: {book}")
    if not 1 <= chapter <= 150:  # Max chapters in Psalms
        raise ValueError(f"Invalid chapter number: {chapter}")
```

### Log Errors with Context
```python
logger = logging.getLogger(__name__)

try:
    data = parse_html(content)
except Exception as e:
    logger.error(f"Failed to parse HTML for {book} {chapter}: {e}")
    raise
```

## Web Scraping Best Practices

### Rate Limiting (CRITICAL)
```python
import time

# Always add delays between requests
time.sleep(SCRAPING_CONFIG['request_delay'])  # Default: 3 seconds

# Use longer delays for bulk operations
time.sleep(SCRAPING_CONFIG['chapter_delay'])  # 5 seconds between chapters
```

### Explicit Waits (Never use time.sleep in browser automation)
```python
# For Playwright MCP
playwright-browser_wait_for(text="Study Bible")

# For Selenium (legacy)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".verse")))
```

### Data Validation
```python
def validate_verse(verse_data: Dict) -> bool:
    """Validate that verse data is complete."""
    required_fields = ['number', 'text']
    return all(field in verse_data and verse_data[field] for field in required_fields)
```

## Playwright MCP Usage

### Navigation Pattern
```python
# 1. Navigate to page
playwright-browser_navigate(url="https://www.jw.org/en/library/bible/study-bible/books/")

# 2. Wait for content
playwright-browser_wait_for(text="Genesis")

# 3. Take snapshot to inspect
snapshot = playwright-browser_snapshot()

# 4. Click element (use ref from snapshot)
playwright-browser_click(element="Genesis link", ref="<ref>")
```

### Content Extraction Pattern
```python
# 1. Navigate to chapter
playwright-browser_navigate(url=chapter_url)

# 2. Wait for verses to load
playwright-browser_wait_for(text="verse 1")

# 3. Get page HTML (via snapshot or evaluate)
html = playwright-browser_evaluate(function="() => document.body.innerHTML")

# 4. Parse with BeautifulSoup
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
verses = soup.find_all('p', class_='verse')
```

## BeautifulSoup Parsing Patterns

### Extract Verses
```python
from src.config import SELECTORS

verses = []
verse_elements = soup.find_all('p', class_=SELECTORS['verse'])

for verse_elem in verse_elements:
    number_elem = verse_elem.find('span', class_=SELECTORS['verse_number'])
    verse_number = number_elem.text.strip() if number_elem else None
    
    # Get text without verse number
    text = verse_elem.get_text(strip=True)
    if verse_number:
        text = text.replace(verse_number, '', 1).strip()
    
    verses.append({
        'number': verse_number,
        'text': text
    })
```

### Extract Study Notes
```python
study_notes = []
note_elements = soup.find_all('div', class_=SELECTORS['study_note'])

for note_elem in note_elements:
    reference_elem = note_elem.find(class_=SELECTORS['study_note_reference'])
    content_elem = note_elem.find(class_=SELECTORS['study_note_content'])
    
    study_notes.append({
        'reference': reference_elem.text.strip() if reference_elem else None,
        'content': content_elem.text.strip() if content_elem else None
    })
```

## Data Storage Patterns

### Save as JSON
```python
from src.utils.storage import DataStorage
import json

storage = DataStorage()

# Save chapter data
data = {
    'book': 'Genesis',
    'chapter': 1,
    'verses': verses,
    'study_notes': study_notes
}

storage.save_chapter_data('Genesis', 1, data)

# Or use direct JSON saving
output_path = f"data/processed/Genesis_1.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

### Save as CSV
```python
import csv

# Save verses to CSV
csv_path = f"data/processed/Genesis_1.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['number', 'text'])
    writer.writeheader()
    writer.writerows(verses)
```

## Testing Requirements

### Test Structure
```python
import pytest
from src.parsers.html_parser import StudyBibleParser

class TestHTMLParser:
    """Tests for HTML parser."""
    
    def test_extract_verses(self, sample_html):
        """Test verse extraction from HTML."""
        parser = StudyBibleParser(sample_html)
        verses = parser.extract_verses()
        
        assert len(verses) > 0
        assert 'number' in verses[0]
        assert 'text' in verses[0]
```

### Use Fixtures
```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_html():
    """Sample HTML for testing."""
    return """
    <html>
        <p class="verse">
            <span class="v">1</span>
            In the beginning...
        </p>
    </html>
    """
```

### Mark Integration Tests
```python
@pytest.mark.integration
@pytest.mark.skip(reason="Requires live website access")
def test_scrape_live_chapter():
    """Test scraping from actual JW.org website."""
    # This test is skipped by default to avoid hitting the live site
    pass
```

## Key CSS Selectors (from config.py)

Always use selectors from `src/config.py`:

```python
from src.config import SELECTORS

# Verses
verse_selector = SELECTORS['verse']          # 'p.verse'
verse_number = SELECTORS['verse_number']     # 'span.v'

# Study materials
study_note = SELECTORS['study_note']         # 'div.studyNote'
footnote = SELECTORS['footnote']             # 'div.footnote'
cross_ref = SELECTORS['cross_reference']     # 'div.crossReference'
```

## Things to NEVER Do

1. **Never hardcode URLs** - Always use `config.py` for base URLs
2. **Never skip rate limiting** - Always add delays between requests
3. **Never ignore errors** - Always use try-except and log errors
4. **Never commit secrets** - Use environment variables for sensitive data
5. **Never use `time.sleep()` in browser automation** - Use explicit waits
6. **Never scrape without validation** - Always validate extracted data
7. **Never ignore PEP 8** - Code must follow Python standards
8. **Never skip docstrings** - All public functions need documentation
9. **Never use generic exception handlers** - Catch specific exceptions
10. **Never commit test data to git** - Use fixtures and mock data

## When in Doubt

1. Check existing code in the repository for patterns
2. Refer to documentation in `docs/` directory
3. Use Playwright MCP tools (not Selenium) for new scraping code
4. Add tests for new functionality
5. Follow the existing project structure
6. Ask for clarification rather than making assumptions
