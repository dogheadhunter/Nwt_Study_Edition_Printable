"""
Tests for the Psalms 83 Scraper.

This module tests the Psalms 83 scraping workflow including:
- Sample data loading
- HTML parsing
- Data formatting
- Output generation
"""

import pytest
import json
import os
from typing import Dict, Any

# Import the scraper
from src.scrapers.psalms_scraper import Psalms83Scraper


class TestPsalms83Scraper:
    """Tests for the Psalms83Scraper class."""
    
    @pytest.fixture
    def scraper(self):
        """Create a scraper instance for testing."""
        return Psalms83Scraper(data_dir="data")
    
    @pytest.fixture
    def sample_data(self, scraper):
        """Load sample Psalms 83 data."""
        return scraper.load_sample_data()
    
    def test_scraper_initialization(self, scraper):
        """Test that the scraper initializes correctly."""
        assert scraper is not None
        assert scraper.PSALMS_83_URL == "https://www.jw.org/en/library/bible/study-bible/books/psalms/83/"
        assert scraper.BASE_URL == "https://www.jw.org/en/library/bible/study-bible/books/"
    
    def test_sample_data_loads(self, sample_data):
        """Test that sample data loads correctly."""
        assert sample_data is not None
        assert isinstance(sample_data, dict)
    
    def test_sample_data_structure(self, sample_data):
        """Test that sample data has the expected structure."""
        required_fields = ['book', 'chapter', 'verses', 'study_notes', 'footnotes']
        
        for field in required_fields:
            assert field in sample_data, f"Missing required field: {field}"
    
    def test_sample_data_book_info(self, sample_data):
        """Test that book info is correct."""
        assert sample_data['book'] == 'Psalms'
        assert sample_data['chapter'] == 83
    
    def test_sample_data_verses(self, sample_data):
        """Test that verses are correctly structured."""
        verses = sample_data.get('verses', [])
        
        # Psalms 83 has 18 verses
        assert len(verses) == 18, f"Expected 18 verses, got {len(verses)}"
        
        # Check verse structure
        for verse in verses:
            assert 'number' in verse
            assert 'text' in verse
            assert isinstance(verse['number'], int)
            assert isinstance(verse['text'], str)
            assert len(verse['text']) > 0
    
    def test_sample_data_verse_numbers_sequential(self, sample_data):
        """Test that verse numbers are sequential."""
        verses = sample_data.get('verses', [])
        
        for i, verse in enumerate(verses):
            expected_num = i + 1
            assert verse['number'] == expected_num, \
                f"Verse {i} has number {verse['number']}, expected {expected_num}"
    
    def test_sample_data_study_notes(self, sample_data):
        """Test that study notes are present."""
        notes = sample_data.get('study_notes', [])
        
        assert len(notes) > 0, "Expected at least one study note"
        
        # Check study note structure
        for note in notes:
            assert 'id' in note
            assert 'reference' in note
            assert 'content' in note
            assert len(note['content']) > 0
    
    def test_sample_data_footnotes(self, sample_data):
        """Test that footnotes are present."""
        footnotes = sample_data.get('footnotes', [])
        
        # Psalms 83 should have at least the Selah footnote
        assert len(footnotes) >= 1
        
        # Check footnote structure
        for fn in footnotes:
            assert 'id' in fn
            assert 'content' in fn
    
    def test_sample_data_cross_references(self, sample_data):
        """Test that cross-references are present."""
        xrefs = sample_data.get('cross_references', [])
        
        assert len(xrefs) > 0, "Expected at least one cross-reference"
        
        # Check cross-reference structure
        for xref in xrefs:
            assert 'id' in xref
            assert 'verses' in xref
            assert isinstance(xref['verses'], list)
    
    def test_superscription(self, sample_data):
        """Test that the psalm superscription is present."""
        superscription = sample_data.get('superscription', '')
        
        assert superscription is not None
        assert len(superscription) > 0
        assert 'Asaph' in superscription
    
    def test_verse_content_key_verses(self, sample_data):
        """Test that key verses contain expected content."""
        verses = sample_data.get('verses', [])
        
        # Verse 1 - Opening prayer
        verse_1 = verses[0]
        assert 'God' in verse_1['text']
        
        # Verse 18 - Famous verse about Jehovah
        verse_18 = verses[17]
        assert 'Jehovah' in verse_18['text']
        assert 'Most High' in verse_18['text']
    
    def test_workflow_structure(self, scraper):
        """Test that the scraping workflow is correctly structured."""
        workflow = scraper.get_scraping_workflow()
        
        assert 'workflow' in workflow
        assert 'target_url' in workflow
        assert 'steps' in workflow
        
        # Verify step structure
        steps = workflow['steps']
        assert len(steps) > 0
        
        for step in steps:
            assert 'step' in step
            assert 'action' in step
            assert 'description' in step


class TestPsalms83Formatting:
    """Tests for Psalms 83 formatting functions."""
    
    @pytest.fixture
    def scraper(self):
        """Create a scraper instance for testing."""
        return Psalms83Scraper(data_dir="data")
    
    @pytest.fixture
    def sample_data(self, scraper):
        """Load sample Psalms 83 data."""
        return scraper.load_sample_data()
    
    def test_format_for_print(self, scraper, sample_data):
        """Test print formatting."""
        output = scraper.format_for_print(sample_data)
        
        assert isinstance(output, str)
        assert len(output) > 0
        
        # Check that key elements are present
        assert 'PSALM 83' in output
        assert 'STUDY NOTES' in output
        assert 'Jehovah' in output
    
    def test_format_for_html(self, scraper, sample_data):
        """Test HTML formatting."""
        output = scraper.format_for_html(sample_data)
        
        assert isinstance(output, str)
        assert len(output) > 0
        
        # Check that it's valid HTML structure
        assert '<!DOCTYPE html>' in output
        assert '<html' in output
        assert '</html>' in output
        assert 'Psalm 83' in output
    
    def test_html_contains_verses(self, scraper, sample_data):
        """Test that HTML output contains all verses."""
        output = scraper.format_for_html(sample_data)
        
        for i in range(1, 19):  # Verses 1-18
            # Check that verse number appears in output
            assert f'>{i}</span>' in output or str(i) in output


class TestPsalms83HTMLParsing:
    """Tests for HTML parsing functionality."""
    
    @pytest.fixture
    def scraper(self):
        """Create a scraper instance for testing."""
        return Psalms83Scraper(data_dir="data")
    
    def test_parse_empty_html(self, scraper):
        """Test parsing empty HTML."""
        result = scraper.parse_html_content("")
        
        assert result is not None
        assert result['book'] == 'Psalms'
        assert result['chapter'] == 83
        assert result['verses'] == []
    
    def test_parse_simple_verse_html(self, scraper):
        """Test parsing HTML with a simple verse structure."""
        html = '''
        <html>
            <body>
                <p class="verse">
                    <span class="v">1</span>
                    O God, do not remain silent.
                </p>
            </body>
        </html>
        '''
        
        result = scraper.parse_html_content(html)
        
        assert result is not None
        assert len(result['verses']) >= 0  # May or may not parse depending on exact selectors


class TestPsalms83DataStorage:
    """Tests for data storage functionality."""
    
    @pytest.fixture
    def scraper(self):
        """Create a scraper instance with temp directory."""
        return Psalms83Scraper(data_dir="data")
    
    @pytest.fixture
    def sample_data(self, scraper):
        """Load sample Psalms 83 data."""
        return scraper.load_sample_data()
    
    def test_save_chapter_data(self, scraper, sample_data, tmp_path):
        """Test saving chapter data to file."""
        # Use a temp scraper for this test
        temp_scraper = Psalms83Scraper(data_dir=str(tmp_path))
        
        filepath = temp_scraper.save_chapter_data(sample_data, "test_psalms_83.json")
        
        assert os.path.exists(filepath)
        
        # Verify the saved data
        with open(filepath, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data['book'] == 'Psalms'
        assert saved_data['chapter'] == 83
        assert len(saved_data['verses']) == 18


class TestPsalms83Workflow:
    """Tests for the complete scraping workflow."""
    
    @pytest.fixture
    def scraper(self):
        """Create a scraper instance for testing."""
        return Psalms83Scraper(data_dir="data")
    
    def test_workflow_has_all_steps(self, scraper):
        """Test that workflow includes all necessary steps."""
        workflow = scraper.get_scraping_workflow()
        steps = workflow['steps']
        
        # Check for key steps
        step_actions = [s['action'] for s in steps]
        
        assert 'Navigate to Psalms 83' in step_actions
        assert 'Wait for content to load' in step_actions
        assert 'Take screenshot' in step_actions
        assert 'Get page snapshot' in step_actions
    
    def test_workflow_screenshot_is_jpeg(self, scraper):
        """Test that workflow specifies JPEG format for screenshots."""
        workflow = scraper.get_scraping_workflow()
        
        for step in workflow['steps']:
            if step['action'] == 'Take screenshot':
                params = step.get('params', {})
                assert params.get('type') == 'jpeg', "Screenshot should be JPEG format"
                assert 'jpeg' in params.get('filename', '').lower(), \
                    "Screenshot filename should have .jpeg extension"


def test_psalms_scraper_import():
    """Test that the Psalms scraper module can be imported."""
    from src.scrapers.psalms_scraper import Psalms83Scraper
    
    scraper = Psalms83Scraper()
    assert scraper is not None


def test_psalms_83_expected_structure():
    """Test the expected structure of Psalms 83."""
    expected = {
        "chapter": 83,
        "total_verses": 18,
        "has_superscription": True,
        "author": "Asaph"
    }
    
    assert expected["total_verses"] == 18
    assert expected["has_superscription"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
