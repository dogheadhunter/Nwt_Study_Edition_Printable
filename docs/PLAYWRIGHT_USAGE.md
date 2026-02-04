# Playwright MCP Usage Guide

## Overview

This project uses **Playwright via Model Context Protocol (MCP)** for web scraping. This approach provides several advantages over traditional Selenium:

- **No Driver Management**: No need to install or manage ChromeDriver
- **Better Performance**: Faster and more reliable than Selenium
- **Built-in Waiting**: Smart waiting for elements and page loads
- **Rich Inspection Tools**: Accessibility snapshots for easy element identification
- **Screenshot Capabilities**: Easy visual documentation

## MCP Tools Available

### Navigation

#### `playwright-browser_navigate`
Navigate to a URL.

```python
playwright-browser_navigate(url="https://www.jw.org/en/library/bible/study-bible/books/")
```

#### `playwright-browser_navigate_back`
Go back to the previous page.

```python
playwright-browser_navigate_back()
```

### Page Interaction

#### `playwright-browser_click`
Click on an element.

```python
playwright-browser_click(
    element="Genesis link",
    ref="<reference from snapshot>"
)
```

#### `playwright-browser_type`
Type text into an input field.

```python
playwright-browser_type(
    element="Search box",
    ref="<reference>",
    text="Genesis",
    submit=True  # Press Enter after typing
)
```

#### `playwright-browser_hover`
Hover over an element (useful for tooltips, dropdowns).

```python
playwright-browser_hover(
    element="Study note marker",
    ref="<reference>"
)
```

#### `playwright-browser_press_key`
Press keyboard keys.

```python
playwright-browser_press_key(key="Enter")
playwright-browser_press_key(key="ArrowDown")
```

### Page Inspection

#### `playwright-browser_snapshot`
Get an accessibility snapshot of the page.

```python
snapshot = playwright-browser_snapshot()
```

Returns a text representation of the page structure:
```
heading "New World Translation Study Bible"
  link "Genesis"
  link "Exodus"
  text "In the beginning..."
```

#### `playwright-browser_take_screenshot`
Take a screenshot of the page or specific element.

```python
# Full page screenshot
playwright-browser_take_screenshot(
    filename="books_list.png",
    fullPage=True
)

# Element screenshot
playwright-browser_take_screenshot(
    element="First verse",
    ref="<reference>",
    filename="verse1.png"
)
```

### Waiting

#### `playwright-browser_wait_for`
Wait for text to appear/disappear or wait for a specific time.

```python
# Wait for text
playwright-browser_wait_for(text="Genesis")

# Wait for text to disappear
playwright-browser_wait_for(textGone="Loading...")

# Wait for specific time (seconds)
playwright-browser_wait_for(time=2)
```

### Browser Management

#### `playwright-browser_close`
Close the browser.

```python
playwright-browser_close()
```

#### `playwright-browser_tabs`
Manage browser tabs.

```python
# List all tabs
playwright-browser_tabs(action="list")

# Create new tab
playwright-browser_tabs(action="new")

# Close current tab
playwright-browser_tabs(action="close")

# Select specific tab
playwright-browser_tabs(action="select", index=0)
```

## Scraping Workflow

### Step 1: Navigate to Page

```python
# Navigate to books list
playwright-browser_navigate(
    url="https://www.jw.org/en/library/bible/study-bible/books/"
)

# Wait for page to load
playwright-browser_wait_for(time=2)
```

### Step 2: Inspect Page Structure

```python
# Get page snapshot
snapshot = playwright-browser_snapshot()

# Analyze the snapshot to find elements
# Look for patterns like:
#   link "Genesis"
#   button "Chapter 1"
#   heading "Verse 1"
```

### Step 3: Extract Data

From the snapshot, identify the elements you need and extract their text.

Example snapshot analysis:
```
heading "Books of the Bible"
  list
    listitem
      link "Genesis"
    listitem
      link "Exodus"
```

### Step 4: Navigate to Details

```python
# Click on a book
playwright-browser_click(
    element="Genesis link",
    ref="<ref from snapshot>"
)

# Wait for chapter page
playwright-browser_wait_for(time=1)

# Get new snapshot
chapter_snapshot = playwright-browser_snapshot()
```

### Step 5: Extract Chapter Content

```python
# Take screenshot for documentation
playwright-browser_take_screenshot(
    filename="genesis_chapter1.png"
)

# Get detailed snapshot
content = playwright-browser_snapshot()

# Parse verses from snapshot
# Look for patterns indicating verses
```

### Step 6: Handle Dynamic Content

For study notes that appear on click:

```python
# Click study note marker
playwright-browser_click(
    element="Study note for verse 1",
    ref="<ref>"
)

# Wait for study pane
playwright-browser_wait_for(time=0.5)

# Get updated snapshot with note visible
note_snapshot = playwright-browser_snapshot()
```

### Step 7: Clean Up

```python
# Close browser
playwright-browser_close()
```

## Parsing Snapshots

### Understanding Snapshot Format

Playwright snapshots return an accessibility tree in text format:

```
heading "Title" level=1
  paragraph
    text "This is some text"
  list
    listitem
      link "Link text"
```

### Parsing Example

```python
def parse_links_from_snapshot(snapshot_text):
    """Extract links from a snapshot."""
    links = []
    for line in snapshot_text.split('\n'):
        if 'link "' in line:
            # Extract text between quotes
            start = line.find('"') + 1
            end = line.find('"', start)
            if end > start:
                link_text = line[start:end]
                links.append(link_text)
    return links
```

### Finding Element References

When you need to click an element, find its reference in the snapshot:

```
link "Genesis"  # This is the element
```

The reference is the entire line or a unique identifier from it.

## Best Practices

### 1. Wait Appropriately

```python
# After navigation, wait for content
playwright-browser_navigate(url)
playwright-browser_wait_for(time=2)

# After clicks, wait for dynamic content
playwright-browser_click(element, ref)
playwright-browser_wait_for(time=0.5)
```

### 2. Take Screenshots for Debugging

```python
# Take screenshot before and after actions
playwright-browser_take_screenshot(filename="before.png")
playwright-browser_click(element, ref)
playwright-browser_take_screenshot(filename="after.png")
```

### 3. Use Snapshots Liberally

```python
# Get snapshot after each navigation
snapshot1 = playwright-browser_snapshot()

# Click something
playwright-browser_click(element, ref)

# Get new snapshot to see changes
snapshot2 = playwright-browser_snapshot()
```

### 4. Handle Errors Gracefully

```python
try:
    playwright-browser_navigate(url)
    playwright-browser_wait_for(text="Expected text")
except TimeoutError:
    # Handle timeout
    pass
```

### 5. Rate Limiting

```python
import time

# Wait between requests
playwright-browser_navigate(url1)
time.sleep(2)

playwright-browser_navigate(url2)
time.sleep(2)
```

## Example: Complete Scraping Script

```python
# Step 1: Navigate
playwright-browser_navigate(
    url="https://www.jw.org/en/library/bible/study-bible/books/"
)
playwright-browser_wait_for(time=2)

# Step 2: Get books list
books_snapshot = playwright-browser_snapshot()
books = parse_links_from_snapshot(books_snapshot)

# Step 3: Navigate to first book
playwright-browser_click(
    element=books[0],  # "Genesis"
    ref="<ref from snapshot>"
)
playwright-browser_wait_for(time=1)

# Step 4: Get chapter
chapter_snapshot = playwright-browser_snapshot()

# Step 5: Extract verses
verses = parse_verses_from_snapshot(chapter_snapshot)

# Step 6: Get study notes (if any)
# Click first study note marker
playwright-browser_click(
    element="Study note marker",
    ref="<ref>"
)
playwright-browser_wait_for(time=0.5)

# Get note content
note_snapshot = playwright-browser_snapshot()

# Step 7: Save screenshot
playwright-browser_take_screenshot(
    filename="genesis_with_notes.png",
    fullPage=True
)

# Step 8: Close
playwright-browser_close()
```

## Comparison with Selenium

| Feature | Playwright MCP | Selenium |
|---------|---------------|----------|
| Setup | No installation needed | Requires ChromeDriver |
| Speed | Faster | Slower |
| Stability | More stable | Can be flaky |
| Waiting | Built-in smart waiting | Manual waits needed |
| Inspection | Accessibility snapshots | Manual element finding |
| Screenshots | Built-in | Requires extra code |
| Multi-browser | Chromium, Firefox, WebKit | Chrome, Firefox, etc. |

## Troubleshooting

### Element Not Found

**Problem**: Can't find element reference in snapshot

**Solution**:
1. Take a screenshot to see the page
2. Get a fresh snapshot
3. Look for alternative text or patterns
4. Try waiting longer for content to load

### Page Not Loading

**Problem**: Timeout waiting for page

**Solution**:
1. Increase wait time
2. Check if site is accessible
3. Look for error messages in screenshot
4. Try navigating to a simpler URL first

### Dynamic Content Not Appearing

**Problem**: Clicked element but content didn't load

**Solution**:
1. Increase wait time after click
2. Check screenshot to verify click worked
3. Try hovering before clicking
4. Look for loading indicators to wait for

### Site Blocking Automated Access

**Problem**: Site returns 403 or blocks request

**Solution**:
1. Add delays between requests (2-5 seconds)
2. This is expected for jw.org - respect their blocking
3. Consider reaching out for API access
4. Use cached/sample data for testing

## Next Steps

1. **Try the Examples**: Run `python examples/playwright_mcp_guide.py`
2. **Run Tests**: Run `pytest tests/test_playwright_scraper.py`
3. **Build Your Scraper**: Use the patterns above to build scrapers
4. **Read More**: Check official Playwright docs for advanced features

## Additional Resources

- [Playwright Documentation](https://playwright.dev/)
- [MCP Protocol Specification](https://modelcontextprotocol.org/)
- Project examples in `examples/playwright_mcp_guide.py`
- Test examples in `tests/test_playwright_scraper.py`
