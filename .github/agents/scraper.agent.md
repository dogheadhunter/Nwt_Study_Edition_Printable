---
name: scraper
description: Web scraping using Playwright MCP.
tools: ['playwright/*', 'filesystem/*']
handoffs:
  - agent: parser
    button: "📄 Parse HTML"
  - agent: tester
    button: "🧪 Create Tests"
---

# Scraper Agent

Web scraping using Playwright MCP tools for NWT Study Edition.

## Playwright MCP Tools

| Tool | Purpose |
|------|---------|
| `playwright-browser_navigate(url)` | Go to URL |
| `playwright-browser_wait_for(text)` | Wait for content |
| `playwright-browser_snapshot()` | Get page structure (use to find refs) |
| `playwright-browser_click(element, ref)` | Click element |
| `playwright-browser_evaluate(function)` | Execute JS |
| `playwright-browser_close()` | Close browser |

## Scraping Pattern

```python
# 1. Navigate
playwright-browser_navigate(url="https://www.jw.org/.../genesis/1/")

# 2. Wait for content (ALWAYS do this)
playwright-browser_wait_for(text="verse 1")

# 3. Get snapshot to find element refs
snapshot = playwright-browser_snapshot()

# 4. Extract HTML
html = playwright-browser_evaluate(function="() => document.body.innerHTML")

# 5. Rate limit between pages
import time
time.sleep(3)  # Minimum 3 seconds
```

## Key Rules

- Always wait for content before extracting
- Use `playwright-browser_wait_for(text=...)` not `time.sleep`
- Minimum 3s delay between page navigations
- Get refs from `playwright-browser_snapshot()` before clicking
- Always close browser when done
