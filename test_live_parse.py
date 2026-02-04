"""
Quick test script to parse the live Psalms 83 HTML extracted via Playwright.
"""
import sys
sys.path.insert(0, 'src')

from scrapers.psalms_scraper import Psalms83Scraper
from utils.validators import validate_chapter_completeness, validate_psalms_83_specific
import json

# Read the HTML from the live extraction
html_content = """[HTML content will be pasted here]"""

# Initialize scraper
scraper = Psalms83Scraper(data_dir='data')

# Parse the HTML
print("Parsing Psalms 83 HTML...")
data = scraper.parse_html_content(html_content)

# Validate the data
print("\n=== VALIDATION RESULTS ===")
errors = validate_chapter_completeness(data, expected_verses=18)
if errors:
    print("Chapter completeness errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✓ Chapter completeness: PASSED")

ps83_errors = validate_psalms_83_specific(data)
if ps83_errors:
    print("\nPsalms 83 specific errors:")
    for error in ps83_errors:
        print(f"  - {error}")
else:
    print("✓ Psalms 83 specific: PASSED")

# Display summary
print("\n=== EXTRACTION SUMMARY ===")
print(f"Book: {data.get('book', 'N/A')}")
print(f"Chapter: {data.get('chapter', 'N/A')}")
print(f"Total verses: {len(data.get('verses', []))}")
print(f"Superscription: {'Yes' if data.get('superscription') else 'No'}")
print(f"Study notes: {len(data.get('study_notes', []))}")
print(f"Footnotes: {len(data.get('footnotes', []))}")
print(f"Cross references: {len(data.get('cross_references', []))}")

# Show first verse
if data.get('verses'):
    print(f"\nFirst verse:")
    print(f"  Number: {data['verses'][0].get('number')}")
    print(f"  Text: {data['verses'][0].get('text')[:100]}...")

# Show last verse (should contain "Jehovah")
if len(data.get('verses', [])) >= 18:
    print(f"\nVerse 18 (should contain 'Jehovah'):")
    print(f"  Number: {data['verses'][17].get('number')}")
    print(f"  Text: {data['verses'][17].get('text')}")

# Save to file
output_file = 'data/processed/live_test_psalms_83.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"\nSaved results to: {output_file}")
