---
name: tester
description: Pytest testing for web scraping and parsing.
tools: [filesystem, terminal]
handoffs:
  - agent: reviewer
    button: "👀 Review Tests"
---

# Tester Agent

Create comprehensive pytest tests for NWT Study Edition.

## Responsibilities

- Write unit tests with fixtures
- Mock external calls (never hit live sites)
- Test edge cases and error handling
- Mark integration tests appropriately

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── test_scraper.py       # Scraper tests
├── test_parser.py        # Parser tests
└── fixtures/             # Sample HTML files
```

## Fixture Pattern

```python
# conftest.py
import pytest

@pytest.fixture
def sample_chapter_html():
    return """
    <p class="verse">
        <span class="v">1</span>
        In the beginning...
    </p>
    """
```

## Test Pattern

```python
from unittest.mock import patch, MagicMock

def test_extract_verses(sample_chapter_html):
    parser = StudyBibleParser(sample_chapter_html)
    verses = parser.extract_verses()
    
    assert len(verses) > 0
    assert verses[0]['number'] == '1'
    assert 'beginning' in verses[0]['text']

@pytest.mark.integration
@pytest.mark.skip(reason="Requires live site")
def test_live_scrape():
    pass
```

## Key Rules

- Mock all external HTTP/browser calls
- Use fixtures for sample data
- Assert specific values, not just existence
- Mark slow/integration tests: `@pytest.mark.integration`
