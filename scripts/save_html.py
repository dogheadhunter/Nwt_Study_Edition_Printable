#!/usr/bin/env python3
"""
Save HTML from Playwright browser.

This script saves HTML content extracted from a Playwright browser session
to the data/samples directory. Run from any directory within the project.
"""
# This will be run after getting HTML via playwright_browser_evaluate
import sys
from pathlib import Path

# Get the project root directory
# __file__ is the path to this script (scripts/save_html.py)
# .parent gets the scripts/ folder, .parent.parent gets the project root
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
