#!/usr/bin/env python3
"""
Generate Cross-Reference Formatting Examples

This script creates three different HTML variations of cross-reference formatting
for Psalms 83, allowing users to choose their preferred style.

Variations:
- Example 1: Separate Paragraphs - Each verse in its own paragraph with citation header
- Example 2: Inline with Markers - All verses flow inline with bold citations
- Example 3: Indented Block Quote - Verses in block quote style with left border
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.formatters.study_print_formatter import StudyBiblePrintFormatter


class CrossRefExampleFormatter(StudyBiblePrintFormatter):
    """Extended formatter with cross-reference variation support."""
    
    def __init__(self, crossref_style='default'):
        """
        Initialize formatter with cross-reference style.
        
        Args:
            crossref_style: 'default', 'separate', 'inline', or 'blockquote'
        """
        super().__init__()
        self.crossref_style = crossref_style
    
    def _format_study_panel_with_style(self, data: dict) -> str:
        """Format study panel with specific cross-ref style."""
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
            if ':' in ref:
                verse_part = ref.split(':')[1]
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
            
            # Add cross-references with selected style
            for cross_ref in materials['cross_refs']:
                verses_list = cross_ref.get('verses', [])
                if verses_list:
                    if self.crossref_style == 'separate':
                        html_parts.append(self._format_crossref_separate(verses_list))
                    elif self.crossref_style == 'inline':
                        html_parts.append(self._format_crossref_inline(verses_list))
                    elif self.crossref_style == 'blockquote':
                        html_parts.append(self._format_crossref_blockquote(verses_list))
                    else:
                        # Default style (current implementation)
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
    
    def _format_crossref_separate(self, verses_list: list) -> str:
        """Format cross-references as separate paragraphs (Variation A)."""
        html_parts = ['            <div class="study-item crossref-separate">']
        
        for citation in verses_list:
            # Create sample verse text (in real implementation, would fetch actual text)
            verse_text = self._get_sample_verse_text(citation)
            html_parts.append(
                f'                <div class="crossref-paragraph">'
                f'<div class="crossref-citation-header">{citation}</div>'
                f'<div class="crossref-verse-text">{verse_text}</div>'
                f'</div>'
            )
        
        html_parts.append('            </div>')
        return '\n'.join(html_parts)
    
    def _format_crossref_inline(self, verses_list: list) -> str:
        """Format cross-references inline (Variation B)."""
        html_parts = ['            <div class="study-item crossref-inline">']
        
        inline_text = []
        for citation in verses_list:
            verse_text = self._get_sample_verse_text(citation)
            inline_text.append(f'<strong>{citation}:</strong> {verse_text}')
        
        html_parts.append(f'                <p>{" ".join(inline_text)}</p>')
        html_parts.append('            </div>')
        return '\n'.join(html_parts)
    
    def _format_crossref_blockquote(self, verses_list: list) -> str:
        """Format cross-references as block quotes (Variation C)."""
        html_parts = ['            <div class="study-item crossref-blockquote">']
        
        for citation in verses_list:
            verse_text = self._get_sample_verse_text(citation)
            html_parts.append(
                f'                <blockquote class="crossref-block">'
                f'<cite>{citation}</cite>'
                f'<p>{verse_text}</p>'
                f'</blockquote>'
            )
        
        html_parts.append('            </div>')
        return '\n'.join(html_parts)
    
    def _get_sample_verse_text(self, citation: str) -> str:
        """Get sample verse text for demonstration purposes."""
        # Sample texts for common references in Psalms 83
        sample_texts = {
            "Genesis 19:36-38": "So both daughters of Lot became pregnant by their father. The firstborn gave birth to a son and named him Moab. He is the father of the Moabites of today. The younger also gave birth to a son and named him Ben-ammi. He is the father of the Ammonites of today.",
            "Genesis 25:12-18": "This is the history of Ishmael... They settled from Havilah near Shur, which is east of Egypt, in the direction of Assyria.",
            "Judges 3:3": "The five lords of the Philistines, all the Canaanites, the Sidonians, and the Hivites dwelling on Mount Lebanon.",
            "Judges 4:15-24": "And Jehovah threw Sisera and all his war chariots and all his army into confusion before the sword of Barak... So on that day God subdued King Jabin of Canaan before the Israelites.",
            "Judges 7:25": "They captured the two princes of Midian, Oreb and Zeeb, and they killed Oreb at the rock of Oreb, and Zeeb they killed at the winepress of Zeeb.",
            "Judges 8:21": "At that Zebah and Zalmunna said: 'Get up and strike us down yourself, for as a man is, so is his might.' So Gideon got up and killed Zebah and Zalmunna.",
            "Exodus 6:3": "I used to appear to Abraham, Isaac, and Jacob as God Almighty, but with regard to my name Jehovah I did not make myself known to them.",
            "Isaiah 42:8": "I am Jehovah. That is my name; I give my glory to no one else, nor my praise to graven images.",
            "Psalm 91:14": "Because he has set his affection on me, I will rescue him. I will protect him because he knows my name."
        }
        
        return sample_texts.get(citation, f"Sample verse text for {citation}. In the actual implementation, this would contain the full referenced verse text from the Bible.")
    
    def _build_css_with_variations(self) -> str:
        """Build CSS with styles for all variations."""
        base_css = super()._build_css()
        
        variation_css = """

/* Cross-Reference Variation Styles */

/* Variation A: Separate Paragraphs */
.crossref-separate .crossref-paragraph {
    margin-bottom: 1em;
    padding-bottom: 0.8em;
    border-bottom: 1px solid #e0e0e0;
}

.crossref-separate .crossref-paragraph:last-child {
    border-bottom: none;
}

.crossref-citation-header {
    font-weight: bold;
    color: #000;
    margin-bottom: 0.3em;
    font-size: 0.95em;
}

.crossref-verse-text {
    color: #444;
    line-height: 1.5;
    padding-left: 0.5em;
}

/* Variation B: Inline with Markers */
.crossref-inline p {
    line-height: 1.7;
    color: #444;
}

.crossref-inline strong {
    color: #000;
    font-weight: 600;
}

/* Variation C: Indented Block Quote */
.crossref-blockquote {
    margin-left: 0;
}

.crossref-block {
    margin: 0.8em 0;
    padding-left: 15px;
    border-left: 3px solid #999;
    background-color: #f9f9f9;
}

.crossref-block cite {
    display: block;
    font-weight: bold;
    font-style: normal;
    color: #000;
    margin-bottom: 0.4em;
    font-size: 0.9em;
}

.crossref-block p {
    margin: 0;
    color: #444;
    line-height: 1.5;
}
"""
        
        return base_css + variation_css
    
    def generate_html(self, data: dict) -> str:
        """Override to use custom formatting methods."""
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
        css = self._build_css_with_variations()
        verses_html = self._format_verses(verses, superscription)
        study_panel_html = self._format_study_panel_with_style(data)
        
        # Assemble complete HTML document
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book} {chapter} - Cross-Reference Example ({self.crossref_style})</title>
    <style>
{css}
    </style>
</head>
<body>
    <header class="page-header">
        <h1>{book} {chapter}</h1>
        <p style="font-size: 0.9em; color: #666; font-style: italic;">
            Cross-Reference Style: {self.crossref_style.title()}
        </p>
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
        <p>{book} {chapter} - New World Translation Study Edition (Example: {self.crossref_style})</p>
    </footer>
</body>
</html>"""
        
        return html


def main():
    """Generate all three cross-reference example variations."""
    # Load Psalms 83 sample data
    sample_path = Path(__file__).parent.parent / "data" / "samples" / "psalms_83_sample.json"
    
    if not sample_path.exists():
        print(f"Error: Sample data not found at {sample_path}")
        return 1
    
    with open(sample_path, 'r') as f:
        data = json.load(f)
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "output" / "print" / "Psalms"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    variations = [
        ('separate', 'chapter_83_example1.html', 'Variation A: Separate Paragraphs'),
        ('inline', 'chapter_83_example2.html', 'Variation B: Inline with Markers'),
        ('blockquote', 'chapter_83_example3.html', 'Variation C: Indented Block Quote'),
    ]
    
    print("Generating Cross-Reference Formatting Examples")
    print("=" * 60)
    
    for style, filename, description in variations:
        formatter = CrossRefExampleFormatter(crossref_style=style)
        html = formatter.generate_html(data)
        
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ {description}")
        print(f"  Generated: {output_path}")
        print(f"  File size: {len(html):,} bytes")
        print()
    
    print("=" * 60)
    print("All examples generated successfully!")
    print()
    print("To review the examples:")
    print(f"  1. Open {output_dir / 'chapter_83_example1.html'} in your browser")
    print(f"  2. Open {output_dir / 'chapter_83_example2.html'} in your browser")
    print(f"  3. Open {output_dir / 'chapter_83_example3.html'} in your browser")
    print()
    print("Compare the cross-reference formatting in the right column to choose your preference.")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
