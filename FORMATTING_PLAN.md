# Bible Print Formatting Implementation Plan

**Project:** NWT Study Edition Printable  
**Goal:** Create A4 two-column print layout (60% verses, 40% study materials)  
**Target Output:** PDF files organized by book/chapter  
**Started:** February 4, 2026

---

## Overview

Implement a print formatter that replicates the JW.org Study Bible website layout with verses on the left (60%) and study materials (footnotes, cross-references with verse text, study notes) on the right (40%), formatted for A4 printing.

---

## Phase 1: Core Formatter Implementation

### Checkpoint 1.1: Create Study Print Formatter Class
**File:** `src/formatters/study_print_formatter.py`

**Tasks:**
- [ ] Create `StudyBiblePrintFormatter` class with `__init__()` method
- [ ] Add `generate_html(data: Dict) -> str` method skeleton
- [ ] Add private methods: `_format_verses()`, `_format_study_panel()`, `_build_css()`
- [ ] Add docstrings for all methods following Google style

**Success Criteria:**
- ✅ Class can be instantiated without errors
- ✅ `generate_html()` returns valid HTML string (even if minimal)
- ✅ All methods have proper type hints
- ✅ Docstrings explain purpose and parameters

**Validation:**
```python
from src.formatters.study_print_formatter import StudyBiblePrintFormatter
formatter = StudyBiblePrintFormatter()
html = formatter.generate_html({"book": "Test", "chapter": 1, "verses": []})
assert isinstance(html, str)
assert "<html" in html
```

---

### Checkpoint 1.2: Implement CSS Grid Layout
**File:** `src/formatters/study_print_formatter.py` (CSS section)

**Tasks:**
- [ ] Create `@page` rule with A4 dimensions (210mm × 297mm)
- [ ] Set page margins (20mm top/bottom, 15mm left/right)
- [ ] Implement two-column CSS Grid: 60% left, 40% right with 10mm gap
- [ ] Add page header styling with book/chapter name
- [ ] Add page footer styling with page numbers
- [ ] Configure print-specific rules (`@media print`)

**Success Criteria:**
- ✅ HTML validates as proper HTML5
- ✅ CSS Grid creates exactly 60/40 column split
- ✅ Page size is A4 (210mm × 297mm)
- ✅ Margins are consistent (20mm top/bottom, 15mm sides)
- ✅ Headers and footers appear on every page

**Validation:**
- Open generated HTML in Chrome
- Print Preview → Check page size shows "A4"
- Use browser DevTools → Measure column widths (should be ~60/40 ratio)
- Verify headers/footers appear

---

### Checkpoint 1.3: Format Left Column (Verses)
**File:** `src/formatters/study_print_formatter.py` (`_format_verses()` method)

**Tasks:**
- [ ] Implement superscription formatting (italic, left column only)
- [ ] Format verse numbers as bold inline elements
- [ ] Add cross-reference markers (a, b, c) as superscript
- [ ] Add footnote markers (*, †) as superscript
- [ ] Apply `page-break-inside: avoid` to prevent verse splitting
- [ ] Handle special characters (ʹ, ·) properly

**Success Criteria:**
- ✅ Verse numbers appear inline and bold
- ✅ Superscript markers (a, b, c, *) are visible and properly positioned
- ✅ Verses never split across pages
- ✅ Special characters display correctly (not as boxes/question marks)
- ✅ Superscription stays in left column only

**Validation:**
```python
# Test with Psalms 83 data
data = load_json("data/processed/psalms_83_live_test.json")
formatter = StudyBiblePrintFormatter()
html = formatter.generate_html(data)

# Check HTML contains:
assert 'class="superscription"' in html
assert 'class="verse-num"' in html
assert '<sup>' in html  # For markers
```

---

### Checkpoint 1.4: Format Right Column (Study Materials)
**File:** `src/formatters/study_print_formatter.py` (`_format_study_panel()` method)

**Tasks:**
- [ ] Create verse heading sections ("Psalm 83:1", "Psalm 83:4", etc.)
- [ ] Format footnotes with marker and content
- [ ] Format cross-references with citation + full verse text
- [ ] Format study notes with content
- [ ] Show blank space when verse has no study materials
- [ ] Apply background shading (#f5f5f5) and borders

**Success Criteria:**
- ✅ Study panel has verse headings matching verse numbers
- ✅ Footnotes display marker (*, †) + explanation text
- ✅ Cross-references show citation (bold) + full verse text (349+ chars)
- ✅ Study notes appear with proper formatting
- ✅ Verses without study materials show blank space
- ✅ Background shading and borders are visible

**Validation:**
```python
# Test cross-reference formatting
cross_refs = data['cross_references']
html = formatter.generate_html(data)

# Should contain cross-ref verse text (100+ chars)
assert "In time there arose over Egypt" in html  # Ex 1:8-10 text
assert len([x for x in cross_refs if x['verses']]) > 0
```

---

## Phase 2: Cross-Reference Formatting Examples

### Checkpoint 2.1: Create Example Variation A (Separate Paragraphs)
**File:** `output/print/Psalms/chapter_83_example1.html`

**Tasks:**
- [ ] Generate HTML with cross-ref verses as separate `<p>` blocks
- [ ] Each verse gets own paragraph with citation header
- [ ] Add spacing between verse paragraphs
- [ ] Test with Psalms 83:4 cross-ref 'd' (3 verses: Ex 1:8-10, 2Ch 20:1, Es 3:6)

**Success Criteria:**
- ✅ Each cross-ref verse is in separate paragraph
- ✅ Citation appears as bold header above verse text
- ✅ Readable spacing between paragraphs (0.5em minimum)
- ✅ File generated without errors

**Validation:**
- Open `chapter_83_example1.html` in browser
- Find cross-ref 'd' in right column
- Count paragraphs: should see 3 separate blocks for the 3 verses
- Measure spacing: paragraphs should not be cramped

---

### Checkpoint 2.2: Create Example Variation B (Inline with Markers)
**File:** `output/print/Psalms/chapter_83_example2.html`

**Tasks:**
- [ ] Generate HTML with cross-ref verses inline with citation markers
- [ ] Format as: **Exodus 1:8-10:** verse text **2 Chronicles 20:1:** verse text
- [ ] Use bold for citations, regular for verse text
- [ ] Test readability with long multi-verse references

**Success Criteria:**
- ✅ Verses flow continuously in single paragraph
- ✅ Citation markers are bold and distinguishable
- ✅ Text flows naturally without awkward breaks
- ✅ Long references (300+ chars) remain readable

**Validation:**
- Open `chapter_83_example2.html` in browser
- Read cross-ref 'd': should flow like "**Exodus 1:8-10:** 8 In time there arose... **2 Chronicles 20:1:** 20 Afterward..."
- Check readability: can you easily distinguish where each verse starts?

---

### Checkpoint 2.3: Create Example Variation C (Indented Block Quote)
**File:** `output/print/Psalms/chapter_83_example3.html`

**Tasks:**
- [ ] Generate HTML with cross-ref verses in block quote style
- [ ] Add left border and indentation
- [ ] Citation as small header, verse text indented below
- [ ] Apply subtle background color to differentiate

**Success Criteria:**
- ✅ Block quote styling is visually distinct
- ✅ Left border (2-3px) and indentation (15-20px) present
- ✅ Citation headers are visually separated from verse text
- ✅ Background color enhances readability

**Validation:**
- Open `chapter_83_example3.html` in browser
- Cross-ref verses should look like quoted blocks
- Check CSS: `border-left: 3px solid #ccc; padding-left: 15px;`
- Background should be subtle (e.g., #f9f9f9)

---

## Phase 3: PDF Generation

### Checkpoint 3.1: Add Weasyprint Dependency
**File:** `requirements.txt`

**Tasks:**
- [ ] Add `weasyprint>=60.0` to requirements.txt
- [ ] Install with `pip install -r requirements.txt`
- [ ] Test Weasyprint import and basic PDF generation
- [ ] Handle any missing system dependencies (on Linux: libpango, libcairo)

**Success Criteria:**
- ✅ `weasyprint>=60.0` in requirements.txt
- ✅ `pip install -r requirements.txt` completes without errors
- ✅ `from weasyprint import HTML` works in Python
- ✅ Can generate simple test PDF

**Validation:**
```bash
pip install -r requirements.txt
python -c "from weasyprint import HTML; HTML(string='<h1>Test</h1>').write_pdf('/tmp/test.pdf')"
ls -lh /tmp/test.pdf  # Should exist and be > 0 bytes
```

---

### Checkpoint 3.2: Implement PDF Export Function
**File:** `src/formatters/study_print_formatter.py` (`generate_pdf()` method)

**Tasks:**
- [ ] Add `generate_pdf(data: Dict, output_path: str) -> None` method
- [ ] Use Weasyprint to convert HTML to PDF
- [ ] Set PDF metadata (title, subject, author)
- [ ] Configure font embedding for special characters
- [ ] Handle file path creation (create directories if needed)

**Success Criteria:**
- ✅ `generate_pdf()` creates valid PDF file at specified path
- ✅ PDF metadata includes "{Book} {Chapter}" as title
- ✅ Special characters (ʹ, ·) render correctly in PDF
- ✅ Directories auto-created if they don't exist
- ✅ File size is reasonable (< 500KB for single chapter)

**Validation:**
```python
formatter = StudyBiblePrintFormatter()
output = "/tmp/test_output.pdf"
formatter.generate_pdf(data, output)

assert os.path.exists(output)
assert os.path.getsize(output) > 1000  # At least 1KB
# Open PDF and verify special characters visible
```

---

## Phase 4: File Organization & Batch Processing

### Checkpoint 4.1: Create Print Generation Script
**File:** `scripts/generate_print.py`

**Tasks:**
- [ ] Create main script with argparse for CLI arguments
- [ ] Add `--book` argument (required, e.g., "Psalms")
- [ ] Add `--chapter` argument (optional, single chapter number)
- [ ] Add `--all-chapters` flag for batch processing
- [ ] Add `--format` argument for output format (html/pdf/both)
- [ ] Implement file organization: `output/print/{book}/chapter_{num}.pdf`

**Success Criteria:**
- ✅ Script runs without errors: `python scripts/generate_print.py --book Psalms --chapter 83`
- ✅ Creates directory structure: `output/print/Psalms/`
- ✅ Generates file: `output/print/Psalms/chapter_83.pdf`
- ✅ Help text displays: `python scripts/generate_print.py --help`
- ✅ Error handling for missing book/chapter data

**Validation:**
```bash
python scripts/generate_print.py --book Psalms --chapter 83 --format pdf
ls -lh output/print/Psalms/chapter_83.pdf  # Should exist

python scripts/generate_print.py --book Psalms --chapter 83 --format html
ls -lh output/print/Psalms/chapter_83.html  # Should exist

python scripts/generate_print.py --help  # Should show usage
```

---

### Checkpoint 4.2: Implement Batch Processing
**File:** `scripts/generate_print.py` (batch mode)

**Tasks:**
- [ ] Add `--all-chapters` functionality
- [ ] Load all chapter JSON files from `data/processed/{book}/`
- [ ] Generate PDF for each chapter found
- [ ] Add progress indicator (e.g., "Processing chapter 1 of 150...")
- [ ] Create summary report of generated files

**Success Criteria:**
- ✅ `--all-chapters` processes multiple chapters
- ✅ Progress indicator shows current chapter being processed
- ✅ All chapters generate without errors
- ✅ Summary report lists all generated files
- ✅ Errors in one chapter don't stop entire batch

**Validation:**
```bash
# Assuming you have multiple chapters scraped
python scripts/generate_print.py --book Psalms --all-chapters

# Check output directory
ls output/print/Psalms/
# Should see: chapter_1.pdf, chapter_2.pdf, etc.

# Verify summary output includes count
# Expected: "Generated 150 chapters successfully"
```

---

## Phase 5: Documentation & Testing

### Checkpoint 5.1: Create Printing Documentation
**File:** `docs/PRINTING.md`

**Tasks:**
- [ ] Document website-style layout (60% verses, 40% study)
- [ ] Provide usage examples with screenshots/examples
- [ ] Explain file organization structure
- [ ] Add CSS customization guide (fonts, spacing, colors)
- [ ] Include troubleshooting section (common issues + solutions)
- [ ] Document Weasyprint installation for different OS

**Success Criteria:**
- ✅ Documentation includes at least 3 usage examples
- ✅ File organization is clearly explained with directory tree
- ✅ CSS customization section has code examples
- ✅ Troubleshooting covers: missing fonts, print issues, PDF generation errors
- ✅ OS-specific installation notes (Linux, macOS, Windows)

**Validation:**
- Read through documentation end-to-end
- Follow a usage example step-by-step: should work without errors
- Check troubleshooting: covers common error messages seen during dev

---

### Checkpoint 5.2: Create Test Suite for Formatter
**File:** `tests/test_study_print_formatter.py`

**Tasks:**
- [ ] Test HTML generation with minimal data
- [ ] Test HTML generation with full Psalms 83 data
- [ ] Test cross-reference formatting (all 3 variations)
- [ ] Test PDF generation and file creation
- [ ] Test batch processing with multiple chapters
- [ ] Test error handling (missing data, invalid paths)

**Success Criteria:**
- ✅ All tests pass: `pytest tests/test_study_print_formatter.py`
- ✅ Code coverage > 80% for formatter module
- ✅ Tests validate HTML structure (has left/right columns)
- ✅ Tests check PDF file is created and valid
- ✅ Edge cases tested (empty verses, missing study materials)

**Validation:**
```bash
pytest tests/test_study_print_formatter.py -v
pytest tests/test_study_print_formatter.py --cov=src/formatters/study_print_formatter
# Coverage should be > 80%
```

---

## Phase 6: Polish & Refinement

### Checkpoint 6.1: User Review & Format Selection
**Deliverable:** User selects preferred cross-reference format

**Tasks:**
- [ ] Present all 3 example HTML files to user
- [ ] User reviews and selects preferred format (A, B, or C)
- [ ] Finalize `generate_html()` to use selected format
- [ ] Remove unused format variations from code

**Success Criteria:**
- ✅ User has reviewed all 3 examples
- ✅ User has clearly selected one format
- ✅ Selected format is implemented as default
- ✅ Code is cleaned up (unused variations removed)

**Validation:**
- Generate final PDF with selected format
- User confirms output matches expectations
- Code review: no dead code for unused formats

---

### Checkpoint 6.2: Performance Optimization
**File:** `src/formatters/study_print_formatter.py`

**Tasks:**
- [ ] Profile PDF generation time for single chapter
- [ ] Optimize HTML string building (use list + join vs concatenation)
- [ ] Cache CSS string (don't rebuild for every chapter)
- [ ] Add option to skip HTML file creation (direct HTML → PDF)
- [ ] Test batch processing speed (target: < 5 seconds per chapter)

**Success Criteria:**
- ✅ Single chapter PDF generates in < 3 seconds
- ✅ Batch processing 10 chapters completes in < 30 seconds
- ✅ Memory usage stays reasonable (< 500MB for batch job)
- ✅ CPU usage is efficient (no unnecessary recomputation)

**Validation:**
```bash
time python scripts/generate_print.py --book Psalms --chapter 83
# Should complete in < 3 seconds

# Profile batch
time python scripts/generate_print.py --book Psalms --all-chapters
# Measure time per chapter
```

---

## Final Deliverables Checklist

### Code Files
- [ ] `src/formatters/study_print_formatter.py` - Main formatter class
- [ ] `scripts/generate_print.py` - CLI script for PDF generation
- [ ] `tests/test_study_print_formatter.py` - Test suite
- [ ] `requirements.txt` - Updated with weasyprint

### Documentation
- [ ] `docs/PRINTING.md` - Complete printing guide
- [ ] `README.md` - Updated with printing section
- [ ] Code comments and docstrings - All public methods documented

### Example Outputs
- [ ] `output/print/Psalms/chapter_83_example1.html` - Format variation A
- [ ] `output/print/Psalms/chapter_83_example2.html` - Format variation B
- [ ] `output/print/Psalms/chapter_83_example3.html` - Format variation C
- [ ] `output/print/Psalms/chapter_83.pdf` - Final PDF with selected format

### Testing
- [ ] All unit tests pass (`pytest tests/test_study_print_formatter.py`)
- [ ] Integration test: Generate Psalms 83 PDF successfully
- [ ] Manual review: PDF opens correctly in Adobe Reader / Chrome
- [ ] Print test: Physical A4 print looks correct

---

## Success Metrics

**Overall Project Success:**
- ✅ Can generate A4 PDF from scraped JSON data
- ✅ PDF has 60/40 two-column layout (verses left, study right)
- ✅ Cross-references include full verse text (100-300+ chars)
- ✅ Footnotes display with markers and explanations
- ✅ Page headers/footers appear on every page
- ✅ Files organize as `output/print/{book}/chapter_{num}.pdf`
- ✅ Batch processing works for multiple chapters
- ✅ Documentation enables user to customize and generate PDFs

**Quality Metrics:**
- PDF file size: < 500KB per chapter
- Generation speed: < 3 seconds per chapter
- Test coverage: > 80%
- Code quality: Passes flake8/black/mypy checks
- User satisfaction: Selected format meets expectations

---

## Risk Management

### Potential Issues

1. **Weasyprint Installation Fails**
   - **Risk Level:** Medium
   - **Mitigation:** Provide OS-specific installation docs with system dependencies
   - **Fallback:** Provide HTML output only, user prints via browser

2. **Cross-Reference Verse Text Missing**
   - **Risk Level:** Low (already validated in demo)
   - **Mitigation:** Test with actual scraped data before finalizing
   - **Fallback:** Show citation only if verse text unavailable

3. **PDF Generation Too Slow**
   - **Risk Level:** Low
   - **Mitigation:** Profile and optimize; use caching
   - **Fallback:** Accept slower speed for batch processing

4. **Layout Breaks on Different PDF Readers**
   - **Risk Level:** Medium
   - **Mitigation:** Test on multiple readers (Adobe, Chrome, Firefox)
   - **Fallback:** Document recommended readers

5. **Special Characters Don't Render**
   - **Risk Level:** Low
   - **Mitigation:** Embed fonts; test character set
   - **Fallback:** Use fallback fonts or character substitution

---

## Timeline Estimate

**Total Estimated Time:** 8-12 hours

- **Phase 1:** Core Formatter (3-4 hours)
- **Phase 2:** Example Variations (1-2 hours)
- **Phase 3:** PDF Generation (2-3 hours)
- **Phase 4:** File Organization (1-2 hours)
- **Phase 5:** Documentation & Testing (2-3 hours)
- **Phase 6:** Polish & Refinement (1-2 hours)

---

## Next Steps

1. Begin with **Checkpoint 1.1**: Create formatter class skeleton
2. Validate each checkpoint before proceeding to next
3. Pause at **Checkpoint 6.1** for user review of format examples
4. Complete final deliverables and run full test suite
5. Generate sample PDF and obtain user approval

---

**Document Version:** 1.0  
**Last Updated:** February 4, 2026  
**Status:** Planning Complete - Ready for Implementation
