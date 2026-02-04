# API and Data Structure Documentation

## Overview
This document describes the expected data structures and potential API endpoints for the JW.org Study Bible content.

## Data Models

### Book
Represents a single book of the Bible.

```json
{
  "id": "string",              // Unique identifier (e.g., "genesis", "matthew")
  "name": "string",            // Full book name
  "testament": "string",       // "Hebrew-Aramaic" or "Christian Greek"
  "book_number": "integer",    // Position in Bible (1-66)
  "chapter_count": "integer",  // Total chapters in book
  "abbreviation": "string",    // Short form (e.g., "Gen.", "Matt.")
  "has_study_notes": "boolean",
  "has_audio": "boolean",
  "introduction": "string"     // Book introduction/overview
}
```

### Chapter
Represents a chapter within a book.

```json
{
  "book_id": "string",
  "chapter_number": "integer",
  "verse_count": "integer",
  "introduction": "string",    // Optional chapter introduction
  "verses": [/* Verse objects */],
  "study_notes": [/* StudyNote objects */],
  "footnotes": [/* Footnote objects */],
  "cross_references": [/* CrossReference objects */],
  "media": [/* Media objects */]
}
```

### Verse
Represents a single Bible verse.

```json
{
  "verse_number": "integer",
  "text": "string",
  "footnote_markers": ["string"],      // IDs of associated footnotes
  "cross_reference_markers": ["string"], // IDs of cross-references
  "study_note_markers": ["string"]     // IDs of study notes
}
```

### StudyNote
Represents a study note for one or more verses.

```json
{
  "id": "string",              // Unique identifier
  "verse_reference": "string", // E.g., "1:1" or "1:1-3"
  "title": "string",           // Optional title
  "content": "string",         // HTML or plain text content
  "related_verses": ["string"], // Other verse references
  "media_references": ["string"], // IDs of related media
  "glossary_terms": ["string"] // Related glossary entries
}
```

### Footnote
Represents a footnote explaining text or translation.

```json
{
  "id": "string",
  "marker": "string",          // Symbol used in text (*, †, etc.)
  "verse_reference": "string",
  "content": "string",
  "type": "string"             // "translation", "definition", "explanation"
}
```

### CrossReference
Represents a cross-reference to other Bible verses.

```json
{
  "id": "string",
  "marker": "string",          // Letter used in margin (a, b, c, etc.)
  "source_verse": "string",    // Where this reference appears
  "target_verses": ["string"], // Referenced verses
  "description": "string"      // Optional explanation
}
```

### Media
Represents associated media content.

```json
{
  "id": "string",
  "type": "string",            // "image", "video", "audio"
  "title": "string",
  "description": "string",
  "url": "string",
  "thumbnail_url": "string",
  "related_verses": ["string"]
}
```

### GlossaryEntry
Represents a glossary term definition.

```json
{
  "term": "string",
  "definition": "string",
  "pronunciation": "string",   // Optional
  "hebrew_greek": "string",    // Original language term
  "related_terms": ["string"]
}
```

## Expected URL Patterns

Based on typical web structure, these patterns are likely:

### Books List
```
GET /en/library/bible/study-bible/books/
```
Returns list of all Bible books with metadata.

### Book Chapters List
```
GET /en/library/bible/study-bible/books/{book_id}/
```
Returns list of chapters for a specific book.

### Chapter Content
```
GET /en/library/bible/study-bible/books/{book_id}/{chapter_number}/
```
Returns complete chapter content with verses and study materials.

### Study Notes (Ajax)
```
GET /en/library/bible/study-bible/books/{book_id}/{chapter_number}/notes/{note_id}
```
May return individual study notes dynamically.

### Media Content
```
GET /en/library/bible/study-bible/books/{book_id}/media/{media_id}
```
Returns media item details.

## Query Parameters

Potential query parameters for content requests:

- `format`: Response format (html, json)
- `include`: Include specific content types (notes, footnotes, refs)
- `lang`: Language code (en, es, fr, etc.)

## Response Formats

### Books List Response
```json
{
  "testament": "Hebrew-Aramaic",
  "books": [
    {
      "id": "genesis",
      "name": "Genesis",
      "book_number": 1,
      "chapter_count": 50,
      "has_study_notes": true,
      "has_audio": true
    }
  ]
}
```

### Chapter Content Response
```json
{
  "book": {
    "id": "genesis",
    "name": "Genesis"
  },
  "chapter": 1,
  "verse_count": 31,
  "content": {
    "verses": [...],
    "study_notes": [...],
    "footnotes": [...],
    "cross_references": [...],
    "media": [...]
  }
}
```

## Data Relationships

### Verse → Study Note
- Verses reference study notes via `study_note_markers`
- Study notes reference verses via `verse_reference`

### Verse → Footnote
- Verses reference footnotes via `footnote_markers`
- Footnotes reference verses via `verse_reference`

### Verse → Cross Reference
- Verses reference cross-references via `cross_reference_markers`
- Cross-references link source and target verses

### Study Note → Media
- Study notes reference media via `media_references`
- Media items list related verses

### Study Note → Glossary
- Study notes reference glossary terms
- Glossary provides definitions for terms

## Storage Schema

### Recommended Database Structure

#### Tables

**books**
- id (PK)
- name
- testament
- book_number
- chapter_count
- abbreviation
- has_study_notes
- has_audio

**chapters**
- id (PK)
- book_id (FK)
- chapter_number
- verse_count
- introduction

**verses**
- id (PK)
- chapter_id (FK)
- verse_number
- text

**study_notes**
- id (PK)
- chapter_id (FK)
- verse_reference
- title
- content

**footnotes**
- id (PK)
- chapter_id (FK)
- marker
- verse_reference
- content
- type

**cross_references**
- id (PK)
- chapter_id (FK)
- marker
- source_verse

**cross_reference_targets**
- id (PK)
- cross_reference_id (FK)
- target_verse

**media**
- id (PK)
- type
- title
- description
- url
- thumbnail_url

**verse_media** (junction table)
- verse_id (FK)
- media_id (FK)

**glossary**
- id (PK)
- term
- definition
- pronunciation
- hebrew_greek

## Usage Examples

### Retrieving a Complete Chapter
```python
from src.scrapers.bible_scraper import BibleScraper
from src.parsers.html_parser import StudyBibleParser
from src.utils.storage import DataStorage

# Initialize components
scraper = BibleScraper(headless=True)
storage = DataStorage()

# Scrape chapter
chapter_data = scraper.get_chapter_content('/genesis', 1)

# Parse and structure data
parser = StudyBibleParser(chapter_data['html'])
structured_data = parser.parse_all()

# Save to storage
storage.save_chapter_data('Genesis', 1, structured_data)
```

### Querying Saved Data
```python
from src.utils.storage import DataStorage

storage = DataStorage()

# Load chapter data
data = storage.load_json('Genesis_chapter_1.json')

# Access verses
for verse in data['verses']:
    print(f"{verse['number']}: {verse['text']}")
    
# Access study notes
for note in data['study_notes']:
    print(f"Note for {note['reference']}: {note['content']}")
```

## Notes

1. **URL Patterns**: Actual patterns should be confirmed through browser network inspection
2. **Selectors**: HTML class names and IDs need to be identified from actual page source
3. **Rate Limiting**: Implement delays between requests (recommended: 2-5 seconds)
4. **Error Handling**: Handle missing content, network errors, and parsing failures
5. **Caching**: Cache responses to minimize repeated requests
