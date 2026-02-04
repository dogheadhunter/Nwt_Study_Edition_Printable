# Integration Tests

This directory contains integration tests for the NWT Study Edition scraper.

## Overview

Integration tests verify the complete scraping workflow against live data from JW.org. These tests are separated from unit tests because they:

- Require network access
- May be blocked by site restrictions
- Take longer to execute
- Depend on external site availability

## Running Integration Tests

### Run all integration tests
```bash
pytest tests/integration -m integration -v
```

### Run only Psalms 83 tests
```bash
pytest tests/integration/test_psalms_83_live.py -v
```

### Run with detailed output
```bash
pytest tests/integration -m integration -v -s --tb=long
```

### Skip integration tests (run only unit tests)
```bash
pytest tests/ -m "not integration"
```

## Test Categories

### Markers Used

- `@pytest.mark.integration` - All integration tests
- `@pytest.mark.jw_org` - Requires JW.org access
- `@pytest.mark.playwright` - Uses Playwright browser automation
- `@pytest.mark.live` - Requires live internet access

### Test Classes

1. **TestPsalms83LiveScraping** - Live scraping tests
   - Tests complete workflow with Playwright MCP
   - Most tests are skipped by default (require manual execution)
   - Demonstrates expected workflow

2. **TestPsalms83DataValidation** - Data structure validation
   - Validates sample data against expected structure
   - Can run without network access
   - Fast execution

3. **TestPsalms83Comparison** - Live vs sample comparison
   - Detects content changes on JW.org
   - Requires successful live scraping

## Manual Test Execution with Playwright MCP

Since these tests use Playwright MCP tools (not available in automated test runs), follow this manual workflow:

### 1. Start Playwright browser
```python
# Via Copilot or MCP tools
playwright-browser_navigate(url="https://www.jw.org/en/library/bible/study-bible/books/psalms/83/")
```

### 2. Wait for content
```python
playwright-browser_wait_for(text="Psalm 83", time=5)
```

### 3. Extract HTML
```python
html = playwright-browser_evaluate(function="() => document.body.innerHTML")
```

### 4. Parse and validate
```python
from src.scrapers.psalms_scraper import Psalms83Scraper

scraper = Psalms83Scraper()
data = scraper.parse_html_content(html)

# Run validators
from src.utils.validators import validate_chapter_completeness, validate_psalms_83_specific

errors = validate_chapter_completeness(data, expected_verses=18)
ps83_errors = validate_psalms_83_specific(data)

assert len(errors) == 0, f"Validation errors: {errors}"
assert len(ps83_errors) == 0, f"Psalms 83 errors: {ps83_errors}"
```

## Graceful Skipping

Tests automatically skip when:

- Network is unavailable (`check_network_available()`)
- JW.org is blocked or down (`skip_if_jw_org_blocked` fixture)
- Playwright MCP tools are not available

## Expected Test Results

### Successful Run
```
tests/integration/test_psalms_83_live.py::TestPsalms83DataValidation::test_sample_data_structure_valid PASSED
tests/integration/test_psalms_83_live.py::TestPsalms83DataValidation::test_sample_verses_sequential PASSED
tests/integration/test_psalms_83_live.py::TestPsalms83DataValidation::test_sample_verse_18_content PASSED
```

### Skipped Tests (Expected)
```
tests/integration/test_psalms_83_live.py::TestPsalms83LiveScraping::test_navigate_to_psalms_83 SKIPPED
  (Requires manual Playwright MCP execution)
```

## Troubleshooting

### Test Skipped: "JW.org not accessible"
- Check network connection
- Verify JW.org is not blocked by firewall
- Site may be temporarily down

### Test Skipped: "Requires Playwright MCP tools"
- These tests document the manual workflow
- Execute steps manually using Playwright MCP tools
- Update test to remove skip marker if running in MCP environment

### Validation Errors
- Compare with sample data in `data/samples/psalms_83_sample.json`
- Check if JW.org updated their content
- Verify CSS selectors are still correct

## Contributing

When adding new integration tests:

1. Mark with appropriate markers (`@pytest.mark.integration`, etc.)
2. Use `skip_if_jw_org_blocked` fixture for network-dependent tests
3. Document expected behavior clearly
4. Add to this README if introducing new test patterns
