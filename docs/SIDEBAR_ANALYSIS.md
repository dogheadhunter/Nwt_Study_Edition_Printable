# JW.org Study Bible Sidebar Analysis

## Date: February 4, 2026
## Page: Psalms 83 (https://www.jw.org/en/library/bible/study-bible/books/psalms/83/)

---

## Critical Discovery: Cross-Reference Verse Text Storage

### ❌ PROBLEM IDENTIFIED
The current scraper extracts:
- ✅ Cross-reference markers (letters like 'a', 'b', 'c')
- ✅ Cross-reference citations (e.g., "Ps 28:1", "Ex 1:8-10; 2Ch 20:1; Es 3:6")
- ❌ **MISSING: The actual text of the referenced verses**

### ✅ SOLUTION
The verse text is stored in **collapsed sections** within the sidebar that only appear when expanded.

---

## HTML Structure Analysis

### 1. Cross-References Section

**Location:** `div.tabContainer.xRefTab`

**Structure:**
```html
<div class="xRef210595971 xRef expander cms-clearfix" data-id="210595971" data-vs-id="19083004">
    <!-- Collapsed Header (Always Visible) -->
    <div class="expanderWrapper">
        <span class="sourceCitation">Ps 83:4</span>
        <span class="xRefID">d</span>
        <span class="targetCitation">Ex 1:8-10; 2Ch 20:1; Es 3:6</span>
        <div class="expanderIcon collapsed"></div>
    </div>
    
    <!-- Collapsible Content (Initially Hidden: style="display: none") -->
    <div class="jsCollapsableBlock cms-clearfix" style="display: none;">
        <!-- Multiple verses if multiple references -->
        <div class="xRefVerse">
            <div class="xRefVerseHeader">
                <span class="xRefCitation">Exodus 1:8-10</span>
                <div class="xRefCategoryIconContainer">
                    <span class="xRefCategory">General</span>
                </div>
            </div>
            <!-- THE ACTUAL VERSE TEXT IS HERE -->
            <p class="xRefContent publications pub-nwtsty dir-ltr ...">
                8 In time there arose over Egypt a new king...
                9 So he said to his people: "Look! The people...
                10 Let us deal shrewdly with them...
            </p>
        </div>
        
        <div class="xRefVerse">
            <div class="xRefVerseHeader">
                <span class="xRefCitation">2 Chronicles 20:1</span>
                <span class="xRefCategory">General</span>
            </div>
            <p class="xRefContent">
                20 Afterward the Moʹab·ites and the Amʹmon·ites...
            </p>
        </div>
        
        <!-- More verses... -->
    </div>
</div>
```

### 2. Footnotes Section

**Location:** `div.tabSubSection.footnotes`

**Structure:**
```html
<div class="tabSubSection footnotes">
    <h4 class="subSectionHeading">Footnotes</h4>
    
    <div class="footnote fn210596411" data-footnote-id="210596411">
        <span>Or "keep speechless."</span>
    </div>
    
    <div class="footnote fn210596420" data-footnote-id="210596420">
        <span>Lit., "Fill."</span>
    </div>
</div>
```

### 3. Study Notes Section

**Location:** `div.tabSubSection.studyNotes`

**Structure:** (appears to be empty for Psalms 83)
```html
<div class="tabSubSection studyNotes none">
    <h4 class="subSectionHeading">Study Notes</h4>
    <!-- Empty for this chapter -->
</div>
```

---

## Data Extraction Requirements

### Cross-References (UPDATED)

**What to extract:**
```python
{
    'id': '210595971',
    'verse_id': '19083004',  # Which verse this references (Ps 83:4)
    'marker': 'd',
    'citation': 'Ex 1:8-10; 2Ch 20:1; Es 3:6',
    'verses': [  # NEW: Extract the actual verse text
        {
            'citation': 'Exodus 1:8-10',
            'category': 'General',
            'content': '8 In time there arose over Egypt a new king...'
        },
        {
            'citation': '2 Chronicles 20:1',
            'category': 'General',
            'content': '20 Afterward the Moʹab·ites and the Amʹmon·ites...'
        },
        {
            'citation': 'Esther 3:6',
            'category': 'General',
            'content': '6 But he despised the thought...'
        }
    ]
}
```

### Footnotes

**What to extract:**
```python
{
    'id': '210596411',
    'marker': 'a',  # From the inline marker in verses
    'content': 'Or "keep speechless."'
}
```

### Study Notes

**What to extract:**
```python
{
    'id': '...',
    'verse_reference': 'Ps 83:1',  # Which verse it references
    'content': '...'
}
```

---

## Scraper Updates Needed

### Current Code Issues

1. **Cross-references `_extract_cross_references()` method:**
   - ✅ Extracts marker, citation
   - ❌ **Does NOT extract verse text from `.xRefVerse` elements**
   - ❌ Missing `.jsCollapsableBlock` parsing

2. **Footnotes `_extract_footnotes()` method:**
   - ✅ Should work correctly (footnotes not collapsed)

3. **Study Notes `_extract_study_notes()` method:**
   - ✅ Should work correctly

### Required Changes

**File:** `src/scrapers/psalms_scraper.py`

**Method:** `_extract_cross_references()`

**Current code:**
```python
def _extract_cross_references(self) -> List[Dict[str, Any]]:
    """Extract cross-references from sidebar."""
    cross_references = []
    xref_section = self.soup.find('div', class_=SELECTORS['cross_ref_section'])
    
    if not xref_section:
        return cross_references
    
    # Find all cross-reference items
    xref_items = xref_section.find_all('li')
    
    for item in xref_items:
        # Get the marker (letter/number)
        marker_elem = item.find('a', class_=SELECTORS['cross_ref_marker'])
        
        # Get verse links
        verse_links = item.find_all('a', class_='b')
        
        cross_references.append({
            'id': item.get('id', ''),
            'marker': marker_elem.text.strip() if marker_elem else '',
            'verses': [link.text.strip() for link in verse_links],
            'content': item.get_text(strip=True)
        })
    
    return cross_references
```

**SHOULD BE:**
```python
def _extract_cross_references(self) -> List[Dict[str, Any]]:
    """Extract cross-references from sidebar INCLUDING verse text."""
    cross_references = []
    
    # Find all cross-reference containers
    xref_containers = self.soup.find_all('div', class_='xRef')
    
    for container in xref_containers:
        xref_data = {
            'id': container.get('data-id', ''),
            'verse_id': container.get('data-vs-id', ''),
            'marker': '',
            'citation': '',
            'verses': []
        }
        
        # Get marker and citation from header
        marker_elem = container.find('span', class_='xRefID')
        if marker_elem:
            xref_data['marker'] = marker_elem.text.strip()
        
        citation_elem = container.find('span', class_='targetCitation')
        if citation_elem:
            xref_data['citation'] = citation_elem.text.strip()
        
        # Get verse content from collapsible block
        collapsible = container.find('div', class_='jsCollapsableBlock')
        if collapsible:
            verse_elements = collapsible.find_all('div', class_='xRefVerse')
            
            for verse_elem in verse_elements:
                citation = verse_elem.find('span', class_='xRefCitation')
                category = verse_elem.find('span', class_='xRefCategory')
                content = verse_elem.find('p', class_='xRefContent')
                
                xref_data['verses'].append({
                    'citation': citation.text.strip() if citation else '',
                    'category': category.text.strip() if category else '',
                    'content': content.get_text(strip=True) if content else ''
                })
        
        if xref_data['marker']:  # Only add if has marker
            cross_references.append(xref_data)
    
    return cross_references
```

---

## Testing Requirements

### Test Data Expectations for Psalms 83

**Cross-References:**
- Total: ~25+ cross-references
- Example: Marker 'd' for Ps 83:4
  - Should have 3 verse texts: Exodus 1:8-10, 2 Chronicles 20:1, Esther 3:6
  - Each verse should have full text (100+ characters)

**Footnotes:**
- Total: ~10+ footnotes
- Example: "Or 'keep speechless.'" for verse 1

**Verses:**
- Total: 18 verses
- Each with verse number, text, and markers

**Superscription:**
- Text: "A song. A melody of Aʹsaph."

---

## Next Steps

1. ✅ Document sidebar structure (this file)
2. ⏳ Update `_extract_cross_references()` method
3. ⏳ Save complete HTML (with sidebar) for testing
4. ⏳ Run test to verify verse text extraction
5. ⏳ Verify all 3 verse texts appear for multi-reference cross-refs
