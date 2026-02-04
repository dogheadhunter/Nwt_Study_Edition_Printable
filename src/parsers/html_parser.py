"""
HTML Parser for JW.org Study Bible Content

This module provides utilities to parse HTML content from JW.org
and extract structured data including verses, study notes, and cross-references.
"""

from typing import Dict, List, Optional
from bs4 import BeautifulSoup, Tag
import re
import logging

logger = logging.getLogger(__name__)


class StudyBibleParser:
    """
    Parser for JW.org Study Bible HTML content.
    
    This class provides methods to extract and structure content
    from the HTML pages.
    """
    
    def __init__(self, html_content: str):
        """
        Initialize parser with HTML content.
        
        Args:
            html_content: Raw HTML string
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        
    def extract_verses(self) -> List[Dict[str, str]]:
        """
        Extract verses from the HTML content.
        
        Returns:
            List of verse dictionaries with number and text
        """
        verses = []
        
        # Note: These selectors are examples and will need to be adjusted
        # based on the actual HTML structure of the JW.org pages
        verse_elements = self.soup.find_all('p', class_='verse')
        
        for verse_elem in verse_elements:
            verse_data = self._parse_verse(verse_elem)
            if verse_data:
                verses.append(verse_data)
                
        logger.info(f"Extracted {len(verses)} verses")
        return verses
        
    def _parse_verse(self, verse_elem: Tag) -> Optional[Dict[str, str]]:
        """
        Parse a single verse element.
        
        Args:
            verse_elem: BeautifulSoup Tag representing a verse
            
        Returns:
            Dictionary with verse data or None
        """
        try:
            # Extract verse number
            verse_num_elem = verse_elem.find('span', class_='v')
            verse_number = verse_num_elem.get_text(strip=True) if verse_num_elem else None
            
            # Extract verse text (remove verse number)
            if verse_num_elem:
                verse_num_elem.extract()
            verse_text = verse_elem.get_text(strip=True)
            
            # Extract footnote markers
            footnote_markers = verse_elem.find_all('a', class_='footnoteLink')
            footnotes = [marker.get('data-footnote', '') for marker in footnote_markers]
            
            # Extract cross-reference markers
            ref_markers = verse_elem.find_all('a', class_='b')
            cross_refs = [ref.get('data-reflink', '') for ref in ref_markers]
            
            return {
                'number': verse_number,
                'text': verse_text,
                'footnotes': footnotes,
                'cross_references': cross_refs
            }
            
        except Exception as e:
            logger.error(f"Error parsing verse: {e}")
            return None
            
    def extract_study_notes(self) -> List[Dict[str, str]]:
        """
        Extract study notes from the HTML content.
        
        Returns:
            List of study note dictionaries
        """
        notes = []
        
        # Note: These selectors are examples and will need adjustment
        note_elements = self.soup.find_all('div', class_='studyNote')
        
        for note_elem in note_elements:
            note_data = self._parse_study_note(note_elem)
            if note_data:
                notes.append(note_data)
                
        logger.info(f"Extracted {len(notes)} study notes")
        return notes
        
    def _parse_study_note(self, note_elem: Tag) -> Optional[Dict[str, str]]:
        """
        Parse a single study note element.
        
        Args:
            note_elem: BeautifulSoup Tag representing a study note
            
        Returns:
            Dictionary with study note data or None
        """
        try:
            # Extract note ID
            note_id = note_elem.get('id', '')
            
            # Extract verse reference
            ref_elem = note_elem.find('span', class_='reference')
            reference = ref_elem.get_text(strip=True) if ref_elem else ''
            
            # Extract note content
            content_elem = note_elem.find('div', class_='content')
            content = content_elem.get_text(strip=True) if content_elem else note_elem.get_text(strip=True)
            
            return {
                'id': note_id,
                'reference': reference,
                'content': content
            }
            
        except Exception as e:
            logger.error(f"Error parsing study note: {e}")
            return None
            
    def extract_footnotes(self) -> List[Dict[str, str]]:
        """
        Extract footnotes from the HTML content.
        
        Returns:
            List of footnote dictionaries
        """
        footnotes = []
        
        footnote_elements = self.soup.find_all('div', class_='footnote')
        
        for footnote_elem in footnote_elements:
            footnote_data = self._parse_footnote(footnote_elem)
            if footnote_data:
                footnotes.append(footnote_data)
                
        logger.info(f"Extracted {len(footnotes)} footnotes")
        return footnotes
        
    def _parse_footnote(self, footnote_elem: Tag) -> Optional[Dict[str, str]]:
        """
        Parse a single footnote element.
        
        Args:
            footnote_elem: BeautifulSoup Tag representing a footnote
            
        Returns:
            Dictionary with footnote data or None
        """
        try:
            footnote_id = footnote_elem.get('id', '')
            content = footnote_elem.get_text(strip=True)
            
            return {
                'id': footnote_id,
                'content': content
            }
            
        except Exception as e:
            logger.error(f"Error parsing footnote: {e}")
            return None
            
    def extract_cross_references(self) -> List[Dict[str, str]]:
        """
        Extract cross-references from the HTML content.
        
        Returns:
            List of cross-reference dictionaries
        """
        cross_refs = []
        
        ref_elements = self.soup.find_all('div', class_='crossReference')
        
        for ref_elem in ref_elements:
            ref_data = self._parse_cross_reference(ref_elem)
            if ref_data:
                cross_refs.append(ref_data)
                
        logger.info(f"Extracted {len(cross_refs)} cross-references")
        return cross_refs
        
    def _parse_cross_reference(self, ref_elem: Tag) -> Optional[Dict[str, str]]:
        """
        Parse a single cross-reference element.
        
        Args:
            ref_elem: BeautifulSoup Tag representing a cross-reference
            
        Returns:
            Dictionary with cross-reference data or None
        """
        try:
            ref_id = ref_elem.get('id', '')
            
            # Extract referenced verses
            verse_links = ref_elem.find_all('a', class_='verseLink')
            verses = [link.get_text(strip=True) for link in verse_links]
            
            return {
                'id': ref_id,
                'verses': verses
            }
            
        except Exception as e:
            logger.error(f"Error parsing cross-reference: {e}")
            return None
            
    def extract_chapter_info(self) -> Dict[str, str]:
        """
        Extract chapter-level information.
        
        Returns:
            Dictionary with chapter metadata
        """
        chapter_info = {}
        
        # Extract book name
        book_elem = self.soup.find('h1', class_='bookName')
        if book_elem:
            chapter_info['book'] = book_elem.get_text(strip=True)
            
        # Extract chapter number
        chapter_elem = self.soup.find('span', class_='chapterNumber')
        if chapter_elem:
            chapter_info['chapter'] = chapter_elem.get_text(strip=True)
            
        # Extract introduction if present
        intro_elem = self.soup.find('div', class_='introduction')
        if intro_elem:
            chapter_info['introduction'] = intro_elem.get_text(strip=True)
            
        return chapter_info
        
    def parse_all(self) -> Dict:
        """
        Parse all content from the HTML.
        
        Returns:
            Complete structured data dictionary
        """
        return {
            'chapter_info': self.extract_chapter_info(),
            'verses': self.extract_verses(),
            'study_notes': self.extract_study_notes(),
            'footnotes': self.extract_footnotes(),
            'cross_references': self.extract_cross_references()
        }


def parse_html_file(file_path: str) -> Dict:
    """
    Parse HTML from a file.
    
    Args:
        file_path: Path to HTML file
        
    Returns:
        Parsed content dictionary
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    parser = StudyBibleParser(html_content)
    return parser.parse_all()
