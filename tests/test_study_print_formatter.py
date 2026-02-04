"""
Tests for the Study Bible Print Formatter.

This module tests the StudyBiblePrintFormatter class for generating
print-ready HTML output from Bible study data.
"""

import pytest
import json
from pathlib import Path
from src.formatters.study_print_formatter import StudyBiblePrintFormatter


class TestStudyBiblePrintFormatter:
    """Tests for StudyBiblePrintFormatter class."""
    
    def test_formatter_instantiation(self):
        """Test that formatter can be instantiated without errors."""
        formatter = StudyBiblePrintFormatter()
        assert formatter is not None
        assert formatter.page_width == 210
        assert formatter.page_height == 297
    
    def test_formatter_custom_dimensions(self):
        """Test formatter with custom page dimensions."""
        formatter = StudyBiblePrintFormatter(page_width=215, page_height=279)
        assert formatter.page_width == 215
        assert formatter.page_height == 279
    
    def test_generate_html_minimal_data(self):
        """Test HTML generation with minimal data."""
        formatter = StudyBiblePrintFormatter()
        data = {
            'book': 'Test',
            'chapter': 1,
            'verses': []
        }
        html = formatter.generate_html(data)
        
        assert isinstance(html, str)
        assert len(html) > 0
        assert '<html' in html
        assert 'Test 1' in html
        assert 'DOCTYPE' in html
    
    def test_generate_html_missing_book(self):
        """Test that ValueError is raised when book is missing."""
        formatter = StudyBiblePrintFormatter()
        data = {
            'chapter': 1,
            'verses': []
        }
        
        with pytest.raises(ValueError, match="book"):
            formatter.generate_html(data)
    
    def test_generate_html_missing_chapter(self):
        """Test that ValueError is raised when chapter is missing."""
        formatter = StudyBiblePrintFormatter()
        data = {
            'book': 'Test',
            'verses': []
        }
        
        with pytest.raises(ValueError, match="chapter"):
            formatter.generate_html(data)
    
    def test_generate_html_invalid_verses(self):
        """Test that ValueError is raised when verses is not a list."""
        formatter = StudyBiblePrintFormatter()
        data = {
            'book': 'Test',
            'chapter': 1,
            'verses': 'not a list'
        }
        
        with pytest.raises(ValueError, match="verses"):
            formatter.generate_html(data)
    
    def test_generate_html_with_verses(self):
        """Test HTML generation with verse data."""
        formatter = StudyBiblePrintFormatter()
        data = {
            'book': 'Genesis',
            'chapter': 1,
            'verses': [
                {'number': 1, 'text': 'In the beginning God created the heavens and the earth.'},
                {'number': 2, 'text': 'Now the earth was formless and desolate.'}
            ]
        }
        html = formatter.generate_html(data)
        
        assert 'Genesis 1' in html
        assert 'class="verse"' in html
        assert 'class="verse-num"' in html
        assert 'In the beginning' in html
        assert 'formless and desolate' in html
    
    def test_generate_html_with_superscription(self):
        """Test HTML generation with superscription."""
        formatter = StudyBiblePrintFormatter()
        data = {
            'book': 'Psalms',
            'chapter': 83,
            'superscription': 'A song. A melody of Asaph.',
            'verses': [
                {'number': 1, 'text': 'O God, do not be silent.'}
            ]
        }
        html = formatter.generate_html(data)
        
        assert 'class="superscription"' in html
        assert 'A song. A melody of Asaph.' in html
    
    def test_format_verses_with_empty_list(self):
        """Test verse formatting with empty list."""
        formatter = StudyBiblePrintFormatter()
        html = formatter._format_verses([], '')
        assert html == ''
    
    def test_format_verses_with_data(self):
        """Test verse formatting with actual verse data."""
        formatter = StudyBiblePrintFormatter()
        verses = [
            {'number': 1, 'text': 'Test verse 1'},
            {'number': 2, 'text': 'Test verse 2'}
        ]
        html = formatter._format_verses(verses, '')
        
        assert 'class="verse"' in html
        assert 'class="verse-num"' in html
        assert 'Test verse 1' in html
        assert 'Test verse 2' in html
    
    def test_build_css(self):
        """Test CSS generation."""
        formatter = StudyBiblePrintFormatter()
        css = formatter._build_css()
        
        assert isinstance(css, str)
        assert '@page' in css
        assert 'A4' in css
        assert 'grid-template-columns' in css
        assert '60%' in css
        assert '40%' in css
        assert '@media print' in css
    
    def test_format_study_panel_empty(self):
        """Test study panel formatting with no study materials."""
        formatter = StudyBiblePrintFormatter()
        data = {
            'book': 'Test',
            'chapter': 1,
            'verses': [],
            'study_notes': [],
            'footnotes': [],
            'cross_references': []
        }
        html = formatter._format_study_panel(data)
        
        assert isinstance(html, str)
        assert 'No study materials' in html
    
    def test_format_study_panel_with_notes(self):
        """Test study panel formatting with study notes."""
        formatter = StudyBiblePrintFormatter()
        data = {
            'book': 'Psalms',
            'chapter': 83,
            'verses': [],
            'study_notes': [
                {
                    'reference': '83:3',
                    'content': 'Test study note'
                }
            ],
            'footnotes': [],
            'cross_references': []
        }
        html = formatter._format_study_panel(data)
        
        assert 'class="verse-heading"' in html
        assert 'Psalms 83:3' in html
        assert 'Test study note' in html
    
    @pytest.mark.unit
    def test_psalms_83_sample_data(self, psalms_83_sample):
        """Test HTML generation with Psalms 83 sample data."""
        formatter = StudyBiblePrintFormatter()
        html = formatter.generate_html(psalms_83_sample)
        
        # Validate structure
        assert '<html' in html
        assert 'Psalms 83' in html
        
        # Check for verses
        assert 'class="verse"' in html
        assert 'O God, do not be silent' in html
        
        # Check for superscription
        assert 'class="superscription"' in html
        assert 'Asaph' in html
        
        # Check for study materials
        assert 'class="study-column"' in html
        
        # Check that we have all 18 verses
        verse_count = html.count('class="verse"')
        assert verse_count == 18, f"Expected 18 verses, found {verse_count}"
    
    @pytest.mark.unit
    def test_html_structure_validity(self):
        """Test that generated HTML has proper structure."""
        formatter = StudyBiblePrintFormatter()
        data = {
            'book': 'Test',
            'chapter': 1,
            'verses': [{'number': 1, 'text': 'Test'}]
        }
        html = formatter.generate_html(data)
        
        # Check essential HTML elements
        assert '<!DOCTYPE html>' in html
        assert '<html lang="en">' in html
        assert '<head>' in html
        assert '<meta charset="UTF-8">' in html
        assert '<title>' in html
        assert '<style>' in html
        assert '<body>' in html
        assert '<header class="page-header">' in html
        assert '<div class="content-grid">' in html
        assert '<div class="verses-column">' in html
        assert '<div class="study-column">' in html
        assert '<footer class="page-footer">' in html
        assert '</body>' in html
        assert '</html>' in html
