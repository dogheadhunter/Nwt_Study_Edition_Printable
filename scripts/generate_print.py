#!/usr/bin/env python3
"""
Generate Print-Ready PDFs from Bible Study Data

This script generates HTML and/or PDF files from scraped Bible chapter data,
formatted for A4 printing with the two-column layout (60% verses, 40% study materials).

Usage:
    python scripts/generate_print.py --book Psalms --chapter 83 --format pdf
    python scripts/generate_print.py --book Psalms --all-chapters --format both
    python scripts/generate_print.py --book Genesis --chapter 1 --format html
"""

import argparse
import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Set

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.formatters.study_print_formatter import StudyBiblePrintFormatter


def discover_chapters(book: str) -> Set[int]:
    """
    Discover available chapter data files for a given book.
    
    Args:
        book: Book name (e.g., "Psalms")
        
    Returns:
        Set of chapter numbers that have data files available
        
    Note:
        Searches in:
        - data/samples/{book_lower}_{chapter}_sample.json
        - data/processed/{book}/chapter_{num}.json
    """
    chapters = set()
    base_dir = Path(__file__).parent.parent
    book_lower = book.lower()
    
    # Search in data/samples/
    samples_dir = base_dir / "data" / "samples"
    if samples_dir.exists():
        # Pattern: psalms_83_sample.json
        pattern = re.compile(rf'^{re.escape(book_lower)}_(\d+)_sample\.json$')
        for file in samples_dir.iterdir():
            if file.is_file():
                match = pattern.match(file.name)
                if match:
                    chapters.add(int(match.group(1)))
    
    # Search in data/processed/{book}/
    processed_dir = base_dir / "data" / "processed" / book
    if processed_dir.exists():
        # Pattern: chapter_1.json
        pattern = re.compile(r'^chapter_(\d+)\.json$')
        for file in processed_dir.iterdir():
            if file.is_file():
                match = pattern.match(file.name)
                if match:
                    chapters.add(int(match.group(1)))
    
    return chapters


def load_chapter_data(book: str, chapter: int, data_dir: Path = None) -> Dict[str, Any]:
    """
    Load chapter data from JSON file.
    
    Args:
        book: Book name (e.g., "Psalms")
        chapter: Chapter number
        data_dir: Base directory for data files (default: data/samples)
        
    Returns:
        Dictionary containing chapter data
        
    Raises:
        FileNotFoundError: If chapter data file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    if data_dir is None:
        # Try data/samples first (for testing)
        data_dir = Path(__file__).parent.parent / "data" / "samples"
    
    # Construct filename (e.g., "psalms_83_sample.json")
    book_lower = book.lower()
    filename = f"{book_lower}_{chapter}_sample.json"
    filepath = data_dir / filename
    
    if not filepath.exists():
        # Try alternate location: data/processed/{book}/chapter_{num}.json
        data_dir = Path(__file__).parent.parent / "data" / "processed" / book
        filepath = data_dir / f"chapter_{chapter}.json"
    
    if not filepath.exists():
        raise FileNotFoundError(
            f"Chapter data not found for {book} {chapter}\n"
            f"Looked for: {filepath}\n"
            f"Please scrape this chapter first or check the file location."
        )
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_chapter(
    book: str,
    chapter: int,
    output_format: str,
    output_dir: Path,
    formatter: StudyBiblePrintFormatter
) -> Dict[str, Any]:
    """
    Generate HTML/PDF for a single chapter.
    
    Args:
        book: Book name
        chapter: Chapter number
        output_format: 'html', 'pdf', or 'both'
        output_dir: Base output directory
        formatter: StudyBiblePrintFormatter instance
        
    Returns:
        Dictionary with 'success' (bool), 'files' (list), and 'error' (str if failed)
    """
    result = {
        'book': book,
        'chapter': chapter,
        'success': False,
        'files': [],
        'error': None
    }
    
    try:
        # Load chapter data
        data = load_chapter_data(book, chapter)
        
        # Create output directory structure
        book_dir = output_dir / book
        book_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate HTML if requested
        if output_format in ('html', 'both'):
            html_path = book_dir / f"chapter_{chapter}.html"
            html_content = formatter.generate_html(data)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            result['files'].append(str(html_path))
        
        # Generate PDF if requested
        if output_format in ('pdf', 'both'):
            pdf_path = book_dir / f"chapter_{chapter}.pdf"
            formatter.generate_pdf(data, str(pdf_path))
            result['files'].append(str(pdf_path))
        
        result['success'] = True
        
    except FileNotFoundError as e:
        result['error'] = str(e)
    except Exception as e:
        result['error'] = f"Error generating {book} {chapter}: {e}"
    
    return result


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate print-ready PDFs from Bible study data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate PDF for a single chapter:
    python scripts/generate_print.py --book Psalms --chapter 83 --format pdf
  
  Generate both HTML and PDF:
    python scripts/generate_print.py --book Psalms --chapter 83 --format both
  
  Generate all chapters in a book (if available):
    python scripts/generate_print.py --book Psalms --all-chapters --format pdf
        """
    )
    
    parser.add_argument(
        '--book',
        required=True,
        help='Book name (e.g., "Psalms", "Genesis")'
    )
    
    parser.add_argument(
        '--chapter',
        type=int,
        help='Chapter number (required unless --all-chapters is used)'
    )
    
    parser.add_argument(
        '--all-chapters',
        action='store_true',
        help='Process all available chapters for the book'
    )
    
    parser.add_argument(
        '--format',
        choices=['html', 'pdf', 'both'],
        default='pdf',
        help='Output format (default: pdf)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('output/print'),
        help='Output directory (default: output/print)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.all_chapters and args.chapter is None:
        parser.error("Either --chapter or --all-chapters must be specified")
    
    if args.all_chapters and args.chapter is not None:
        parser.error("Cannot use both --chapter and --all-chapters")
    
    # Create formatter
    formatter = StudyBiblePrintFormatter()
    
    # Process single chapter
    if args.chapter:
        print(f"Generating {args.format} for {args.book} {args.chapter}...")
        result = generate_chapter(
            args.book,
            args.chapter,
            args.format,
            args.output_dir,
            formatter
        )
        
        if result['success']:
            print(f"✓ Successfully generated:")
            for filepath in result['files']:
                print(f"  - {filepath}")
            return 0
        else:
            print(f"✗ Error: {result['error']}", file=sys.stderr)
            return 1
    
    # Process all chapters
    else:
        print(f"Processing all chapters for {args.book}...")
        
        # Discover available chapter files
        chapters = discover_chapters(args.book)
        
        if not chapters:
            print(f"\n✗ No chapter data files found for {args.book}")
            print(f"Looked in:")
            print(f"  - data/samples/{args.book.lower()}_{{chapter}}_sample.json")
            print(f"  - data/processed/{args.book}/chapter_{{num}}.json")
            print(f"\nPlease scrape chapters first or check file locations.")
            return 1
        
        print(f"Found {len(chapters)} chapter(s): {', '.join(map(str, sorted(chapters)))}")
        print()
        
        # Process each chapter
        results = []
        success_count = 0
        error_count = 0
        
        for i, chapter in enumerate(sorted(chapters), 1):
            print(f"[{i}/{len(chapters)}] Processing {args.book} {chapter}...", end=' ')
            
            result = generate_chapter(
                args.book,
                chapter,
                args.format,
                args.output_dir,
                formatter
            )
            
            results.append(result)
            
            if result['success']:
                print("✓")
                success_count += 1
            else:
                print(f"✗ {result['error']}")
                error_count += 1
        
        # Print summary
        print()
        print("=" * 60)
        print(f"Batch Processing Summary for {args.book}")
        print("=" * 60)
        print(f"Total chapters: {len(chapters)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {error_count}")
        
        if success_count > 0:
            print(f"\nGenerated files in: {args.output_dir / args.book}")
            
            # List all generated files
            all_files = []
            for result in results:
                if result['success']:
                    all_files.extend(result['files'])
            
            if all_files:
                print(f"Total files generated: {len(all_files)}")
        
        if error_count > 0:
            print(f"\n⚠ {error_count} chapter(s) failed to process")
            print("Failed chapters:")
            for result in results:
                if not result['success']:
                    print(f"  - {result['book']} {result['chapter']}: {result['error']}")
        
        # Return 0 if at least some chapters succeeded
        return 0 if success_count > 0 else 1


if __name__ == '__main__':
    sys.exit(main())
