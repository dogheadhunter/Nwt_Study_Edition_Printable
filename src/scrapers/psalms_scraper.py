"""
Psalms 83 Scraper Workflow

This module provides the workflow for scraping Psalms 83 from the JW.org
Study Bible using Playwright MCP tools.

The workflow is designed to:
1. Navigate to the Psalms 83 page
2. Extract verses, study notes, footnotes, and cross-references
3. Parse and format the content
4. Save the structured data

Note: JW.org may block automated access. This module provides both:
- Live scraping workflow (when access is available)
- Sample data fallback (for testing and development)
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any

from bs4 import BeautifulSoup

# Import selectors from config
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import SELECTORS, SCRAPING_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Psalms83Scraper:
    """
    Scraper specifically for Psalms 83 content.
    
    This class provides methods to scrape, parse, and format Psalms 83
    from the JW.org Study Bible.
    """
    
    BASE_URL = "https://www.jw.org/en/library/bible/study-bible/books/"
    PSALMS_83_URL = "https://www.jw.org/en/library/bible/study-bible/books/psalms/83/"
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the Psalms 83 scraper.
        
        Args:
            data_dir: Base directory for data storage
        """
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, "raw")
        self.processed_dir = os.path.join(data_dir, "processed")
        self.samples_dir = os.path.join(data_dir, "samples")
        
        # Create directories if they don't exist
        for directory in [self.raw_dir, self.processed_dir, self.samples_dir]:
            os.makedirs(directory, exist_ok=True)
            
        logger.info("Psalms83Scraper initialized")
    
    def get_scraping_workflow(self) -> Dict[str, Any]:
        """
        Get the complete workflow for scraping Psalms 83 using Playwright MCP.
        
        Returns:
            Dictionary containing step-by-step workflow instructions
        """
        return {
            "workflow": "Psalms 83 Scraping",
            "target_url": self.PSALMS_83_URL,
            "steps": [
                {
                    "step": 1,
                    "action": "Navigate to Psalms 83",
                    "tool": "playwright-browser_navigate",
                    "params": {"url": self.PSALMS_83_URL},
                    "description": "Navigate to the Psalms 83 chapter page"
                },
                {
                    "step": 2,
                    "action": "Wait for content to load",
                    "tool": "playwright-browser_wait_for",
                    "params": {"time": 3},
                    "description": "Wait for dynamic content to load"
                },
                {
                    "step": 3,
                    "action": "Take screenshot",
                    "tool": "playwright-browser_take_screenshot",
                    "params": {
                        "filename": "psalms_83_page.jpeg",
                        "fullPage": True,
                        "type": "jpeg"
                    },
                    "description": "Capture screenshot of the page (JPEG format)"
                },
                {
                    "step": 4,
                    "action": "Get page snapshot",
                    "tool": "playwright-browser_snapshot",
                    "params": {},
                    "description": "Get accessibility snapshot for element identification"
                },
                {
                    "step": 5,
                    "action": "Extract HTML",
                    "tool": "playwright-browser_evaluate",
                    "params": {"function": "() => document.body.innerHTML"},
                    "description": "Get raw HTML for parsing with BeautifulSoup"
                },
                {
                    "step": 6,
                    "action": "Parse content",
                    "method": "parse_html_content",
                    "description": "Use BeautifulSoup to extract structured data"
                },
                {
                    "step": 7,
                    "action": "Format and save",
                    "method": "save_chapter_data",
                    "description": "Save formatted data to JSON"
                }
            ],
            "expected_output": {
                "verses": "18 verses",
                "study_notes": "Multiple study notes on key verses",
                "footnotes": "Footnote about Selah",
                "cross_references": "References to Judges, Genesis, etc."
            }
        }
    
    def parse_html_content(self, html_content: str) -> Dict[str, Any]:
        """
        Parse Psalms 83 HTML content using BeautifulSoup.
        
        Args:
            html_content: Raw HTML string from the page
            
        Returns:
            Structured dictionary with extracted content
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        data = {
            "book": "Psalms",
            "chapter": 83,
            "url": self.PSALMS_83_URL,
            "superscription": self._extract_superscription(soup),
            "verses": self._extract_verses(soup),
            "study_notes": self._extract_study_notes(soup),
            "footnotes": self._extract_footnotes(soup),
            "cross_references": self._extract_cross_references(soup),
            "metadata": {
                "scraped_at": datetime.now().isoformat(),
                "source": "jw.org Study Bible"
            }
        }
        
        # Add computed metadata
        data["metadata"]["total_verses"] = len(data["verses"])
        data["metadata"]["has_superscription"] = bool(data["superscription"])
        
        logger.info(f"Parsed Psalms 83: {len(data['verses'])} verses, "
                   f"{len(data['study_notes'])} study notes")
        
        return data
    
    def _extract_superscription(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract the psalm superscription if present."""
        # Use live-verified selectors first
        selectors = [
            'div#tt4',            # Psalms-specific (LIVE-VERIFIED)
            'sup',                # Generic superscription (LIVE-VERIFIED)
            '.superscription',    # Fallback
            '.psalm-heading',
            '.ss',
            'p.superscription'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                # Remove footnote/xref markers to get clean text
                for marker in elem.find_all('a', class_=['fn', 'study-note-ref']):
                    marker.extract()
                return elem.get_text(strip=True)
        
        return None
    
    def _extract_verses(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract all verses from the chapter."""
        verses = []
        
        # Use live-verified selectors first
        verse_selectors = [
            'p.sb',           # LIVE-VERIFIED: verse paragraphs
            'p[data-pid]',    # Fallback: paragraphs with data-pid
            'p.verse',        # Legacy fallback
            'span.verse',
            '.v'
        ]
        
        verse_elements = []
        for selector in verse_selectors:
            verse_elements = soup.select(selector)
            if verse_elements:
                logger.info(f"Found {len(verse_elements)} elements with selector: {selector}")
                break
        
        # Group verse paragraphs by verse number
        current_verse = None
        verse_parts = []
        
        for elem in verse_elements:
            verse_data = self._parse_verse_element(elem)
            if verse_data:
                # If this element has a verse number, start a new verse
                if verse_data.get('number') is not None:
                    # Save previous verse if exists
                    if current_verse:
                        verses.append(current_verse)
                    current_verse = verse_data
                    verse_parts = [verse_data['text']]
                # Otherwise, append text to current verse
                elif current_verse and verse_data.get('text'):
                    verse_parts.append(verse_data['text'])
                    current_verse['text'] = ' '.join(verse_parts)
                    # Merge markers
                    current_verse['footnotes'].extend(verse_data.get('footnotes', []))
                    current_verse['cross_references'].extend(verse_data.get('cross_references', []))
        
        # Add the last verse
        if current_verse:
            verses.append(current_verse)
        
        return verses
    
    def _parse_verse_element(self, elem) -> Optional[Dict[str, Any]]:
        """Parse a single verse element."""
        try:
            # Make a copy to avoid modifying original
            elem_copy = elem.__copy__()
            
            # Extract verse number (LIVE-VERIFIED: span.verseNum)
            verse_num_elem = elem_copy.find('span', class_='verseNum')
            verse_number = None
            if verse_num_elem:
                verse_text = verse_num_elem.get_text(strip=True)
                # Extract just the number
                match = re.search(r'\d+', verse_text)
                if match:
                    verse_number = int(match.group())
                verse_num_elem.extract()  # Remove to get clean text
            
            # Extract footnote markers (LIVE-VERIFIED: a.fn)
            footnote_markers = elem_copy.find_all('a', class_='fn')
            footnotes = []
            for marker in footnote_markers:
                # Get the marker text (usually "*")
                marker_text = marker.get_text(strip=True)
                footnotes.append(marker_text)
                marker.extract()  # Remove marker from text
            
            # Extract cross-reference markers (LIVE-VERIFIED: a.study-note-ref)
            xref_markers = elem_copy.find_all('a', class_='study-note-ref')
            cross_refs = []
            for marker in xref_markers:
                # Get the reference letter (a, b, c, etc.)
                ref_letter = marker.get_text(strip=True)
                cross_refs.append(ref_letter)
                marker.extract()  # Remove marker from text
            
            # Get clean text
            text = elem_copy.get_text(strip=True)
            
            if verse_number is not None or text:
                return {
                    "number": verse_number,
                    "text": text,
                    "footnotes": footnotes,
                    "cross_references": cross_refs
                }
            
        except Exception as e:
            logger.error(f"Error parsing verse element: {e}")
        
        return None
    
    def _extract_study_notes(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract study notes from the tabbed sidebar."""
        notes = []
        
        # Use live-verified selector for study notes section in sidebar
        notes_section = soup.select_one(SELECTORS['study_note_section'])
        
        if notes_section:
            # Find all study note list items
            note_items = notes_section.find_all('li')
            
            for item in note_items:
                try:
                    note_id = item.get('id', '')
                    
                    # Extract verse reference (e.g., "83:1")
                    ref_elem = item.find('a', class_='b')
                    reference = ref_elem.get_text(strip=True) if ref_elem else ''
                    
                    # Get full note content
                    content = item.get_text(strip=True)
                    
                    if content:
                        notes.append({
                            "id": note_id,
                            "reference": reference,
                            "content": content
                        })
                except Exception as e:
                    logger.error(f"Error parsing study note: {e}")
        
        return notes
    
    def _parse_study_note_element(self, elem) -> Optional[Dict[str, Any]]:
        """Parse a single study note element."""
        try:
            note_id = elem.get('id', '')
            
            # Extract reference
            ref_elem = elem.find(['span', 'strong'], class_=['reference', 'ref'])
            reference = ref_elem.get_text(strip=True) if ref_elem else ''
            
            # Extract content
            content_elem = elem.find(['div', 'p'], class_=['content', 'noteContent'])
            content = content_elem.get_text(strip=True) if content_elem else elem.get_text(strip=True)
            
            return {
                "id": note_id,
                "reference": reference,
                "content": content
            }
            
        except Exception as e:
            logger.error(f"Error parsing study note: {e}")
        
        return None
    
    def _extract_footnotes(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract footnotes from the tabbed sidebar."""
        footnotes = []
        
        # Use live-verified selector for footnotes section in sidebar
        footnote_section = soup.select_one(SELECTORS['footnote_section'])
        
        if footnote_section:
            # Find all footnote list items
            footnote_items = footnote_section.find_all('li')
            
            for item in footnote_items:
                try:
                    footnote_id = item.get('id', '')
                    
                    # Extract footnote marker/reference (e.g., "a" or "b")
                    marker_elem = item.find('a', class_='fn')
                    marker = marker_elem.get_text(strip=True) if marker_elem else ''
                    
                    # Get full content
                    content = item.get_text(strip=True)
                    
                    if content:
                        footnotes.append({
                            "id": footnote_id,
                            "marker": marker,
                            "content": content
                        })
                except Exception as e:
                    logger.error(f"Error parsing footnote: {e}")
        
        return footnotes
    
    def _extract_cross_references(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract cross-references from the tabbed sidebar including full verse text.
        
        Cross-references are stored in div.xRef containers with collapsed sections
        (div.jsCollapsableBlock) that contain the actual verse text in div.xRefVerse elements.
        """
        cross_refs = []
        
        # Find all cross-reference containers (not using section selector)
        xref_containers = soup.find_all('div', class_='xRef')
        
        for container in xref_containers:
            try:
                xref_data = {
                    'id': container.get('data-id', ''),
                    'verse_id': container.get('data-vs-id', ''),
                    'marker': '',
                    'citation': '',
                    'verses': []
                }
                
                # Get marker and citation from the header
                marker_elem = container.find('span', class_='xRefID')
                if marker_elem:
                    xref_data['marker'] = marker_elem.get_text(strip=True)
                
                citation_elem = container.find('span', class_='targetCitation')
                if citation_elem:
                    xref_data['citation'] = citation_elem.get_text(strip=True)
                
                # Get verse content from the collapsible block
                collapsible = container.find('div', class_='jsCollapsableBlock')
                if collapsible:
                    verse_elements = collapsible.find_all('div', class_='xRefVerse')
                    
                    for verse_elem in verse_elements:
                        # Extract citation (e.g., "Exodus 1:8-10")
                        citation = verse_elem.find('span', class_='xRefCitation')
                        
                        # Extract category (e.g., "General")
                        category = verse_elem.find('span', class_='xRefCategory')
                        
                        # Extract the actual verse text
                        content = verse_elem.find('p', class_='xRefContent')
                        
                        verse_data = {
                            'citation': citation.get_text(strip=True) if citation else '',
                            'category': category.get_text(strip=True) if category else '',
                            'content': content.get_text(strip=True) if content else ''
                        }
                        
                        # Only add if has content
                        if verse_data['citation'] or verse_data['content']:
                            xref_data['verses'].append(verse_data)
                
                # Only add cross-reference if it has a marker
                if xref_data['marker']:
                    cross_refs.append(xref_data)
                    
            except Exception as e:
                logger.error(f"Error parsing cross-reference container: {e}")
        
        return cross_refs
    
    def save_chapter_data(self, data: Dict[str, Any], filename: str = None) -> str:
        """
        Save parsed chapter data to JSON file.
        
        Args:
            data: Structured chapter data
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"psalms_83_{timestamp}.json"
        
        filepath = os.path.join(self.processed_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved Psalms 83 data to {filepath}")
        return filepath
    
    def load_sample_data(self) -> Dict[str, Any]:
        """
        Load sample Psalms 83 data for testing.
        
        Returns:
            Sample chapter data
        """
        sample_file = os.path.join(self.samples_dir, "psalms_83_sample.json")
        
        if os.path.exists(sample_file):
            with open(sample_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info("Loaded Psalms 83 sample data")
            return data
        else:
            logger.warning("Sample data file not found")
            return {}
    
    def format_for_print(self, data: Dict[str, Any]) -> str:
        """
        Format Psalms 83 data for readable print output.
        
        Args:
            data: Structured chapter data
            
        Returns:
            Formatted text string
        """
        lines = []
        
        # Header
        lines.append("=" * 60)
        lines.append(f"PSALM {data.get('chapter', 83)}")
        lines.append("=" * 60)
        
        # Superscription
        if data.get('superscription'):
            lines.append(f"\n{data['superscription']}\n")
        
        # Verses
        lines.append("")
        for verse in data.get('verses', []):
            verse_num = verse.get('number', '')
            verse_text = verse.get('text', '')
            lines.append(f"  {verse_num}  {verse_text}")
        
        # Study Notes
        if data.get('study_notes'):
            lines.append("\n" + "-" * 60)
            lines.append("STUDY NOTES")
            lines.append("-" * 60)
            for note in data['study_notes']:
                ref = note.get('reference', '')
                content = note.get('content', '')
                lines.append(f"\n{ref}")
                lines.append(f"  {content}")
        
        # Footnotes
        if data.get('footnotes'):
            lines.append("\n" + "-" * 60)
            lines.append("FOOTNOTES")
            lines.append("-" * 60)
            for fn in data['footnotes']:
                lines.append(f"\n  {fn.get('content', '')}")
        
        # Cross-References
        if data.get('cross_references'):
            lines.append("\n" + "-" * 60)
            lines.append("CROSS-REFERENCES")
            lines.append("-" * 60)
            for xref in data['cross_references']:
                ref = xref.get('reference', xref.get('id', ''))
                verses = ', '.join(xref.get('verses', []))
                lines.append(f"\n{ref}: {verses}")
        
        lines.append("\n" + "=" * 60)
        
        return '\n'.join(lines)
    
    def format_for_html(self, data: Dict[str, Any]) -> str:
        """
        Format Psalms 83 data as HTML for display.
        
        Args:
            data: Structured chapter data
            
        Returns:
            HTML formatted string
        """
        html_parts = []
        
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="en">')
        html_parts.append('<head>')
        html_parts.append('  <meta charset="UTF-8">')
        html_parts.append('  <title>Psalm 83 - NWT Study Edition</title>')
        html_parts.append('  <style>')
        html_parts.append('    body { font-family: Georgia, serif; max-width: 800px; margin: 0 auto; padding: 20px; }')
        html_parts.append('    h1 { text-align: center; color: #333; }')
        html_parts.append('    .superscription { font-style: italic; text-align: center; margin-bottom: 20px; }')
        html_parts.append('    .verse { margin: 10px 0; }')
        html_parts.append('    .verse-num { font-weight: bold; color: #666; margin-right: 5px; }')
        html_parts.append('    .study-notes { background: #f5f5f5; padding: 20px; margin-top: 30px; border-radius: 5px; }')
        html_parts.append('    .note { margin: 15px 0; }')
        html_parts.append('    .note-ref { font-weight: bold; color: #0066cc; }')
        html_parts.append('  </style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        
        # Header
        html_parts.append(f'  <h1>Psalm {data.get("chapter", 83)}</h1>')
        
        # Superscription
        if data.get('superscription'):
            html_parts.append(f'  <p class="superscription">{data["superscription"]}</p>')
        
        # Verses
        html_parts.append('  <div class="verses">')
        for verse in data.get('verses', []):
            verse_num = verse.get('number', '')
            verse_text = verse.get('text', '')
            html_parts.append(f'    <p class="verse"><span class="verse-num">{verse_num}</span> {verse_text}</p>')
        html_parts.append('  </div>')
        
        # Study Notes
        if data.get('study_notes'):
            html_parts.append('  <div class="study-notes">')
            html_parts.append('    <h2>Study Notes</h2>')
            for note in data['study_notes']:
                ref = note.get('reference', '')
                content = note.get('content', '')
                html_parts.append(f'    <div class="note">')
                html_parts.append(f'      <span class="note-ref">{ref}</span>')
                html_parts.append(f'      <p>{content}</p>')
                html_parts.append(f'    </div>')
            html_parts.append('  </div>')
        
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return '\n'.join(html_parts)


def main():
    """Main entry point demonstrating the Psalms 83 scraper."""
    scraper = Psalms83Scraper()
    
    print("Psalms 83 Scraper Workflow")
    print("=" * 60)
    
    # Show workflow
    workflow = scraper.get_scraping_workflow()
    print(f"\nTarget URL: {workflow['target_url']}")
    print("\nSteps:")
    for step in workflow['steps']:
        print(f"  {step['step']}. {step['action']}: {step['description']}")
    
    # Load and display sample data
    print("\n" + "=" * 60)
    print("Loading sample data...")
    data = scraper.load_sample_data()
    
    if data:
        print(f"\nLoaded Psalms {data.get('chapter', '?')}:")
        print(f"  Verses: {len(data.get('verses', []))}")
        print(f"  Study Notes: {len(data.get('study_notes', []))}")
        print(f"  Footnotes: {len(data.get('footnotes', []))}")
        
        # Show formatted output
        print("\n" + "=" * 60)
        print("Formatted for print:")
        print(scraper.format_for_print(data))
    else:
        print("No sample data available")


if __name__ == "__main__":
    main()
