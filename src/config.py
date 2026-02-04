"""
Configuration settings for the Bible scraper.

This file contains all configurable parameters for the scraping process.
"""

# Base URLs
BASE_URL = "https://www.jw.org/en/library/bible/study-bible/books/"

# Scraping Settings
SCRAPING_CONFIG = {
    # Browser settings
    'headless': True,           # Run browser in headless mode
    'wait_time': 10,            # Default wait time for elements (seconds)
    'page_load_timeout': 30,    # Page load timeout (seconds)
    
    # Rate limiting
    'request_delay': 3,         # Delay between requests (seconds)
    'chapter_delay': 5,         # Delay between chapters (seconds)
    'book_delay': 10,           # Delay between books (seconds)
    
    # Retry settings
    'max_retries': 3,           # Maximum retry attempts
    'retry_delay': 5,           # Delay between retries (seconds)
    
    # Data collection
    'save_html': True,          # Save raw HTML for debugging
    'validate_data': True,      # Validate scraped data
}

# HTML Selectors (Updated from live scraping - Feb 4, 2026)
SELECTORS = {
    # Books list page
    'book_link': 'a.bookLink',                    # Links to individual books
    'book_name': '.bookName',                     # Book name element
    'testament_section': '.testament',            # Testament section container
    
    # Main content containers (LIVE-VERIFIED)
    'main_content': 'div.bodyTxt',               # Main text container
    'chapter_heading': 'h1.sectionHeading',      # Chapter heading
    'article': 'article',                        # Main article element
    
    # Chapter page - Verses (LIVE-VERIFIED)
    'verse_container': 'p.sb',                   # Verse paragraph (class="sb")
    'verse_number': 'span.verseNum',             # Verse number span
    'verse_section': 'div[id^="section"]',      # Section divs (section1, section2, etc.)
    'verse': 'p.sb',                             # Legacy - same as verse_container
    'verse_text': '.verseText',                  # Verse text (legacy)
    
    # Special content (LIVE-VERIFIED)
    'superscription': 'div#tt4',                 # Psalms superscription (specific ID)
    'superscription_generic': 'sup',             # Generic superscription
    'emphasis': 'em',                            # Emphasis text (e.g., "Selah")
    
    # Study materials - Sidebar (LIVE-VERIFIED)
    'tab_container': 'div.tabContainer',         # Tabbed sidebar container
    'study_note': 'div.studyNote',               # Study note container
    'study_note_section': 'div.tabSubSection.studyNotes',  # Study notes section
    'study_note_content': '.noteContent',        # Study note text
    'study_note_reference': '.reference',        # Verse reference
    
    # Footnotes (LIVE-VERIFIED)
    'footnote_marker': 'a.fn',                   # Footnote marker link (asterisk)
    'footnote_section': 'div.tabSubSection.footnotes',  # Footnotes section
    'footnote': 'div.footnote',                  # Footnote container
    'footnote_link': 'a.footnoteLink',           # Link to footnote
    
    # Cross-references (LIVE-VERIFIED)
    'cross_ref_marker': 'a.study-note-ref',      # Cross-ref marker link (letters)
    'cross_ref_section': 'div.tabSubSection.xRefs',  # Cross-refs section
    'cross_reference': 'div.crossReference',     # Cross-reference container (legacy)
    'cross_reference_marker': '.refMarker',      # Reference letter (legacy)
    'xref_item': 'div.xRef',                     # Individual cross-ref item
    'xref_citation': 'span.xRefCitation',        # Citation text
    'cross_reference_link': 'a.b',               # Cross-reference link
    
    # Media
    'media_container': '.mediaContainer',        # Media content container
    'video': 'video',                            # Video elements
    'audio': 'audio',                            # Audio elements
    'image': 'img.studyImage',                   # Images
    
    # Navigation
    'chapter_selector': '.chapterSelector',      # Chapter navigation
    'next_chapter': 'a.nextChapter',             # Next chapter button
    'prev_chapter': 'a.prevChapter',             # Previous chapter button
}

# Data Storage Settings
STORAGE_CONFIG = {
    'base_dir': 'data',                          # Base directory for data
    'raw_dir': 'data/raw',                       # Raw HTML storage
    'processed_dir': 'data/processed',           # Processed data storage
    'format': 'json',                            # Default format (json, csv)
    'indent': 2,                                 # JSON indentation
    'encoding': 'utf-8',                         # File encoding
}

# Logging Settings
LOGGING_CONFIG = {
    'level': 'INFO',                             # Logging level (DEBUG, INFO, WARNING, ERROR)
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'scraper.log',                       # Log file path
    'console': True,                             # Also log to console
}

# Bible Structure (For reference and validation)
BIBLE_BOOKS = {
    'Hebrew-Aramaic Scriptures': [
        {'name': 'Genesis', 'abbr': 'Ge', 'chapters': 50},
        {'name': 'Exodus', 'abbr': 'Ex', 'chapters': 40},
        {'name': 'Leviticus', 'abbr': 'Le', 'chapters': 27},
        {'name': 'Numbers', 'abbr': 'Nu', 'chapters': 36},
        {'name': 'Deuteronomy', 'abbr': 'De', 'chapters': 34},
        {'name': 'Joshua', 'abbr': 'Jos', 'chapters': 24},
        {'name': 'Judges', 'abbr': 'Jg', 'chapters': 21},
        {'name': 'Ruth', 'abbr': 'Ru', 'chapters': 4},
        {'name': '1 Samuel', 'abbr': '1Sa', 'chapters': 31},
        {'name': '2 Samuel', 'abbr': '2Sa', 'chapters': 24},
        {'name': '1 Kings', 'abbr': '1Ki', 'chapters': 22},
        {'name': '2 Kings', 'abbr': '2Ki', 'chapters': 25},
        {'name': '1 Chronicles', 'abbr': '1Ch', 'chapters': 29},
        {'name': '2 Chronicles', 'abbr': '2Ch', 'chapters': 36},
        {'name': 'Ezra', 'abbr': 'Ezr', 'chapters': 10},
        {'name': 'Nehemiah', 'abbr': 'Ne', 'chapters': 13},
        {'name': 'Esther', 'abbr': 'Es', 'chapters': 10},
        {'name': 'Job', 'abbr': 'Job', 'chapters': 42},
        {'name': 'Psalms', 'abbr': 'Ps', 'chapters': 150},
        {'name': 'Proverbs', 'abbr': 'Pr', 'chapters': 31},
        {'name': 'Ecclesiastes', 'abbr': 'Ec', 'chapters': 12},
        {'name': 'Song of Solomon', 'abbr': 'Ca', 'chapters': 8},
        {'name': 'Isaiah', 'abbr': 'Isa', 'chapters': 66},
        {'name': 'Jeremiah', 'abbr': 'Jer', 'chapters': 52},
        {'name': 'Lamentations', 'abbr': 'La', 'chapters': 5},
        {'name': 'Ezekiel', 'abbr': 'Eze', 'chapters': 48},
        {'name': 'Daniel', 'abbr': 'Da', 'chapters': 12},
        {'name': 'Hosea', 'abbr': 'Ho', 'chapters': 14},
        {'name': 'Joel', 'abbr': 'Joe', 'chapters': 3},
        {'name': 'Amos', 'abbr': 'Am', 'chapters': 9},
        {'name': 'Obadiah', 'abbr': 'Ob', 'chapters': 1},
        {'name': 'Jonah', 'abbr': 'Jon', 'chapters': 4},
        {'name': 'Micah', 'abbr': 'Mic', 'chapters': 7},
        {'name': 'Nahum', 'abbr': 'Na', 'chapters': 3},
        {'name': 'Habakkuk', 'abbr': 'Hab', 'chapters': 3},
        {'name': 'Zephaniah', 'abbr': 'Zep', 'chapters': 3},
        {'name': 'Haggai', 'abbr': 'Hag', 'chapters': 2},
        {'name': 'Zechariah', 'abbr': 'Zec', 'chapters': 14},
        {'name': 'Malachi', 'abbr': 'Mal', 'chapters': 4},
    ],
    'Christian Greek Scriptures': [
        {'name': 'Matthew', 'abbr': 'Mt', 'chapters': 28},
        {'name': 'Mark', 'abbr': 'Mr', 'chapters': 16},
        {'name': 'Luke', 'abbr': 'Lu', 'chapters': 24},
        {'name': 'John', 'abbr': 'Joh', 'chapters': 21},
        {'name': 'Acts', 'abbr': 'Ac', 'chapters': 28},
        {'name': 'Romans', 'abbr': 'Ro', 'chapters': 16},
        {'name': '1 Corinthians', 'abbr': '1Co', 'chapters': 16},
        {'name': '2 Corinthians', 'abbr': '2Co', 'chapters': 13},
        {'name': 'Galatians', 'abbr': 'Ga', 'chapters': 6},
        {'name': 'Ephesians', 'abbr': 'Eph', 'chapters': 6},
        {'name': 'Philippians', 'abbr': 'Php', 'chapters': 4},
        {'name': 'Colossians', 'abbr': 'Col', 'chapters': 4},
        {'name': '1 Thessalonians', 'abbr': '1Th', 'chapters': 5},
        {'name': '2 Thessalonians', 'abbr': '2Th', 'chapters': 3},
        {'name': '1 Timothy', 'abbr': '1Ti', 'chapters': 6},
        {'name': '2 Timothy', 'abbr': '2Ti', 'chapters': 4},
        {'name': 'Titus', 'abbr': 'Tit', 'chapters': 3},
        {'name': 'Philemon', 'abbr': 'Phm', 'chapters': 1},
        {'name': 'Hebrews', 'abbr': 'Heb', 'chapters': 13},
        {'name': 'James', 'abbr': 'Jas', 'chapters': 5},
        {'name': '1 Peter', 'abbr': '1Pe', 'chapters': 5},
        {'name': '2 Peter', 'abbr': '2Pe', 'chapters': 3},
        {'name': '1 John', 'abbr': '1Jo', 'chapters': 5},
        {'name': '2 John', 'abbr': '2Jo', 'chapters': 1},
        {'name': '3 John', 'abbr': '3Jo', 'chapters': 1},
        {'name': 'Jude', 'abbr': 'Jude', 'chapters': 1},
        {'name': 'Revelation', 'abbr': 'Re', 'chapters': 22},
    ]
}

# User Agent (to identify requests)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Features to scrape
FEATURES = {
    'verses': True,              # Scrape Bible verses
    'study_notes': True,         # Scrape study notes
    'footnotes': True,           # Scrape footnotes
    'cross_references': True,    # Scrape cross-references
    'media': False,              # Scrape media (images, videos) - May require additional storage
    'audio': False,              # Scrape audio files - Requires significant storage
    'introductions': True,       # Scrape book/chapter introductions
}
