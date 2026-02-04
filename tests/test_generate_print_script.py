"""
Tests for the generate_print.py CLI script.

This module tests the CLI script functionality including batch processing.
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the functions we want to test
from scripts.generate_print import discover_chapters, generate_chapter, load_chapter_data


class TestDiscoverChapters:
    """Tests for chapter discovery functionality."""
    
    def test_discover_chapters_from_samples(self, tmp_path, monkeypatch):
        """Test discovering chapters from samples directory."""
        # Create mock samples directory
        samples_dir = tmp_path / "data" / "samples"
        samples_dir.mkdir(parents=True)
        
        # Create sample files
        (samples_dir / "psalms_1_sample.json").touch()
        (samples_dir / "psalms_83_sample.json").touch()
        (samples_dir / "psalms_150_sample.json").touch()
        (samples_dir / "genesis_1_sample.json").touch()  # Different book
        
        # Mock the base directory
        with patch('scripts.generate_print.Path') as mock_path:
            mock_path.return_value.parent.parent = tmp_path
            
            # Import after mocking
            import importlib
            import scripts.generate_print
            importlib.reload(scripts.generate_print)
            
            chapters = scripts.generate_print.discover_chapters("Psalms")
        
        # Should find 3 Psalms chapters
        assert len(chapters) == 3
        assert 1 in chapters
        assert 83 in chapters
        assert 150 in chapters
    
    def test_discover_chapters_from_processed(self, tmp_path, monkeypatch):
        """Test discovering chapters from processed directory."""
        # Create mock processed directory
        processed_dir = tmp_path / "data" / "processed" / "Genesis"
        processed_dir.mkdir(parents=True)
        
        # Create chapter files
        (processed_dir / "chapter_1.json").touch()
        (processed_dir / "chapter_2.json").touch()
        (processed_dir / "chapter_50.json").touch()
        
        # Mock the base directory
        with patch('scripts.generate_print.Path') as mock_path:
            mock_path.return_value.parent.parent = tmp_path
            
            import importlib
            import scripts.generate_print
            importlib.reload(scripts.generate_print)
            
            chapters = scripts.generate_print.discover_chapters("Genesis")
        
        assert len(chapters) == 3
        assert 1 in chapters
        assert 2 in chapters
        assert 50 in chapters
    
    def test_discover_chapters_empty(self, tmp_path):
        """Test discovering chapters when no files exist."""
        with patch('scripts.generate_print.Path') as mock_path:
            mock_path.return_value.parent.parent = tmp_path
            
            import importlib
            import scripts.generate_print
            importlib.reload(scripts.generate_print)
            
            chapters = scripts.generate_print.discover_chapters("NonExistent")
        
        assert len(chapters) == 0


class TestGenerateChapter:
    """Tests for chapter generation functionality."""
    
    def test_generate_chapter_success(self, tmp_path, psalms_83_sample):
        """Test successful chapter generation."""
        # Save sample data to temp file
        data_dir = tmp_path / "data" / "samples"
        data_dir.mkdir(parents=True)
        sample_file = data_dir / "psalms_83_sample.json"
        
        with open(sample_file, 'w') as f:
            json.dump(psalms_83_sample, f)
        
        # Mock load_chapter_data to use our temp file
        with patch('scripts.generate_print.load_chapter_data') as mock_load:
            mock_load.return_value = psalms_83_sample
            
            from scripts.generate_print import generate_chapter
            from src.formatters.study_print_formatter import StudyBiblePrintFormatter
            
            formatter = StudyBiblePrintFormatter()
            output_dir = tmp_path / "output"
            
            result = generate_chapter(
                "Psalms",
                83,
                "html",
                output_dir,
                formatter
            )
        
        assert result['success'] is True
        assert result['book'] == "Psalms"
        assert result['chapter'] == 83
        assert len(result['files']) == 1
        assert 'chapter_83.html' in result['files'][0]
    
    def test_generate_chapter_missing_data(self, tmp_path):
        """Test chapter generation with missing data."""
        from scripts.generate_print import generate_chapter
        from src.formatters.study_print_formatter import StudyBiblePrintFormatter
        
        formatter = StudyBiblePrintFormatter()
        output_dir = tmp_path / "output"
        
        result = generate_chapter(
            "NonExistent",
            999,
            "pdf",
            output_dir,
            formatter
        )
        
        assert result['success'] is False
        assert result['error'] is not None
        assert 'Chapter data not found' in result['error']


class TestLoadChapterData:
    """Tests for chapter data loading."""
    
    def test_load_chapter_data_from_samples(self, tmp_path, psalms_83_sample):
        """Test loading chapter data from samples directory."""
        # Create samples directory and file
        samples_dir = tmp_path / "data" / "samples"
        samples_dir.mkdir(parents=True)
        sample_file = samples_dir / "psalms_83_sample.json"
        
        with open(sample_file, 'w') as f:
            json.dump(psalms_83_sample, f)
        
        # Mock the base directory
        with patch('scripts.generate_print.Path') as mock_path:
            # Make __file__.parent.parent return tmp_path
            mock_file = MagicMock()
            mock_file.parent.parent = tmp_path
            mock_path.return_value = mock_file
            
            import importlib
            import scripts.generate_print
            importlib.reload(scripts.generate_print)
            
            data = scripts.generate_print.load_chapter_data("Psalms", 83)
        
        assert data['book'] == "Psalms"
        assert data['chapter'] == 83
    
    def test_load_chapter_data_not_found(self, tmp_path):
        """Test loading non-existent chapter data."""
        with patch('scripts.generate_print.Path') as mock_path:
            mock_file = MagicMock()
            mock_file.parent.parent = tmp_path
            mock_path.return_value = mock_file
            
            import importlib
            import scripts.generate_print
            importlib.reload(scripts.generate_print)
            
            with pytest.raises(FileNotFoundError):
                scripts.generate_print.load_chapter_data("NonExistent", 999)


@pytest.mark.integration
class TestBatchProcessingIntegration:
    """Integration tests for batch processing."""
    
    def test_batch_processing_workflow(self, tmp_path):
        """Test complete batch processing workflow."""
        # Create test data files
        processed_dir = tmp_path / "data" / "processed" / "TestBook"
        processed_dir.mkdir(parents=True)
        
        for chapter in [1, 2, 3]:
            chapter_data = {
                "book": "TestBook",
                "chapter": chapter,
                "verses": [{"number": 1, "text": f"Chapter {chapter} verse 1"}],
                "study_notes": [],
                "footnotes": [],
                "cross_references": []
            }
            
            with open(processed_dir / f"chapter_{chapter}.json", 'w') as f:
                json.dump(chapter_data, f)
        
        # Mock the base directory
        with patch('scripts.generate_print.Path') as mock_path:
            mock_file = MagicMock()
            mock_file.parent.parent = tmp_path
            mock_path.return_value = mock_file
            mock_path.side_effect = lambda x: Path(x)  # For other Path calls
            
            import importlib
            import scripts.generate_print
            importlib.reload(scripts.generate_print)
            
            # Discover chapters
            chapters = scripts.generate_print.discover_chapters("TestBook")
        
        assert len(chapters) == 3
        assert set(chapters) == {1, 2, 3}
