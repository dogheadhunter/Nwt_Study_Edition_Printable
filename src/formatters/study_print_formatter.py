"""
Study Bible Print Formatter

This module provides a formatter for creating print-ready HTML output
of Bible study content with a two-column layout (60% verses, 40% study materials).
"""

from typing import Dict, Any, List, Optional


class StudyBiblePrintFormatter:
    """
    Formats Bible study data into printable HTML with two-column layout.
    
    This formatter creates an A4-sized HTML document with verses on the left
    (60% width) and study materials (footnotes, cross-references, study notes)
    on the right (40% width), matching the JW.org Study Bible website layout.
    
    Attributes:
        page_width: Width of the page in millimeters (default: 210mm for A4)
        page_height: Height of the page in millimeters (default: 297mm for A4)
    
    Example:
        >>> formatter = StudyBiblePrintFormatter()
        >>> data = load_json("data/samples/psalms_83_sample.json")
        >>> html = formatter.generate_html(data)
        >>> with open("output.html", "w") as f:
        ...     f.write(html)
    """
    
    def __init__(self, page_width: int = 210, page_height: int = 297):
        """
        Initialize the formatter with page dimensions.
        
        Args:
            page_width: Width of the page in millimeters (default: 210mm for A4)
            page_height: Height of the page in millimeters (default: 297mm for A4)
        """
        self.page_width = page_width
        self.page_height = page_height
    
    def generate_html(self, data: Dict[str, Any]) -> str:
        """
        Generate complete HTML document from Bible chapter data.
        
        Args:
            data: Dictionary containing Bible chapter data with keys:
                - book (str): Book name (e.g., "Psalms")
                - chapter (int): Chapter number
                - verses (List[Dict]): List of verse objects
                - study_notes (List[Dict]): List of study note objects
                - footnotes (List[Dict]): List of footnote objects
                - cross_references (List[Dict]): List of cross-reference objects
                - superscription (str, optional): Chapter superscription text
        
        Returns:
            Complete HTML document as a string with embedded CSS
            
        Raises:
            ValueError: If required data fields are missing
            
        Example:
            >>> formatter = StudyBiblePrintFormatter()
            >>> data = {"book": "Psalms", "chapter": 83, "verses": [...]}
            >>> html = formatter.generate_html(data)
            >>> assert "<html" in html
            >>> assert "Psalms 83" in html
        """
        # Validate required fields
        if not data.get('book') or not data.get('chapter'):
            raise ValueError("Data must include 'book' and 'chapter' fields")
        
        if not isinstance(data.get('verses', []), list):
            raise ValueError("Data must include 'verses' as a list")
        
        book = data['book']
        chapter = data['chapter']
        verses = data.get('verses', [])
        superscription = data.get('superscription', '')
        
        # Build HTML sections
        css = self._build_css()
        verses_html = self._format_verses(verses, superscription)
        study_panel_html = self._format_study_panel(data)
        
        # Assemble complete HTML document
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book} {chapter} - NWT Study Bible</title>
    <style>
{css}
    </style>
</head>
<body>
    <header class="page-header">
        <h1>{book} {chapter}</h1>
    </header>
    
    <div class="content-grid">
        <div class="verses-column">
{verses_html}
        </div>
        
        <div class="study-column">
{study_panel_html}
        </div>
    </div>
    
    <footer class="page-footer">
        <p>{book} {chapter} - New World Translation Study Edition</p>
    </footer>
</body>
</html>"""
        
        return html
    
    def _build_css(self) -> str:
        """
        Build CSS styles for the print layout.
        
        Returns:
            CSS stylesheet as a string with A4 page rules, grid layout,
            and print-specific styling
            
        Note:
            - Page size: A4 (210mm × 297mm)
            - Margins: 20mm top/bottom, 15mm left/right
            - Grid: 60% left column, 40% right column with 10mm gap
            - Headers/footers on every page
        """
        return """
/* Page setup for A4 printing */
@page {
    size: A4;
    margin: 20mm 15mm;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

/* Page header */
.page-header {
    text-align: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #333;
}

.page-header h1 {
    font-size: 18pt;
    font-weight: bold;
}

/* Two-column grid layout: 60% verses, 40% study materials */
.content-grid {
    display: grid;
    grid-template-columns: 60% 40%;
    gap: 10mm;
    min-height: 200mm;
}

/* Left column: Verses */
.verses-column {
    padding-right: 5mm;
}

/* Right column: Study materials */
.study-column {
    padding-left: 5mm;
    background-color: #f5f5f5;
    padding: 10px;
    border-left: 1px solid #ccc;
}

/* Verse formatting */
.verse {
    margin-bottom: 0.5em;
    page-break-inside: avoid;
}

.verse-num {
    font-weight: bold;
    margin-right: 0.3em;
}

.superscription {
    font-style: italic;
    margin-bottom: 1em;
    color: #555;
}

/* Superscript markers for cross-refs and footnotes */
sup {
    font-size: 0.8em;
    font-weight: bold;
}

/* Study materials formatting */
.verse-heading {
    font-weight: bold;
    margin-top: 1em;
    margin-bottom: 0.5em;
    color: #222;
}

.verse-heading:first-child {
    margin-top: 0;
}

.study-item {
    margin-bottom: 1em;
    padding-left: 1em;
}

.footnote-marker,
.crossref-marker {
    font-weight: bold;
    margin-right: 0.3em;
}

.study-note-content,
.footnote-content,
.crossref-content {
    color: #444;
}

.crossref-citation {
    font-weight: bold;
    color: #000;
}

.crossref-verse {
    margin-left: 1em;
    color: #555;
}

/* Page footer */
.page-footer {
    margin-top: 20px;
    padding-top: 10px;
    border-top: 1px solid #ccc;
    text-align: center;
    font-size: 9pt;
    color: #666;
}

/* Print-specific rules */
@media print {
    body {
        background: white;
    }
    
    .page-header,
    .page-footer {
        position: fixed;
    }
    
    .page-header {
        top: 0;
    }
    
    .page-footer {
        bottom: 0;
    }
    
    /* Ensure columns don't break awkwardly */
    .verse,
    .study-item {
        page-break-inside: avoid;
    }
}
"""
    
    def _format_verses(self, verses: List[Dict[str, Any]], superscription: str = "") -> str:
        """
        Format the verses for the left column.
        
        Args:
            verses: List of verse dictionaries with 'number' and 'text' keys
            superscription: Optional superscription text to display before verses
            
        Returns:
            HTML string containing formatted verses
            
        Note:
            - Verse numbers are bold and inline
            - Cross-reference markers (a, b, c) appear as superscript
            - Footnote markers (*, †) appear as superscript
            - Superscription appears in italics above verses
        """
        html_parts = []
        
        # Add superscription if present
        if superscription:
            html_parts.append(f'            <p class="superscription">{superscription}</p>')
        
        # Format each verse
        for verse in verses:
            verse_num = verse.get('number', '')
            verse_text = verse.get('text', '')
            
            # Add cross-reference markers if present
            cross_refs = verse.get('cross_references', [])
            markers = []
            for i, _ in enumerate(cross_refs):
                marker = chr(97 + i)  # a, b, c, etc.
                markers.append(f'<sup>{marker}</sup>')
            
            # Add footnote markers if present
            footnotes = verse.get('footnotes', [])
            if footnotes:
                markers.append('<sup>*</sup>')
            
            markers_html = ''.join(markers)
            
            html_parts.append(
                f'            <p class="verse">'
                f'<span class="verse-num">{verse_num}</span>{verse_text}{markers_html}'
                f'</p>'
            )
        
        return '\n'.join(html_parts)
    
    def _format_study_panel(self, data: Dict[str, Any]) -> str:
        """
        Format the study materials for the right column.
        
        Args:
            data: Complete chapter data including study notes, footnotes,
                  and cross-references
        
        Returns:
            HTML string containing formatted study materials organized by verse
            
        Note:
            - Creates verse heading sections (e.g., "Psalm 83:1")
            - Groups all study materials by verse number
            - Includes footnotes, cross-references, and study notes
            - Shows blank space for verses without study materials
        """
        html_parts = []
        verses = data.get('verses', [])
        study_notes = data.get('study_notes', [])
        footnotes = data.get('footnotes', [])
        cross_references = data.get('cross_references', [])
        book = data.get('book', '')
        chapter = data.get('chapter', '')
        
        # Create a mapping of verse numbers to study materials
        verse_materials = {}
        
        # Group study notes by verse
        for note in study_notes:
            ref = note.get('reference', '')
            # Parse reference like "83:3" to get verse number
            if ':' in ref:
                verse_num = ref.split(':')[1]
                if verse_num not in verse_materials:
                    verse_materials[verse_num] = {'notes': [], 'footnotes': [], 'cross_refs': []}
                verse_materials[verse_num]['notes'].append(note)
        
        # Group footnotes by verse
        for footnote in footnotes:
            ref = footnote.get('reference', '')
            if ':' in ref:
                verse_num = ref.split(':')[1]
                if verse_num not in verse_materials:
                    verse_materials[verse_num] = {'notes': [], 'footnotes': [], 'cross_refs': []}
                verse_materials[verse_num]['footnotes'].append(footnote)
        
        # Group cross-references by verse
        for cross_ref in cross_references:
            ref = cross_ref.get('reference', '')
            # Handle ranges like "83:6-8"
            if ':' in ref:
                verse_part = ref.split(':')[1]
                # For now, use the first verse in a range
                verse_num = verse_part.split('-')[0]
                if verse_num not in verse_materials:
                    verse_materials[verse_num] = {'notes': [], 'footnotes': [], 'cross_refs': []}
                verse_materials[verse_num]['cross_refs'].append(cross_ref)
        
        # Generate HTML for each verse with study materials
        for verse_num_str in sorted(verse_materials.keys(), key=lambda x: int(x) if x.isdigit() else 0):
            materials = verse_materials[verse_num_str]
            
            # Add verse heading
            html_parts.append(f'            <div class="verse-heading">{book} {chapter}:{verse_num_str}</div>')
            
            # Add footnotes
            for footnote in materials['footnotes']:
                content = footnote.get('content', '')
                html_parts.append(
                    f'            <div class="study-item">'
                    f'<span class="footnote-marker">*</span>'
                    f'<span class="footnote-content">{content}</span>'
                    f'</div>'
                )
            
            # Add cross-references
            for cross_ref in materials['cross_refs']:
                verses_list = cross_ref.get('verses', [])
                if verses_list:
                    html_parts.append(f'            <div class="study-item">')
                    for verse_citation in verses_list:
                        html_parts.append(
                            f'                <div class="crossref-content">'
                            f'<span class="crossref-citation">{verse_citation}</span>'
                            f'</div>'
                        )
                    html_parts.append(f'            </div>')
            
            # Add study notes
            for note in materials['notes']:
                content = note.get('content', '')
                html_parts.append(
                    f'            <div class="study-item">'
                    f'<span class="study-note-content">{content}</span>'
                    f'</div>'
                )
        
        return '\n'.join(html_parts) if html_parts else '            <p>No study materials for this chapter.</p>'
