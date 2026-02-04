#!/usr/bin/env python3
"""
Save HTML from Playwright browser.
"""
# This will be run after getting HTML via playwright_browser_evaluate
import sys
from pathlib import Path

# Get the project root directory (scripts folder is one level down from root)
project_root = Path(__file__).parent.parent

# The HTML will be passed as a command line argument
if len(sys.argv) > 1:
    html = sys.argv[1]
    output_path = project_root / 'data' / 'samples' / 'psalms_83_live.html'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Saved {len(html):,} characters to {output_path}")
else:
    print("Usage: python scripts/save_html.py '<html_content>'")
