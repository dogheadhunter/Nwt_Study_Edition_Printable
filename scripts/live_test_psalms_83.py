#!/usr/bin/env python3
"""Live testing script for Psalms 83."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scrapers.psalms_scraper import Psalms83Scraper
from src.utils.validators import validate_chapter_completeness, validate_psalms_83_specific

scraper = Psalms83Scraper(data_dir="data")

print("PSALMS 83 LIVE TESTING")
print("=" * 70)
print(f"\nURL: {scraper.PSALMS_83_URL}")
print("\nPlaywright MCP Commands:")
print("1. playwright-browser_navigate(url='{}')".format(scraper.PSALMS_83_URL))
print("2. playwright-browser_wait_for(text='Psalm 83', time=5)")
print("3. html = playwright-browser_evaluate(function='() => document.body.innerHTML')")
print("\nThen paste HTML to parse...")
