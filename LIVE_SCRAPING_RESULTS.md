# Live Scraping Results - Psalms 83

**Date**: February 4, 2026  
**URL**: https://www.jw.org/en/library/bible/study-bible/books/psalms/83/  
**Status**: ✅ Successfully scraped

## Summary

Successfully navigated to Psalms 83 on JW.org and extracted the complete HTML using Playwright MCP tools.

## Verified Content

From the page snapshot and extracted HTML:

### ✅ Verses
- **Total**: 18 verses (confirmed)
- All verses from 1-18 are present in the HTML
- Each verse has proper structure with verse numbers

### ✅ Superscription
- Present: "A song. A melody of Aʹsaph"
- Linked to cross-reference "a" → 2Ch 20:14

### ✅ Special Content
- **"Selah"** appears in verse 8 (in italics/emphasis tag)
- **"Jehovah"** appears in verse 18: "May people know that you, whose name is Jehovah"

### ✅ Study Materials
- **Outline** section visible with:
  - "A prayer when facing enemies"
  - "O God, do not be silent" (1)
  - "Enemies like a whirling thistle" (13)
  - "God's name is Jehovah" (18)
  
- **Footnotes** (multiple)
  - Verse 1: "Or 'keep speechless.'"
  - Verse 2: "Or 'raise their heads.'"
  - Verse 3: "Lit., 'concealed ones.'"
  - Verse 5: "Lit., 'They consult with a heart together.'" / "Or 'a covenant.'"
  - Verse 8: "Lit., 'have become an arm to.'"
  - Verse 9: "Or 'wadi.'"
  - Verse 11: "Or 'leaders.'"
  - Verse 13: "Or 'like tumbleweed.'"
  - Verse 16: "Lit., 'Fill.'"

- **Cross-References** (extensive)
  - Each verse has multiple cross-references to other Bible books
  - References include: 2 Chronicles, Exodus, Judges, Genesis, Psalms, Isaiah, etc.

## HTML Structure Analysis

### Verse Structure
```html
<div class="bodyTxt">
  <div id="section1">
    <p id="p3" data-pid="3" class="sb">
      <sup><span id="v19083001-1" class="verse verseNum">1</span></sup>
      O God, do not be silent;
      <a class="study-note-ref" href="#xref">b</a>
    </p>
    <p id="p3" data-pid="3" class="sb">
      Do not keep quiet<a class="fn" href="#footnote">*</a> or still, O Divine One.
    </p>
  </div>
</div>
```

### Actual CSS Selectors Found

Based on the live HTML extraction:

```python
ACTUAL_SELECTORS = {
    # Main content containers
    'main_content': 'div.bodyTxt',
    'chapter_heading': 'h1.sectionHeading',
    
    # Verses
    'verse_container': 'p.sb',  # Paragraphs with class="sb"
    'verse_number': 'span.verseNum',  # Inside <sup> tag
    'verse_section': 'div[id^="section"]',  # Sections like "section1", "section2"
    
    # Special content
    'superscription': 'div#tt4',  # Specific ID for Psalms superscription
    'emphasis': 'em',  # For "Selah"
    
    # References
    'footnote_marker': 'a.fn',
    'cross_ref_marker': 'a.study-note-ref',
    
    # Study materials (in sidebar)
    'outline_section': 'div.tabContainer',
    'study_note_section': 'div.tabSubSection.studyNotes',
    'footnote_section': 'div.tabSubSection.footnotes',
    'xref_section': 'div.tabSubSection.xRefs',
}
```

## Key Findings

1. **Verse Structure**: Each verse is split across multiple `<p class="sb">` elements
2. **Verse Numbers**: Located in `<span class="verse verseNum">` inside `<sup>` tags
3. **Superscription**: Has specific ID `#tt4` for Psalms
4. **Study Materials**: Located in a tabbed sidebar with class `.tabContainer`
5. **References**: 
   - Footnotes: `<a class="fn">` with asterisk markers
   - Cross-refs: `<a class="study-note-ref">` with letter markers (a, b, c, etc.)

## Workflow Success

The following Playwright MCP workflow was successful:

1. ✅ `playwright-browser_navigate` → Page loaded
2. ✅ `playwright-browser_wait_for` → Content loaded
3. ✅ `playwright-browser_click` (Accept cookies) → Banner dismissed
4. ✅ `playwright-browser_snapshot` → Accessibility tree captured
5. ✅ `playwright-browser_evaluate` → Full HTML extracted

## Next Steps

1. ✅ Update `src/config.py` with actual selectors
2. ✅ Test BeautifulSoup parser with live HTML
3. ✅ Validate extracted data against expectations
4. ✅ Run integration tests
5. ⏳ Update `docs/WEBPAGE_STRUCTURE.md` with findings

## Notes

- Cookie consent banner must be dismissed before extracting content
- Page uses dynamic content loading (requires wait time)
- HTML structure is well-organized with semantic IDs and classes
- Study materials are in a separate sidebar (not inline with verses)
