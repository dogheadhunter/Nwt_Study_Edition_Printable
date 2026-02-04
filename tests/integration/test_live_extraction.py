#!/usr/bin/env python3
"""
Test script to verify Psalms 83 scraper captures all data components.
"""
import json
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.scrapers.psalms_scraper import Psalms83Scraper

# Simple validator functions
def validate_chapter_completeness(data):
    """Check if all 18 verses are present."""
    verses = data.get('verses', [])
    verse_numbers = {int(v['number']) for v in verses if v.get('number')}
    expected = set(range(1, 19))
    missing = expected - verse_numbers
    return len(missing) == 0, missing

def validate_psalms_83_specific(data):
    """Check Psalms 83 specific content."""
    checks = {}
    
    # Check for "Jehovah" in verse 18
    verse_18 = next((v for v in data.get('verses', []) if v.get('number') == '18'), None)
    checks['Has "Jehovah" in verse 18'] = verse_18 and 'Jehovah' in verse_18.get('text', '') if verse_18 else False
    
    # Check for superscription
    checks['Has superscription'] = bool(data.get('superscription'))
    checks['Superscription mentions Asaph'] = 'Aʹsaph' in data.get('superscription', '') if data.get('superscription') else False
    
    # Check for "Selah"
    verse_8 = next((v for v in data.get('verses', []) if v.get('number') == '8'), None)
    checks['Has "Selah" in verse 8'] = verse_8 and 'Selah' in verse_8.get('text', '') if verse_8 else False
    
    return checks


def print_section(title: str, data: any, indent: int = 0):
    """Print a formatted section of data."""
    prefix = "  " * indent
    print(f"\n{prefix}{'='*60}")
    print(f"{prefix}{title}")
    print(f"{prefix}{'='*60}")
    
    if isinstance(data, list):
        print(f"{prefix}Count: {len(data)}")
        for i, item in enumerate(data[:3], 1):  # Show first 3 items
            print(f"{prefix}[{i}] {item}")
        if len(data) > 3:
            print(f"{prefix}... and {len(data) - 3} more")
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"{prefix}{key}: {value[:100]}...")
            else:
                print(f"{prefix}{key}: {value}")
    else:
        print(f"{prefix}{data}")


def main():
    """Test Psalms 83 extraction with live HTML."""
    
    # Read the HTML file that was saved from Playwright
    html_file = project_root / 'data' / 'samples' / 'psalms_83_live.html'
    
    if not html_file.exists():
        print(f"❌ HTML file not found: {html_file}")
        print("Please save the live HTML first using Playwright MCP")
        return 1
    
    print("="*80)
    print("PSALMS 83 COMPREHENSIVE DATA EXTRACTION TEST")
    print("="*80)
    
    # Read HTML
    print("\n📄 Reading live HTML...")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    print(f"✅ Loaded {len(html_content):,} characters of HTML")
    
    # Parse with scraper
    print("\n🔍 Parsing with Psalms83Scraper...")
    scraper = Psalms83Scraper()
    data = scraper.parse_html_content(html_content)
    
    # Display results
    print("\n" + "="*80)
    print("EXTRACTION RESULTS")
    print("="*80)
    
    print(f"\n📖 Book: {data.get('book', 'N/A')}")
    print(f"📖 Chapter: {data.get('chapter', 'N/A')}")
    
    # Superscription
    if data.get('superscription'):
        print(f"\n📝 Superscription: {data['superscription']}")
    
    # Verses
    verses = data.get('verses', [])
    print_section(f"📜 VERSES ({len(verses)} total)", None)
    for verse in verses[:3]:
        print(f"\n  Verse {verse['number']}:")
        print(f"    Text: {verse['text'][:80]}...")
        if verse.get('footnotes'):
            print(f"    Footnote markers: {verse['footnotes']}")
        if verse.get('cross_references'):
            print(f"    Cross-ref markers: {verse['cross_references']}")
    if len(verses) > 3:
        print(f"\n  ... and {len(verses) - 3} more verses")
    
    # Footnotes
    footnotes = data.get('footnotes', [])
    print_section(f"📌 FOOTNOTES ({len(footnotes)} total)", None)
    for fn in footnotes[:3]:
        print(f"\n  [{fn.get('marker', '?')}] {fn.get('content', '')[:100]}...")
    if len(footnotes) > 3:
        print(f"\n  ... and {len(footnotes) - 3} more footnotes")
    
    # Cross-references
    cross_refs = data.get('cross_references', [])
    print_section(f"🔗 CROSS-REFERENCES ({len(cross_refs)} total)", None)
    for xref in cross_refs[:3]:
        print(f"\n  [{xref.get('marker', '?')}] Verses: {xref.get('verses', [])[:3]}")
        print(f"      Content: {xref.get('content', '')[:80]}...")
    if len(cross_refs) > 3:
        print(f"\n  ... and {len(cross_refs) - 3} more cross-references")
    
    # Study notes
    study_notes = data.get('study_notes', [])
    print_section(f"📚 STUDY NOTES ({len(study_notes)} total)", None)
    for note in study_notes[:3]:
        print(f"\n  Ref: {note.get('reference', '?')}")
        print(f"  Content: {note.get('content', '')[:100]}...")
    if len(study_notes) > 3:
        print(f"\n  ... and {len(study_notes) - 3} more study notes")
    
    # Validation
    print("\n" + "="*80)
    print("VALIDATION CHECKS")
    print("="*80)
    
    # Check verse count
    is_complete, missing = validate_chapter_completeness(data)
    if is_complete:
        print("✅ All 18 verses present")
    else:
        print(f"❌ Missing verses: {missing}")
    
    # Check Psalms 83 specific content
    checks = validate_psalms_83_specific(data)
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ Verses: {len(verses)}/18")
    print(f"✅ Footnotes: {len(footnotes)}")
    print(f"✅ Cross-references: {len(cross_refs)}")
    print(f"✅ Study notes: {len(study_notes)}")
    print(f"✅ Superscription: {'Yes' if data.get('superscription') else 'No'}")
    
    # Save results
    output_file = project_root / 'data' / 'processed' / 'psalms_83_live_test.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Full results saved to: {output_file}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
