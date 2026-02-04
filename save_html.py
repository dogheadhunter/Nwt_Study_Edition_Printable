#!/usr/bin/env python3
"""
Save HTML from Playwright browser.
"""
# This will be run after getting HTML via playwright_browser_evaluate
import sys

# The HTML will be passed as a command line argument
if len(sys.argv) > 1:
    html = sys.argv[1]
    with open('data/samples/psalms_83_live.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Saved {len(html):,} characters to psalms_83_live.html")
else:
    print("Usage: python save_html.py '<html_content>'")
