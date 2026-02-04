"""
Data validators for Bible scraper.

This module provides validation functions for checking the structure
and completeness of scraped Bible content.
"""

from typing import Dict, List, Any, Optional


def validate_verse_structure(verse: Dict[str, Any]) -> bool:
    """
    Validate that a verse has the expected structure.
    
    Args:
        verse: Dictionary containing verse data
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['number', 'text']
    
    # Check required fields exist
    for field in required_fields:
        if field not in verse:
            return False
    
    # Validate field types
    if not isinstance(verse['number'], int):
        return False
    
    if not isinstance(verse['text'], str):
        return False
    
    # Verse text should not be empty
    if len(verse['text'].strip()) == 0:
        return False
    
    # Optional fields should be lists if present
    if 'footnotes' in verse and not isinstance(verse['footnotes'], list):
        return False
    
    if 'cross_references' in verse and not isinstance(verse['cross_references'], list):
        return False
    
    return True


def validate_study_note(note: Dict[str, Any]) -> bool:
    """
    Validate that a study note has the expected structure.
    
    Args:
        note: Dictionary containing study note data
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['id', 'reference', 'content']
    
    # Check required fields exist
    for field in required_fields:
        if field not in note:
            return False
        if not isinstance(note[field], str):
            return False
    
    # Content should not be empty
    if len(note['content'].strip()) == 0:
        return False
    
    return True


def validate_footnote(footnote: Dict[str, Any]) -> bool:
    """
    Validate that a footnote has the expected structure.
    
    Args:
        footnote: Dictionary containing footnote data
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['id', 'content']
    
    for field in required_fields:
        if field not in footnote:
            return False
        if not isinstance(footnote[field], str):
            return False
    
    if len(footnote['content'].strip()) == 0:
        return False
    
    return True


def validate_cross_reference(xref: Dict[str, Any]) -> bool:
    """
    Validate that a cross-reference has the expected structure.
    
    Args:
        xref: Dictionary containing cross-reference data
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['id', 'verses']
    
    if 'id' not in xref or not isinstance(xref['id'], str):
        return False
    
    if 'verses' not in xref or not isinstance(xref['verses'], list):
        return False
    
    # Verses list should not be empty
    if len(xref['verses']) == 0:
        return False
    
    # All verse references should be strings
    for verse_ref in xref['verses']:
        if not isinstance(verse_ref, str):
            return False
    
    return True


def validate_chapter_completeness(
    data: Dict[str, Any], 
    expected_verses: int
) -> List[str]:
    """
    Validate that a chapter has all expected components.
    
    Args:
        data: Complete chapter data dictionary
        expected_verses: Expected number of verses
        
    Returns:
        List of validation error messages (empty if all valid)
    """
    errors = []
    
    # Check required top-level fields
    required_fields = ['book', 'chapter', 'verses']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate book name
    if 'book' in data and not isinstance(data['book'], str):
        errors.append("Book name should be a string")
    
    # Validate chapter number
    if 'chapter' in data and not isinstance(data['chapter'], int):
        errors.append("Chapter number should be an integer")
    
    # Validate verses
    if 'verses' in data:
        if not isinstance(data['verses'], list):
            errors.append("Verses should be a list")
        else:
            # Check verse count
            actual_count = len(data['verses'])
            if actual_count != expected_verses:
                errors.append(
                    f"Expected {expected_verses} verses, found {actual_count}"
                )
            
            # Validate each verse
            for i, verse in enumerate(data['verses']):
                if not validate_verse_structure(verse):
                    errors.append(f"Invalid verse structure at index {i}")
                
                # Check verse numbering is sequential
                expected_num = i + 1
                if verse.get('number') != expected_num:
                    errors.append(
                        f"Verse at index {i} has number {verse.get('number')}, "
                        f"expected {expected_num}"
                    )
    
    # Validate study notes if present
    if 'study_notes' in data:
        if not isinstance(data['study_notes'], list):
            errors.append("Study notes should be a list")
        else:
            for i, note in enumerate(data['study_notes']):
                if not validate_study_note(note):
                    errors.append(f"Invalid study note structure at index {i}")
    
    # Validate footnotes if present
    if 'footnotes' in data:
        if not isinstance(data['footnotes'], list):
            errors.append("Footnotes should be a list")
        else:
            for i, fn in enumerate(data['footnotes']):
                if not validate_footnote(fn):
                    errors.append(f"Invalid footnote structure at index {i}")
    
    # Validate cross-references if present
    if 'cross_references' in data:
        if not isinstance(data['cross_references'], list):
            errors.append("Cross-references should be a list")
        else:
            for i, xref in enumerate(data['cross_references']):
                if not validate_cross_reference(xref):
                    errors.append(f"Invalid cross-reference structure at index {i}")
    
    return errors


def validate_psalms_83_specific(data: Dict[str, Any]) -> List[str]:
    """
    Validate Psalms 83 specific requirements.
    
    Args:
        data: Psalms 83 chapter data
        
    Returns:
        List of validation error messages (empty if all valid)
    """
    errors = []
    
    # Should be Psalms 83
    if data.get('book') != 'Psalms':
        errors.append(f"Expected book 'Psalms', got '{data.get('book')}'")
    
    if data.get('chapter') != 83:
        errors.append(f"Expected chapter 83, got {data.get('chapter')}")
    
    # Should have 18 verses
    verses = data.get('verses', [])
    if len(verses) != 18:
        errors.append(f"Psalms 83 should have 18 verses, found {len(verses)}")
    
    # Should have superscription
    if 'superscription' in data:
        if not data['superscription']:
            errors.append("Psalms 83 should have a superscription")
        elif 'Asaph' not in data['superscription']:
            errors.append("Superscription should mention Asaph")
    
    # Verse 18 should contain key words
    if len(verses) >= 18:
        verse_18_text = verses[17].get('text', '')
        if 'Jehovah' not in verse_18_text:
            errors.append("Verse 18 should contain 'Jehovah'")
        if 'Most High' not in verse_18_text:
            errors.append("Verse 18 should contain 'Most High'")
    
    # Should have study notes
    study_notes = data.get('study_notes', [])
    if len(study_notes) < 3:
        errors.append(f"Expected at least 3 study notes, found {len(study_notes)}")
    
    # Should have Selah footnote
    footnotes = data.get('footnotes', [])
    has_selah = any('Selah' in fn.get('content', '') for fn in footnotes)
    if not has_selah:
        errors.append("Should have a Selah footnote")
    
    return errors


def is_valid_chapter_data(data: Dict[str, Any], expected_verses: int = None) -> bool:
    """
    Quick validation check for chapter data.
    
    Args:
        data: Chapter data to validate
        expected_verses: Expected verse count (optional)
        
    Returns:
        True if data appears valid, False otherwise
    """
    if not isinstance(data, dict):
        return False
    
    required_fields = ['book', 'chapter', 'verses']
    for field in required_fields:
        if field not in data:
            return False
    
    if not isinstance(data['verses'], list):
        return False
    
    if expected_verses is not None:
        if len(data['verses']) != expected_verses:
            return False
    
    # Check at least first verse is valid
    if len(data['verses']) > 0:
        if not validate_verse_structure(data['verses'][0]):
            return False
    
    return True
