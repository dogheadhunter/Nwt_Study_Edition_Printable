# Printing Bible Study Materials

This guide explains how to generate print-ready PDFs from scraped Bible study data using the NWT Study Edition Printable formatter.

## Overview

The print formatter creates A4-sized PDFs with a two-column layout that matches the JW.org Study Bible website:

- **Left column (60%)**: Bible verses with verse numbers, superscription, and reference markers
- **Right column (40%)**: Study materials including footnotes, cross-references, and study notes
- **Professional layout**: Clean typography, proper spacing, and print-optimized CSS

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
- [Output Format](#output-format)
- [File Organization](#file-organization)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

Generate a PDF for Psalms 83:

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Generate PDF
python scripts/generate_print.py --book Psalms --chapter 83 --format pdf

# Output: output/print/Psalms/chapter_83.pdf
```

Open the generated PDF in any PDF reader (Adobe Reader, Chrome, etc.) and print or view.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
cd /path/to/Nwt_Study_Edition_Printable
pip install -r requirements.txt
```

This installs:
- `weasyprint>=60.0` - PDF generation library
- `beautifulsoup4>=4.12.0` - HTML parsing (for scraping)
- Other dependencies for web scraping

### System Dependencies (Linux Only)

On Linux, Weasyprint requires system libraries for rendering:

**Ubuntu/Debian:**
```bash
sudo apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info
```

**Fedora/CentOS:**
```bash
sudo dnf install -y \
    pango \
    gdk-pixbuf2 \
    libffi-devel
```

**macOS:**
No additional dependencies needed (install via Homebrew if issues occur):
```bash
brew install pango gdk-pixbuf libffi
```

**Windows:**
No additional dependencies needed. Weasyprint includes pre-compiled binaries.

---

## Usage

### Command Line Interface

The `scripts/generate_print.py` script provides a simple CLI for PDF generation.

#### Basic Usage

```bash
python scripts/generate_print.py --book BOOK --chapter CHAPTER [OPTIONS]
```

#### Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--book` | ✅ Yes | Book name | `Psalms`, `Genesis` |
| `--chapter` | See note | Chapter number | `83`, `1` |
| `--all-chapters` | See note | Process all chapters | (flag) |
| `--format` | No | Output format: `html`, `pdf`, `both` | Default: `pdf` |
| `--output-dir` | No | Output directory | Default: `output/print` |

**Note:** Either `--chapter` or `--all-chapters` must be specified, but not both.

#### Examples

**Generate PDF for a single chapter:**
```bash
python scripts/generate_print.py --book Psalms --chapter 83 --format pdf
```

**Generate both HTML and PDF:**
```bash
python scripts/generate_print.py --book Psalms --chapter 83 --format both
```

**Generate HTML only (for preview):**
```bash
python scripts/generate_print.py --book Genesis --chapter 1 --format html
```

**Batch process all available chapters:**
```bash
python scripts/generate_print.py --book Psalms --all-chapters --format pdf
```

This will:
- Discover all available chapter files for the book
- Process each chapter in order
- Show progress: `[1/150] Processing Psalms 1... ✓`
- Generate a summary report with success/failure counts
- Continue processing even if some chapters fail

**Custom output directory:**
```bash
python scripts/generate_print.py --book Psalms --chapter 83 \
    --format pdf --output-dir ~/Documents/Bible
```

**View help:**
```bash
python scripts/generate_print.py --help
```

### Python API

You can also use the formatter programmatically in your Python code.

#### Basic Example

```python
import json
from src.formatters.study_print_formatter import StudyBiblePrintFormatter

# Load chapter data
with open('data/samples/psalms_83_sample.json', 'r') as f:
    data = json.load(f)

# Create formatter
formatter = StudyBiblePrintFormatter()

# Generate HTML
html = formatter.generate_html(data)
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Generate PDF
formatter.generate_pdf(data, 'output.pdf')
```

#### Custom Page Dimensions

```python
# Create formatter with custom page size (e.g., Letter: 215mm × 279mm)
formatter = StudyBiblePrintFormatter(page_width=215, page_height=279)

html = formatter.generate_html(data)
formatter.generate_pdf(data, 'output_letter.pdf')
```

#### API Reference

**`StudyBiblePrintFormatter(page_width=210, page_height=297)`**

Initialize formatter with page dimensions.

- **Parameters:**
  - `page_width` (int): Page width in millimeters (default: 210 for A4)
  - `page_height` (int): Page height in millimeters (default: 297 for A4)

**`generate_html(data: Dict) -> str`**

Generate HTML from chapter data.

- **Parameters:**
  - `data` (Dict): Chapter data with keys: `book`, `chapter`, `verses`, `study_notes`, `footnotes`, `cross_references`, `superscription` (optional)
- **Returns:** Complete HTML document as string
- **Raises:** `ValueError` if required fields are missing

**`generate_pdf(data: Dict, output_path: str) -> None`**

Generate PDF from chapter data.

- **Parameters:**
  - `data` (Dict): Chapter data (same format as `generate_html`)
  - `output_path` (str): Path where PDF should be saved
- **Returns:** None
- **Raises:**
  - `ValueError` if data is invalid or output_path is empty
  - `OSError` if unable to create directories or write file
  - `ImportError` if weasyprint is not installed

---

## Output Format

### Layout Specifications

- **Page size:** A4 (210mm × 297mm)
- **Margins:** 20mm top/bottom, 15mm left/right
- **Column layout:** CSS Grid with 60/40 split
  - Left column: 60% width (verses)
  - Right column: 40% width (study materials)
  - Gap: 10mm between columns

### Left Column (Verses)

- **Verse numbers:** Bold, inline with verse text
- **Superscription:** Italic, appears above first verse (if present)
- **Cross-reference markers:** Superscript letters (a, b, c, etc.)
- **Footnote markers:** Superscript symbols (*, †, etc.)
- **Formatting:** Optimized for readability with appropriate line spacing

### Right Column (Study Materials)

- **Verse headings:** Bold section headers (e.g., "Psalm 83:3")
- **Footnotes:** Marker (*, †) followed by explanation text
- **Cross-references:** Citation in bold, followed by verse text
- **Study notes:** Indented with proper spacing
- **Background:** Light gray (#f5f5f5) with subtle border

### Typography

- **Font:** Georgia (serif) for main text
- **Size:** 11pt base font size
- **Line height:** 1.6 for comfortable reading
- **Headers:** 18pt for chapter title, bold

---

## File Organization

Generated files follow this structure:

```
output/print/
├── Psalms/
│   ├── chapter_1.html
│   ├── chapter_1.pdf
│   ├── chapter_2.html
│   ├── chapter_2.pdf
│   └── ...
├── Genesis/
│   ├── chapter_1.html
│   ├── chapter_1.pdf
│   └── ...
└── [Other Books]/
    └── ...
```

### File Naming Convention

- **HTML:** `chapter_{number}.html`
- **PDF:** `chapter_{number}.pdf`
- **Directory:** `output/print/{BookName}/`

---

## Customization

### CSS Styling

You can customize the appearance by modifying the CSS in `src/formatters/study_print_formatter.py`.

#### Key CSS Classes

| Class | Purpose | Location |
|-------|---------|----------|
| `.page-header` | Chapter title header | Top of page |
| `.verses-column` | Left column container | 60% width |
| `.study-column` | Right column container | 40% width |
| `.verse` | Individual verse | Left column |
| `.verse-num` | Verse number | Inline, bold |
| `.superscription` | Chapter superscription | Italic |
| `.verse-heading` | Study section header | Right column |
| `.study-item` | Study material entry | Right column |

#### Example Customizations

**Change fonts:**
```python
# In _build_css() method, modify:
body {
    font-family: 'Arial', 'Helvetica', sans-serif;  # Change from Georgia
    font-size: 11pt;
}
```

**Adjust column widths:**
```python
# In _build_css() method, modify:
.content-grid {
    grid-template-columns: 55% 45%;  # Change from 60% 40%
    gap: 10mm;
}
```

**Change background color:**
```python
# In _build_css() method, modify:
.study-column {
    background-color: #e8f4f8;  # Change from #f5f5f5
}
```

### Page Dimensions

Common page sizes (width × height in mm):

| Size | Dimensions | Usage |
|------|------------|-------|
| A4 | 210 × 297 | Default, international standard |
| Letter | 215 × 279 | US standard |
| Legal | 215 × 355 | US legal documents |
| A5 | 148 × 210 | Half of A4 |

**Example: Use Letter size**
```python
formatter = StudyBiblePrintFormatter(page_width=215, page_height=279)
```

---

## Troubleshooting

### Common Issues

#### 1. Weasyprint Installation Fails

**Problem:** `pip install weasyprint` fails with compilation errors.

**Solution (Linux):**
```bash
# Install system dependencies first
sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0

# Then reinstall weasyprint
pip install --upgrade weasyprint
```

**Solution (Windows/macOS):**
```bash
# Use pre-built wheels
pip install --upgrade pip
pip install weasyprint
```

#### 2. PDF Generation Fails with "Unable to load font"

**Problem:** PDF generates but special characters appear as boxes.

**Solution:**
The formatter uses system fonts. Ensure Georgia or Times New Roman is installed:

**Linux:**
```bash
sudo apt-get install fonts-liberation
```

**macOS/Windows:**
Georgia and Times New Roman are installed by default.

#### 3. Chapter Data Not Found

**Problem:** `FileNotFoundError: Chapter data not found for Psalms 83`

**Solution:**
Ensure chapter data exists in one of these locations:
- `data/samples/psalms_83_sample.json`
- `data/processed/Psalms/chapter_83.json`

Scrape the chapter first if data doesn't exist.

#### 4. PDF File is Too Large

**Problem:** PDF exceeds 500 KB for a single chapter.

**Solution:**
This is unusual. Check if:
- High-resolution images are embedded (should not be)
- Multiple copies of the same chapter are included
- File corruption

Regenerate the PDF:
```bash
rm output/print/Psalms/chapter_83.pdf
python scripts/generate_print.py --book Psalms --chapter 83 --format pdf
```

Expected file size: 15-30 KB for typical chapters.

#### 5. Print Preview Doesn't Show Two Columns

**Problem:** HTML looks correct in browser but print preview shows single column.

**Solution:**
Ensure `@media print` rules are working. Try:
1. Use "Print to PDF" from browser instead of opening generated PDF
2. Check CSS is not being overridden by browser print settings
3. Use the PDF format instead of printing HTML directly

#### 6. Permission Denied When Writing Files

**Problem:** `PermissionError: [Errno 13] Permission denied: 'output/print/Psalms/chapter_83.pdf'`

**Solution:**
```bash
# Ensure output directory has write permissions
chmod -R u+w output/

# Or use a different output directory
python scripts/generate_print.py --book Psalms --chapter 83 \
    --output-dir ~/Documents/Bible
```

---

## Performance

### Benchmarks

Typical generation times on modern hardware:

| Operation | Time | File Size |
|-----------|------|-----------|
| HTML generation | < 0.1 seconds | 8-10 KB |
| PDF generation | 1-2 seconds | 15-30 KB |
| Batch (10 chapters) | 15-25 seconds | 150-300 KB |

### Optimization Tips

1. **Generate HTML for preview, PDF for final output:**
   ```bash
   # Quick preview
   python scripts/generate_print.py --book Psalms --chapter 83 --format html
   
   # Final output
   python scripts/generate_print.py --book Psalms --chapter 83 --format pdf
   ```

2. **Use batch processing for multiple chapters** (when available):
   ```bash
   python scripts/generate_print.py --book Psalms --all-chapters --format pdf
   ```

3. **Cache formatter instance** when processing multiple chapters programmatically:
   ```python
   formatter = StudyBiblePrintFormatter()  # Create once
   
   for chapter in range(1, 151):  # Reuse for all chapters
       data = load_chapter(chapter)
       formatter.generate_pdf(data, f'output/chapter_{chapter}.pdf')
   ```

---

## Additional Resources

- **Project Documentation:** See `docs/` directory for more guides
- **API Reference:** See `docs/API_DOCUMENTATION.md`
- **Code Examples:** See `examples/` directory
- **Test Suite:** See `tests/test_study_print_formatter.py`

---

## Support

For issues, questions, or contributions:

1. Check this documentation first
2. Review existing issues on GitHub
3. Create a new issue with details about your problem

Include in bug reports:
- Python version (`python --version`)
- Weasyprint version (`pip show weasyprint`)
- Operating system
- Full error message
- Steps to reproduce

---

**Last Updated:** February 4, 2026  
**Version:** 1.0
